import os
from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import List

from .users import validate_user_exists, get_current_user
from ..schemas import (
    AchievementCollectionResponse,
    AchievementUnlocked,
    AchievementDefinition,
    SpeciesLeaderboardEntry,
    XPLeaderboardEntry,
    # service-mirroring models
    AchievementResponse,
    UserAchievementResponse,
    UserStatsResponse,
    UserCollectionResponse,
    AchievementProgressResponse,
    LeaderboardEntryResponse,
    SpeciesListResponse,
)

router = APIRouter(prefix="/achievements", tags=["achievements"])

ACHIEVEMENTS_URL = os.getenv("ACHIEVEMENTS_URL", "http://achievements:8003")


def _normalize_collection_payload(payload: dict) -> dict:
    """Normalize various achievements service payload shapes into the
    `AchievementCollectionResponse` shape: { user_id, achievements: [...] }.

    The achievements service currently returns a richer structure with
    `birds`, `stats`, and `recent_achievements`. We map `recent_achievements`
    into the simple `achievements` list expected by the BFF response model.
    """
    if not isinstance(payload, dict):
        return payload

    # If payload already matches our expected shape, return as-is
    if "achievements" in payload and "user_id" in payload:
        return payload

    user_id = payload.get("user_id")

    achievements = []
    recent = payload.get("recent_achievements") or []
    for ua in recent:
        try:
            ach = ua.get("achievement") if isinstance(ua, dict) else None
            achievement_id = ua.get("achievement_id") if isinstance(ua, dict) else None
            title = None
            description = None
            if isinstance(ach, dict):
                title = ach.get("name") or ach.get("title")
                description = ach.get("description")
            # fallback to top-level fields
            if not title:
                title = ua.get("title") or ua.get("name")

            achievements.append({
                "achievement_id": achievement_id or ua.get("achievement_id"),
                "title": title,
                "description": description,
                "unlocked_at": ua.get("unlocked_at"),
            })
        except Exception:
            # be tolerant: skip malformed entries
            continue

    return {"user_id": user_id, "achievements": achievements}


@router.get("/users/{user_id}/collection", response_model=UserCollectionResponse)
async def get_user_collection(user_id: int):
    # ensure user exists in users service
    await validate_user_exists(user_id)
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/collection")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    # unwrap possible wrapper { success, message, data }
    if isinstance(body, dict) and "data" in body:
        body = body.get("data")

    # Return the upstream shape (service-mirroring). FastAPI will validate
    # against UserCollectionResponse so we don't need to remodel here.
    return body


@router.get("/users/{user_id}/achievements", response_model=List[UserAchievementResponse])
async def get_user_achievements(user_id: int):
    await validate_user_exists(user_id)
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/achievements")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        body = body.get("data")

    return body


@router.get("/me/collection", response_model=UserCollectionResponse)
async def get_my_collection(current: dict = Depends(get_current_user)):
    """Return the achievements collection for the currently authenticated user."""
    user_id = current.get("user_id") or current.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unable to determine current user")

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/collection")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        body = body.get("data")

    # Return the full collection payload as provided by the achievements service
    return body


@router.get("/me/achievements", response_model=List[UserAchievementResponse])
async def get_my_achievements(current: dict = Depends(get_current_user)):
    """Return the available achievements for the currently authenticated user."""
    user_id = current.get("user_id") or current.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unable to determine current user")

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/achievements")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        body = body.get("data")

    return body


@router.get("/me/stats", response_model=UserStatsResponse)
async def get_my_stats(current: dict = Depends(get_current_user)):
    """Return the available stats for the currently authenticated user."""
    user_id = current.get("user_id") or current.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unable to determine current user")

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/stats")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        body = body.get("data")
    return body

@router.get("/me/progress", response_model=List[AchievementProgressResponse])
async def get_my_progress(current: dict = Depends(get_current_user)):
    """Return the available progress for the currently authenticated user."""
    user_id = current.get("user_id") or current.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unable to determine current user")

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/progress")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        body = body.get("data")
    return body

@router.get("/species/leaderboard", response_model=SpeciesListResponse)
async def get_species_leaderboard():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/leaderboard/species/all")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    # service returns { "species": [...] } — return as-is for service-mirroring
    if isinstance(body, dict) and "species" in body:
        return body
    if isinstance(body, list):
        return {"species": body}
    return {"species": []}


@router.get("/xp/leaderboard", response_model=List[LeaderboardEntryResponse])
async def get_xp_leaderboard():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ACHIEVEMENTS_URL}/leaderboard/xp")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    body = resp.json()
    if isinstance(body, dict) and "data" in body:
        body = body.get("data")
    return body
