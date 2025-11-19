import os
from typing import Optional
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import time
import asyncio
from typing import Dict, Tuple

from ..schemas import (
    UserSignupRequest,
    UserLoginRequest,
    SignupResponse,
    LoginResponse,
    UserResponse,
)

security = HTTPBearer()

router = APIRouter(prefix="/users", tags=["users"])

USERS_URL = os.getenv("USERS_URL", "http://users:8001")
USER_PROFILE_CACHE_TTL = int(os.getenv("USER_PROFILE_CACHE_TTL", "60"))

# Simple in-memory TTL cache for profiles keyed by token. Stored value is
# (data_dict, expiry_timestamp). Protected by an asyncio.Lock.
_profile_cache: Dict[str, Tuple[dict, float]] = {}
_profile_cache_lock = asyncio.Lock()


async def _get_cached_profile(token: str) -> Optional[dict]:
    now = time.time()
    async with _profile_cache_lock:
        entry = _profile_cache.get(token)
        if not entry:
            return None
        data, expiry = entry
        if expiry < now:
            # expired
            del _profile_cache[token]
            return None
        return data


async def _set_cached_profile(token: str, data: dict) -> None:
    expiry = time.time() + USER_PROFILE_CACHE_TTL
    async with _profile_cache_lock:
        _profile_cache[token] = (data, expiry)


async def _get_current_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    return f"Bearer {credentials.credentials}"


async def get_current_user(token: str = Depends(_get_current_token)) -> dict:
    """Dependency that returns the current user's profile (data dict).

    This calls the Users service /profile endpoint and returns the inner
    `data` payload so other controllers can use the authenticated user's id
    without duplicating token handling.
    """
    # Try cache first
    cached = await _get_cached_profile(token)
    if cached is not None:
        return cached

    headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{USERS_URL}/profile", headers=headers)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    if resp.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    body = resp.json()
    data = body.get("data") if isinstance(body, dict) and "data" in body else body
    if isinstance(data, dict) and data.get("created_at") == "":
        data["created_at"] = None

    # store in cache for next time
    await _set_cached_profile(token, data)
    return data


@router.post("/signup", response_model=SignupResponse)
async def signup_user(request: UserSignupRequest):
    """Register user and auto-login by calling users service register + login."""
    email = request.email
    password = request.password
    name = request.name or email.split("@", 1)[0].replace('.', ' ').replace('_', ' ').title()

    # call register
    async with httpx.AsyncClient() as client:
        try:
            reg = await client.post(
                f"{USERS_URL}/register",
                json={"name": name, "email": email, "password": password},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    if reg.status_code != 201:
        raise HTTPException(status_code=reg.status_code, detail=reg.text)

    # login
    async with httpx.AsyncClient() as client:
        try:
            login = await client.post(
                f"{USERS_URL}/login",
                json={"email": email, "password": password},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    if login.status_code != 200:
        return reg.json()

    return {
        "success": True,
        "message": "User registered and logged in successfully",
        "data": reg.json().get("data", {}),
        "access_token": login.json().get("access_token"),
        "refresh_token": login.json().get("refresh_token"),
    }


@router.post("/login", response_model=LoginResponse)
async def login_user(request: UserLoginRequest):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{USERS_URL}/login", json={"email": request.email, "password": request.password})
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    return resp.json()


@router.get("/me", response_model=UserResponse)
async def get_me(token: str = Depends(_get_current_token)):
    headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{USERS_URL}/profile", headers=headers)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    if resp.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        data = body.get("data") or {}
    else:
        data = body

    # normalize created_at empty -> None
    if data.get("created_at") == "":
        data["created_at"] = None

    return data


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{USERS_URL}/users/{user_id}")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="User not found")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        data = body.get("data") or {}
    else:
        data = body

    if data.get("created_at") == "":
        data["created_at"] = None

    return data


@router.patch("/me/xp", response_model=UserResponse)
async def update_my_xp(token: str = Depends(_get_current_token), xp_to_add: int = 0):
    """Update XP for the authenticated user (determined from the token)."""
    # Resolve current user via dependency
    current = await get_current_user(token)
    user_id = current.get("user_id") or current.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unable to determine current user")

    headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.patch(
                f"{USERS_URL}/users/{user_id}/xp",
                headers=headers,
                params={"xp_to_add": xp_to_add},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="User not found")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    # Unwrap the users service response shape { success, message, data }
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        data = body.get("data") or {}
    else:
        data = body

    # normalize created_at empty -> None to satisfy Pydantic
    if data.get("created_at") == "":
        data["created_at"] = None

    return data


async def validate_user_exists(user_id: int) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{USERS_URL}/users/{user_id}")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="User not found")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return True
