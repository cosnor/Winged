from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ...infrastructure.database.connection import get_database_session
from ...infrastructure.database.achievement_repository_impl import (
    SQLAlchemyAchievementRepository, SQLAlchemyUserAchievementRepository, SQLAlchemyUserProgressRepository
)
from ...infrastructure.database.species_repository_impl import SQLAlchemyUserSpeciesRepository
from ...domain.services.gamification_service import GamificationService
from ...application.use_cases.achievement_use_cases import AchievementUseCases
from ..schemas.achievement_schemas import (
    AchievementResponse, UserAchievementResponse, UserProgressResponse, 
    LeaderboardEntryResponse, UserStatisticsResponse, AchievementProgressResponse,
    AchievementTypeSchema, AchievementTierSchema
)

router = APIRouter(prefix="/achievements", tags=["Achievements"])


async def get_achievement_use_cases(session: AsyncSession = Depends(get_database_session)) -> AchievementUseCases:
    """Dependency to get AchievementUseCases with all dependencies."""
    achievement_repo = SQLAlchemyAchievementRepository(session)
    user_achievement_repo = SQLAlchemyUserAchievementRepository(session)
    user_progress_repo = SQLAlchemyUserProgressRepository(session)
    user_species_repo = SQLAlchemyUserSpeciesRepository(session)
    
    gamification_service = GamificationService(
        achievement_repo, user_achievement_repo, user_progress_repo, user_species_repo
    )
    
    return AchievementUseCases(
        achievement_repo, user_achievement_repo, user_progress_repo, gamification_service
    )


@router.get("/", response_model=List[AchievementResponse])
async def get_available_achievements(
    user_id: Optional[str] = Query(None, min_length=1, max_length=255),
    achievement_type: Optional[AchievementTypeSchema] = Query(None),
    tier: Optional[AchievementTierSchema] = Query(None),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get all available achievements (excluding hidden ones not yet unlocked)."""
    try:
        if user_id:
            achievement_dtos = await use_cases.get_available_achievements(user_id)
        else:
            # Get all non-hidden achievements
            all_achievements = await use_cases.achievement_repo.get_all(include_hidden=False)
            achievement_dtos = [use_cases._achievement_to_dto(a) for a in all_achievements]
        
        # Apply filters
        if achievement_type:
            achievement_dtos = [a for a in achievement_dtos if a.achievement_type == achievement_type.value]
        
        if tier:
            achievement_dtos = [a for a in achievement_dtos if a.tier == tier.value]
        
        return [AchievementResponse(**dto.__dict__) for dto in achievement_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving achievements: {str(e)}")


@router.get("/{achievement_id}", response_model=AchievementResponse)
async def get_achievement_details(
    achievement_id: int = Path(gt=0),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get detailed information about a specific achievement."""
    try:
        achievement = await use_cases.achievement_repo.get_by_id(achievement_id)
        if not achievement:
            raise HTTPException(status_code=404, detail="Achievement not found")
        
        achievement_dto = use_cases._achievement_to_dto(achievement)
        return AchievementResponse(**achievement_dto.__dict__)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving achievement: {str(e)}")


@router.get("/users/{user_id}", response_model=List[UserAchievementResponse])
async def get_user_achievements(
    user_id: str = Path(min_length=1, max_length=255),
    completed_only: bool = Query(False),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get all achievements unlocked by a user."""
    try:
        if completed_only:
            user_achievement_dtos = await use_cases.user_achievement_repo.get_user_completed_achievements(user_id)
            user_achievement_dtos = [use_cases._user_achievement_to_dto(ua, use_cases._achievement_to_dto(await use_cases.achievement_repo.get_by_id(ua.achievement_id))) for ua in user_achievement_dtos]
        else:
            user_achievement_dtos = await use_cases.get_user_achievements(user_id)
        
        return [UserAchievementResponse(**dto.__dict__) for dto in user_achievement_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user achievements: {str(e)}")


@router.get("/users/{user_id}/progress", response_model=List[AchievementProgressResponse])
async def get_user_achievement_progress(
    user_id: str = Path(min_length=1, max_length=255),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get user's progress on all achievements."""
    try:
        progress_dtos = await use_cases.get_achievement_progress(user_id)
        return [AchievementProgressResponse(**dto.__dict__) for dto in progress_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving achievement progress: {str(e)}")


# Temporarily commented out due to circular import issues
# @router.get("/users/{user_id}/statistics", response_model=UserStatisticsResponse)
async def get_user_statistics(
    user_id: str = Path(min_length=1, max_length=255),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get comprehensive user statistics."""
    try:
        statistics_dto = await use_cases.get_user_statistics(user_id)
        return UserStatisticsResponse(**statistics_dto.__dict__)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user statistics: {str(e)}")


@router.get("/users/{user_id}/progress-summary", response_model=UserProgressResponse)
async def get_user_progress_summary(
    user_id: str = Path(min_length=1, max_length=255),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get user's overall progress summary."""
    try:
        user_progress = await use_cases.user_progress_repo.get_by_user_id(user_id)
        if not user_progress:
            raise HTTPException(status_code=404, detail="User progress not found")
        
        # Get user rank
        user_rank = await use_cases.user_progress_repo.get_user_rank(user_id)
        
        # Create DTO with rank
        progress_dto = UserProgressResponse(
            id=user_progress.id,
            user_id=user_progress.user_id,
            total_species_discovered=user_progress.total_species_discovered,
            total_points=user_progress.total_points,
            current_streak_days=user_progress.current_streak_days,
            longest_streak_days=user_progress.longest_streak_days,
            last_discovery_date=user_progress.last_discovery_date,
            achievements_unlocked=user_progress.achievements_unlocked,
            rare_species_count=user_progress.rare_species_count,
            collections_completed=user_progress.collections_completed,
            total_identifications=user_progress.total_identifications,
            high_confidence_identifications=user_progress.high_confidence_identifications,
            accuracy_rate=user_progress.accuracy_rate,
            average_points_per_species=user_progress.average_points_per_species,
            rank=user_rank,
            created_at=user_progress.created_at,
            updated_at=user_progress.updated_at
        )
        
        return progress_dto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user progress: {str(e)}")


@router.get("/leaderboard/", response_model=List[LeaderboardEntryResponse])
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    metric: str = Query("total_points", regex="^(total_points|total_species_discovered|achievements_unlocked|current_streak_days|longest_streak_days|rare_species_count)$"),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get leaderboard based on specified metric."""
    try:
        leaderboard_dtos = await use_cases.get_leaderboard(limit, metric)
        return [LeaderboardEntryResponse(**dto.__dict__) for dto in leaderboard_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving leaderboard: {str(e)}")


@router.get("/types/{achievement_type}", response_model=List[AchievementResponse])
async def get_achievements_by_type(
    achievement_type: AchievementTypeSchema = Path(),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get achievements filtered by type."""
    try:
        from ...domain.entities.achievement import AchievementType
        type_enum = AchievementType(achievement_type.value)
        achievements = await use_cases.achievement_repo.get_by_type(type_enum)
        achievement_dtos = [use_cases._achievement_to_dto(a) for a in achievements]
        return [AchievementResponse(**dto.__dict__) for dto in achievement_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving achievements by type: {str(e)}")


@router.get("/tiers/{tier}", response_model=List[AchievementResponse])
async def get_achievements_by_tier(
    tier: AchievementTierSchema = Path(),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get achievements filtered by tier."""
    try:
        from ...domain.entities.achievement import AchievementTier
        tier_enum = AchievementTier(tier.value)
        achievements = await use_cases.achievement_repo.get_by_tier(tier_enum)
        achievement_dtos = [use_cases._achievement_to_dto(a) for a in achievements]
        return [AchievementResponse(**dto.__dict__) for dto in achievement_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving achievements by tier: {str(e)}")


@router.get("/users/{user_id}/rank", response_model=dict)
async def get_user_rank(
    user_id: str = Path(min_length=1, max_length=255),
    metric: str = Query("total_points", regex="^(total_points|total_species_discovered|achievements_unlocked|current_streak_days|longest_streak_days|rare_species_count)$"),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get user's rank in leaderboard for specified metric."""
    try:
        rank = await use_cases.user_progress_repo.get_user_rank(user_id, metric)
        if rank is None:
            raise HTTPException(status_code=404, detail="User progress not found")
        
        return {
            "user_id": user_id,
            "metric": metric,
            "rank": rank
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user rank: {str(e)}")


@router.get("/streaks/active", response_model=List[LeaderboardEntryResponse])
async def get_active_streaks(
    min_days: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    use_cases: AchievementUseCases = Depends(get_achievement_use_cases)
):
    """Get users with active streaks above minimum days."""
    try:
        users_with_streaks = await use_cases.user_progress_repo.get_users_by_streak(min_days)
        
        # Convert to leaderboard entries
        result = []
        for rank, user_progress in enumerate(users_with_streaks[:limit], 1):
            entry = LeaderboardEntryResponse(
                user_id=user_progress.user_id,
                rank=rank,
                total_points=user_progress.total_points,
                total_species_discovered=user_progress.total_species_discovered,
                achievements_unlocked=user_progress.achievements_unlocked,
                current_streak_days=user_progress.current_streak_days
            )
            result.append(entry)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving active streaks: {str(e)}")