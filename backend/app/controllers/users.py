import os
from typing import Optional
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

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


async def _get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return f"Bearer {credentials.credentials}"


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
