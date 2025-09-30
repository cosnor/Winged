from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ....application.services.achievement_application_service import AchievementApplicationService
from ..schemas.requests import CreateAchievementRequest
from ..schemas.responses import AchievementResponse
from ...dependencies import get_achievement_service

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/", response_model=List[AchievementResponse])
def get_all_achievements(
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get all available achievements"""
    achievements = service.get_all_achievements()
    return [_entity_to_response(achievement) for achievement in achievements]


@router.get("/{achievement_id}", response_model=AchievementResponse)
def get_achievement(
    achievement_id: int,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Get specific achievement details"""
    achievement = service.get_achievement(achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return _entity_to_response(achievement)


@router.post("/", response_model=AchievementResponse)
def create_achievement(
    request: CreateAchievementRequest,
    service: AchievementApplicationService = Depends(get_achievement_service)
):
    """Create a new achievement (admin endpoint)"""
    achievement = service.create_achievement(
        name=request.name,
        description=request.description,
        category=request.category,
        criteria_data=request.criteria or {},
        xp_reward=request.xp_reward,
        icon=request.icon
    )
    return _entity_to_response(achievement)


def _entity_to_response(achievement) -> AchievementResponse:
    """Convert domain entity to response schema"""
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