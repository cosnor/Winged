from fastapi import APIRouter, Depends, Query
from typing import List
from ....application.services.achievement_application_service import AchievementApplicationService
from ..schemas.responses import LeaderboardEntryResponse
from ...dependencies import get_achievement_service

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/species", response_model=List[LeaderboardEntryResponse])
def get_species_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get leaderboard of users by unique species count"""
    leaderboard = service.get_species_leaderboard(limit)
    
    return [
        LeaderboardEntryResponse(
            user_id=entry["user_id"],
            rank=entry["rank"],
            unique_species=entry["unique_species"],
            total_sightings=entry["total_sightings"],
            level=entry["level"]
        )
        for entry in leaderboard
    ]


@router.get("/xp", response_model=List[LeaderboardEntryResponse])
def get_xp_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get leaderboard of users by total XP"""
    leaderboard = service.get_xp_leaderboard(limit)
    
    return [
        LeaderboardEntryResponse(
            user_id=entry["user_id"],
            rank=entry["rank"],
            total_xp=entry["total_xp"],
            level=entry["level"],
            achievements_unlocked=entry["achievements_unlocked"]
        )
        for entry in leaderboard
    ]


@router.get("/species/all")
def get_all_species(
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get list of all bird species that have been sighted"""
    species = service.get_all_species()
    return {"species": species}


@router.get("/species/{species_name}/users")
def get_users_with_species(
    species_name: str,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get list of user IDs who have sighted a specific species"""
    users = service.get_users_with_species(species_name)
    return {"species_name": species_name, "user_ids": users}