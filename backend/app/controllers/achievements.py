import os
from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import List

from .users import validate_user_exists
from ..schemas import (
    AchievementCollectionResponse,
    AchievementUnlocked,
    AchievementDefinition,
    SpeciesLeaderboardEntry,
    XPLeaderboardEntry,
)

router = APIRouter(prefix="/achievements", tags=["achievements"])

ACHIEVEMENTS_URL = os.getenv("ACHIEVEMENTS_URL", "http://achievements:8003")


@router.get("/users/{user_id}/collection", response_model=AchievementCollectionResponse)
async def get_user_collection(user_id: int):
    # ensure user exists in users service
    await validate_user_exists(user_id)
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/achievements/users/{user_id}/collection")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/users/{user_id}/achievements", response_model=List[AchievementDefinition])
async def get_user_achievements(user_id: int):
    await validate_user_exists(user_id)
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/achievements/users/{user_id}/achievements")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/species/leaderboard", response_model=List[SpeciesLeaderboardEntry])
async def get_species_leaderboard():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/achievements/species/leaderboard")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/xp/leaderboard", response_model=List[XPLeaderboardEntry])
async def get_xp_leaderboard():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/achievements/xp/leaderboard")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
