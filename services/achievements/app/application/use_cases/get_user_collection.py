from dataclasses import dataclass
from typing import List
from ..interfaces.repositories import BirdCollectionRepository, UserStatsRepository, UserAchievementRepository
from ...domain.entities.bird_collection import BirdCollection
from ...domain.entities.user_stats import UserStats
from ...domain.entities.user_achievement import UserAchievement


@dataclass
class GetUserCollectionRequest:
    user_id: int


@dataclass
class GetUserCollectionResponse:
    user_id: int
    birds: List[BirdCollection]
    stats: UserStats
    recent_achievements: List[UserAchievement]


class GetUserCollectionUseCase:
    """Use case for getting user's bird collection with stats and recent achievements"""
    
    def __init__(self,
                 bird_collection_repo: BirdCollectionRepository,
                 user_stats_repo: UserStatsRepository,
                 user_achievement_repo: UserAchievementRepository):
        self.bird_collection_repo = bird_collection_repo
        self.user_stats_repo = user_stats_repo
        self.user_achievement_repo = user_achievement_repo
    
    def execute(self, request: GetUserCollectionRequest) -> GetUserCollectionResponse:
        """Execute the use case"""
        # Get user's bird collection
        birds = self.bird_collection_repo.get_by_user_id(request.user_id)
        
        # Get user stats (create if doesn't exist)
        stats = self.user_stats_repo.get_by_user_id(request.user_id)
        if not stats:
            stats = UserStats(
                id=None,
                user_id=request.user_id
            )
            stats = self.user_stats_repo.create(stats)
        
        # Get recent achievements (last 5)
        all_achievements = self.user_achievement_repo.get_by_user_id(request.user_id)
        recent_achievements = sorted(all_achievements, key=lambda x: x.unlocked_at, reverse=True)[:5]
        
        return GetUserCollectionResponse(
            user_id=request.user_id,
            birds=birds,
            stats=stats,
            recent_achievements=recent_achievements
        )