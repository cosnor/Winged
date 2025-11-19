import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
import httpx
from ..schemas import SightingRequest, SightingResponse
from .users import get_current_user, get_user

router = APIRouter(prefix="/sightings", tags=["sightings"])

SIGHTINGS_URL = os.getenv("SIGHTINGS_URL", "http://sightings:8002")


@router.post("/", response_model=SightingResponse)
async def create_sighting(sighting: SightingRequest, current_user: dict = Depends(get_current_user)):
    # Ensure the sighting is created for the authenticated user. Override any
    # provided user_id in the incoming payload with the id from the authenticated
    # profile.
    # Convert the Pydantic model to a JSON-serializable structure.
    # Pydantic models may contain `datetime` objects which Python's
    # json.dumps cannot serialize. `jsonable_encoder` converts datetimes
    # to ISO strings (and handles other non-serializable values).
    payload = sighting.dict()
    payload["user_id"] = current_user.get("user_id")
    json_payload = jsonable_encoder(payload)

    async with httpx.AsyncClient() as client:
        try:
            # follow_redirects=True helps when the sightings service issues a 307/3xx
            # redirect (common if the service enforces trailing slashes or similar).
            resp = await client.post(f"{SIGHTINGS_URL}/sightings/", json=json_payload, follow_redirects=True)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=str(e))

    # Propagate upstream errors. If the sightings service failed with a 500
    # (internal error), return a 502 Bad Gateway to indicate the error
    # happened in an upstream service and include the upstream body for
    # debugging. For other statuses, propagate as-is.
    if resp.status_code >= 400:
        if resp.status_code == 500:
            detail = resp.text or "Sightings service internal error"
            raise HTTPException(status_code=502, detail=f"Upstream sightings service error: {detail}")
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    # Some upstream responses may not be JSON (empty body, plain text, etc.).
    # Attempt to decode JSON and provide a clear 502 if decoding fails.
    try:
        body = resp.json()
    except ValueError:
        raise HTTPException(status_code=502, detail=(resp.text or "Invalid/empty response from sightings service"))

    # Unwrap {"data": {...}} shapes to return the inner sighting object.
    sighting_resp = body.get("data") if isinstance(body, dict) and "data" in body else body

    # Normalize achievements_unlocked to always be a list of dicts.
    if isinstance(sighting_resp, dict):
        a = sighting_resp.get("achievements_unlocked")
        # handle None / missing
        if a is None:
            sighting_resp["achievements_unlocked"] = []
        else:
            # If the achievements service returned a wrapper {"data": [...]}
            if isinstance(a, dict) and "data" in a:
                norm = a.get("data") or []
                # if data is a single dict, wrap it
                if isinstance(norm, dict):
                    norm = [norm]
                sighting_resp["achievements_unlocked"] = norm
            elif isinstance(a, list):
                # already a list - leave as-is
                pass
            elif isinstance(a, dict):
                # single achievement object -> wrap in list
                sighting_resp["achievements_unlocked"] = [a]
            else:
                # unexpected type (string, number, etc.) -> set empty list for safety
                sighting_resp["achievements_unlocked"] = []

    # Try to enrich the returned sighting with the denormalized user profile
    try:
        uid = None
        if isinstance(sighting_resp, dict):
            uid = sighting_resp.get("user_id")
        if uid is not None:
            # get_user may raise HTTPException on failure; swallow errors and leave user None
            try:
                user_profile = await get_user(int(uid))
            except Exception:
                user_profile = None
            if user_profile:
                sighting_resp["user"] = user_profile
    except Exception:
        # Non-fatal: if enrichment fails, return the sighting without user
        pass

    return sighting_resp


@router.get("/{sighting_id}", response_model=SightingResponse)
async def get_sighting(sighting_id: int, current_user: dict = Depends(get_current_user)):
    """Retrieve a specific sighting and ensure it's owned by the authenticated user.

    If the sighting service returns the sighting wrapped in {"data": {...}},
    we unwrap it. If the sighting's user_id does not match the current user's
    id, return 403 Forbidden.
    """
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{SIGHTINGS_URL}/sightings/{sighting_id}")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    body = resp.json()
    sighting = body.get("data") if isinstance(body, dict) and "data" in body else body

    # Ensure ownership - be tolerant about types (str vs int) and key names.
    if not isinstance(sighting, dict):
        raise HTTPException(status_code=502, detail="Invalid sighting payload from sightings service")

    # Try common keys for user id
    sighting_user_id_raw = sighting.get("user_id") if "user_id" in sighting else sighting.get("userId")
    if sighting_user_id_raw is None:
        # unexpected shape from sightings service
        raise HTTPException(status_code=502, detail="Invalid sighting payload from sightings service: missing user_id")

    # current_user may come from users service; try common keys
    current_user_id_raw = current_user.get("user_id") if isinstance(current_user, dict) and "user_id" in current_user else current_user.get("id") if isinstance(current_user, dict) else None

    # Normalize to integers when possible for comparison
    def _to_int_maybe(v):
        try:
            return int(v)
        except Exception:
            return None

    sighting_user_id = _to_int_maybe(sighting_user_id_raw)
    current_user_id = _to_int_maybe(current_user_id_raw)

    # Debug logs to assist in local troubleshooting (can be removed later)
    print(f"BFF: sighting_user_id_raw={sighting_user_id_raw} sighting_user_id={sighting_user_id} current_user_raw={current_user_id_raw} current_user_id={current_user_id}")

    # If we could convert both to ints, compare them; otherwise compare as strings
    if sighting_user_id is not None and current_user_id is not None:
        if sighting_user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: sighting does not belong to the authenticated user")
    else:
        # fallback to string comparison
        if str(sighting_user_id_raw) != str(current_user_id_raw):
            raise HTTPException(status_code=403, detail="Forbidden: sighting does not belong to the authenticated user")

    return sighting

@router.get("/{user_id}/sightings")
async def get_user_sightings(user_id: int, limit: int = 50, current_user: dict = Depends(get_current_user)):
        """Get sightings for a specific user, ensuring it matches the authenticated user."""
        # Ensure the requested user_id matches the authenticated user's id
        current_user_id = current_user.get("user_id")
        if int(user_id) != int(current_user_id):
            raise HTTPException(status_code=403, detail="Forbidden: cannot access sightings of other users")
    
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{SIGHTINGS_URL}/users/{user_id}/sightings", params={"limit": limit})
            except Exception as e:
                raise HTTPException(status_code=502, detail=str(e))
    
        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
    
        body = resp.json()
        sightings = body.get("data") if isinstance(body, dict) and "data" in body else body
    
        return sightings                                            