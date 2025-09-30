from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from ..interfaces.repositories import (
    AchievementRepository,
    UserAchievementRepository,
    BirdCollectionRepository,
    UserStatsRepository
)
from ...domain.entities.achievement import Achievement
from ...domain.entities.user_stats import UserStats
from ...domain.services.achievement_domain_service import AchievementDomainService


@dataclass
class AchievementProgressItem:
    achievement: Achievement
    progress: float
    is_unlocked: bool
    unlocked_at: Optional[datetime] = None


@dataclass
class GetAchievementProgressRequest:
    user_id: int


@dataclass
class GetAchievementProgressResponse:
    user_id: int
    progress_items: List[AchievementProgressItem]


class GetAchievementProgressUseCase:
    """Use case for getting user's progress on all achievements"""
    
    def __init__(self,
                 achievement_repo: AchievementRepository,
                 user_achievement_repo: UserAchievementRepository,
                 bird_collection_repo: BirdCollectionRepository,
                 user_stats_repo: UserStatsRepository,
                 achievement_domain_service: AchievementDomainService):
        self.achievement_repo = achievement_repo
        self.user_achievement_repo = user_achievement_repo
        self.bird_collection_repo = bird_collection_repo
        self.user_stats_repo = user_stats_repo
        self.achievement_domain_service = achievement_domain_service
    
    def execute(self, request: GetAchievementProgressRequest) -> GetAchievementProgressResponse:
        """Execute the use case"""
        # Get all active achievements
        achievements = self.achievement_repo.get_all_active()
        
        # Get user's current achievements
        user_achievements = self.user_achievement_repo.get_by_user_id(request.user_id)
        user_achievement_map = {ua.achievement_id: ua for ua in user_achievements}
        
        # Get user stats and collection for progress calculation
        user_stats = self.user_stats_repo.get_by_user_id(request.user_id)
        if not user_stats:
            from ...domain.entities.user_stats import UserStats
            user_stats = UserStats(id=None, user_id=request.user_id)
        
        user_collection = self.bird_collection_repo.get_by_user_id(request.user_id)
        
        # Calculate progress for each achievement
        progress_items = []
        for achievement in achievements:
            user_achievement = user_achievement_map.get(achievement.id)
            
            if user_achievement:
                # Achievement is unlocked
                progress_items.append(AchievementProgressItem(
                    achievement=achievement,
                    progress=1.0,
                    is_unlocked=True,
                    unlocked_at=user_achievement.unlocked_at
                ))
            else:
                # Calculate progress towards achievement
                progress = self.achievement_domain_service.calculate_achievement_progress(
                    user_stats, user_collection, achievement
                )
                progress_items.append(AchievementProgressItem(
                    achievement=achievement,
                    progress=progress,
                    is_unlocked=False
                ))
        
        return GetAchievementProgressResponse(
            user_id=request.user_id,
            progress_items=progress_items
        )