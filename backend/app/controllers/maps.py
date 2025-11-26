import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
from fastapi.encoders import jsonable_encoder

from ..schemas import (
    PredictRequest,
    PredictResponse,
    FeatureCollection,
    DistributionRequest,
    DistributionResponse,
)

router = APIRouter(prefix="/maps", tags=["maps"])

MAPS_URL = os.getenv("EXPO_PUBLIC_MAPS_URL", "http://maps:8004")


@router.post("/predict")
async def predict_zone(payload: PredictRequest):
    """Forward predict request (lat/lon/timestamp) to the Maps service and
    return normalized species probability results.
    """
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            # payload may contain datetime objects; use jsonable_encoder to produce
            # JSON-serializable values (ISO strings for datetimes)
            resp = await client.post(f"{MAPS_URL}/predict", json=jsonable_encoder(payload))
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Maps service unavailable: {e}")

    # propagate upstream errors
    if resp.status_code >= 400:
        # try to extract JSON error when possible
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=resp.status_code, detail=detail)

    try:
        body = resp.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Maps service returned invalid JSON")

    # Return upstream JSON as-is (permissive proxy). If the upstream wraps the
    # result in {success,message,data} that wrapper will be forwarded too.
    return JSONResponse(content=body, status_code=resp.status_code)


@router.post("/distribution")
async def distribution(payload: DistributionRequest):
    """Proxy endpoint for full distribution (radius/grid) calculations.

    Forwards the request to the maps service `/distribution` endpoint and
    returns the upstream JSON response without enforcing a local Pydantic
    response model (permissive proxy). Use `jsonable_encoder(..., by_alias=True)`
    so the alias `"datetime"` is used when present.
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(
                f"{MAPS_URL}/distribution", json=jsonable_encoder(payload, by_alias=True)
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Maps service unavailable: {e}")

    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=resp.status_code, detail=detail)

    try:
        body = resp.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Maps service returned invalid JSON")

    return JSONResponse(content=body, status_code=resp.status_code)


@router.get("/zones")
async def get_zones():
    """Return zones as GeoJSON FeatureCollection by proxying the maps service.

    The maps service is expected to expose a GET /zones that returns a
    FeatureCollection or the wrapped shape { success, message, data } where
    data is the FeatureCollection.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(f"{MAPS_URL}/zones")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Maps service unavailable: {e}")

    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=resp.status_code, detail=detail)

    try:
        body = resp.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Maps service returned invalid JSON")

    return JSONResponse(content=body, status_code=resp.status_code)



@router.post("/distribution-zone")
async def distribution_zone(payload: DistributionRequest):
    """Proxy endpoint for distribution zone calculation.

    Forwards request to the maps service and returns species distributions for
    the requested point/grid.
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            # use by_alias=True so the JSON key "datetime" (alias) is used
            resp = await client.post(f"{MAPS_URL}/distribution-zone", json=jsonable_encoder(payload, by_alias=True))
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Maps service unavailable: {e}")

    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=resp.status_code, detail=detail)

    try:
        body = resp.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Maps service returned invalid JSON")

    return JSONResponse(content=body, status_code=resp.status_code)
