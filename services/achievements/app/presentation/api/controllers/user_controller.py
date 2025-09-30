from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ....application.services.achievement_application_service import AchievementApplicationService
from ..schemas.requests import SightingEventRequest
from ..schemas.responses import (
    UserCollectionResponse, UserStatsResponse, UserAchievementResponse,
    AchievementProgressResponse, LeaderboardEntryResponse, BirdCollectionResponse
)
from ....domain.value_objects.sighting_event import SightingEvent
from ....domain.value_objects.location import Location
from ...dependencies import get_achievement_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/collection", response_model=UserCollectionResponse)
def get_user_collection(
    user_id: int,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get user's bird collection with stats and recent achievements"""
    result = service.get_user_collection(user_id)
    
    return UserCollectionResponse(
        user_id=result.user_id,
        birds=[_bird_entity_to_response(bird) for bird in result.birds],
        stats=_stats_entity_to_response(result.stats),
        recent_achievements=[_user_achievement_entity_to_response(ua) for ua in result.recent_achievements]
    )


@router.get("/{user_id}/stats", response_model=UserStatsResponse)
def get_user_stats(
    user_id: int,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get user statistics"""
    stats = service.get_user_stats(user_id)
    if not stats:
        raise HTTPException(status_code=404, detail="User stats not found")
    return _stats_entity_to_response(stats)


@router.get("/{user_id}/achievements", response_model=List[UserAchievementResponse])
def get_user_achievements(
    user_id: int,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get user's unlocked achievements"""
    achievements = service.get_user_achievements(user_id)
    return [_user_achievement_entity_to_response(ua) for ua in achievements]


@router.get("/{user_id}/progress", response_model=List[AchievementProgressResponse])
def get_achievement_progress(
    user_id: int,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get user's progress on all achievements"""
    result = service.get_achievement_progress(user_id)
    
    return [
        AchievementProgressResponse(
            achievement=_achievement_entity_to_response(item.achievement),
            progress=item.progress,
            is_unlocked=item.is_unlocked,
            unlocked_at=item.unlocked_at
        )
        for item in result.progress_items
    ]


@router.post("/{user_id}/sightings")
async def process_sighting(
    user_id: int,
    request: SightingEventRequest,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Process a new bird sighting"""
    # Validate user_id matches request
    if user_id != request.user_id:
        raise HTTPException(status_code=400, detail="User ID mismatch")
    
    # Create sighting event
    location = Location(latitude=request.location_lat, longitude=request.location_lon)
    sighting_event = SightingEvent(
        user_id=request.user_id,
        species_name=request.species_name,
        common_name=request.common_name,
        confidence_score=request.confidence_score,
        location=location,
        timestamp=request.timestamp
    )
    
    # Process the sighting
    result = await service.process_sighting(sighting_event)
    
    return {
        "message": "Sighting processed successfully",
        "newly_unlocked_achievements": [
            _user_achievement_entity_to_response(ua) 
            for ua in result.newly_unlocked_achievements
        ]
    }


def _bird_entity_to_response(bird) -> BirdCollectionResponse:
    """Convert bird collection entity to response schema"""
    return BirdCollectionResponse(
        id=bird.id,
        user_id=bird.user_id,
        species_name=bird.species_name,
        common_name=bird.common_name,
        first_sighted_at=bird.first_sighted_at,
        sighting_count=bird.sighting_count,
        last_sighted_at=bird.last_sighted_at,
        confidence_score=bird.confidence_score,
        location_lat=bird.location.latitude if bird.location else None,
        location_lon=bird.location.longitude if bird.location else None
    )


def _stats_entity_to_response(stats) -> UserStatsResponse:
    """Convert user stats entity to response schema"""
    return UserStatsResponse(
        id=stats.id,
        user_id=stats.user_id,
        total_sightings=stats.total_sightings,
        unique_species=stats.unique_species,
        total_xp=stats.total_xp,
        current_level=stats.current_level,
        achievements_unlocked=stats.achievements_unlocked,
        first_sighting_date=stats.first_sighting_date,
        last_sighting_date=stats.last_sighting_date,
        longest_streak=stats.longest_streak,
        current_streak=stats.current_streak,
        updated_at=stats.updated_at
    )


def _user_achievement_entity_to_response(ua) -> UserAchievementResponse:
    """Convert user achievement entity to response schema"""
    from ..schemas.responses import AchievementResponse
    
    achievement_response = None
    if ua.achievement:
        achievement_response = AchievementResponse(
            id=ua.achievement.id,
            name=ua.achievement.name,
            description=ua.achievement.description,
            category=ua.achievement.category,
            criteria=ua.achievement.criteria.to_json(),
            xp_reward=ua.achievement.xp_reward,
            icon=ua.achievement.icon,
            is_active=ua.achievement.is_active,
            created_at=ua.achievement.created_at
        )
    
    return UserAchievementResponse(
        id=ua.id,
        user_id=ua.user_id,
        achievement_id=ua.achievement_id,
        unlocked_at=ua.unlocked_at,
        progress=ua.progress,
        achievement=achievement_response
    )


def _achievement_entity_to_response(achievement):
    """Convert achievement entity to response schema"""
    from ..schemas.responses import AchievementResponse
    
    return AchievementResponse(
        id=achievement.id,
        name=achievement.name,
        description=achievement.description,
        category=achievement.category,
        criteria=achievement.criteria.to_json(),
        xp_reward=achievement.xp_reward,
        icon=achievement.icon,
        is_active=achievement.is_active,
        created_at=achievement.created_at
    )