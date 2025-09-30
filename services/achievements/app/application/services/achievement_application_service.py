from typing import List, Optional
from ..interfaces.repositories import (
    AchievementRepository,
    UserAchievementRepository,
    BirdCollectionRepository,
    UserStatsRepository
)
from ..interfaces.external_services import NotificationService, EventPublisher
from ..use_cases.get_user_collection import GetUserCollectionUseCase, GetUserCollectionRequest
from ..use_cases.process_sighting import ProcessSightingUseCase, ProcessSightingRequest
from ..use_cases.get_achievement_progress import GetAchievementProgressUseCase, GetAchievementProgressRequest
from ..use_cases.manage_achievements import ManageAchievementsUseCase, CreateAchievementRequest, GetAchievementRequest, GetAllAchievementsRequest
from ...domain.services.achievement_domain_service import AchievementDomainService
from ...domain.entities.achievement import Achievement
from ...domain.entities.user_achievement import UserAchievement
from ...domain.entities.user_stats import UserStats
from ...domain.value_objects.sighting_event import SightingEvent


class AchievementApplicationService:
    """Application service that orchestrates use cases"""
    
    def __init__(self,
                 achievement_repo: AchievementRepository,
                 user_achievement_repo: UserAchievementRepository,
                 bird_collection_repo: BirdCollectionRepository,
                 user_stats_repo: UserStatsRepository,
                 achievement_domain_service: AchievementDomainService,
                 notification_service: Optional[NotificationService] = None,
                 event_publisher: Optional[EventPublisher] = None):
        self.achievement_repo = achievement_repo
        self.user_achievement_repo = user_achievement_repo
        self.bird_collection_repo = bird_collection_repo
        self.user_stats_repo = user_stats_repo
        self.achievement_domain_service = achievement_domain_service
        self.notification_service = notification_service
        self.event_publisher = event_publisher
        
        # Initialize use cases
        self._get_user_collection_use_case = GetUserCollectionUseCase(
            bird_collection_repo, user_stats_repo, user_achievement_repo
        )
        
        self._process_sighting_use_case = ProcessSightingUseCase(
            bird_collection_repo, user_stats_repo, user_achievement_repo,
            achievement_repo, achievement_domain_service, notification_service, event_publisher
        )
        
        self._get_achievement_progress_use_case = GetAchievementProgressUseCase(
            achievement_repo, user_achievement_repo, bird_collection_repo,
            user_stats_repo, achievement_domain_service
        )
        
        self._manage_achievements_use_case = ManageAchievementsUseCase(achievement_repo)
    
    def get_user_collection(self, user_id: int):
        """Get user's bird collection with stats and recent achievements"""
        request = GetUserCollectionRequest(user_id=user_id)
        return self._get_user_collection_use_case.execute(request)
    
    def get_user_stats(self, user_id: int) -> Optional[UserStats]:
        """Get user statistics"""
        return self.user_stats_repo.get_by_user_id(user_id)
    
    def get_user_achievements(self, user_id: int) -> List[UserAchievement]:
        """Get user's unlocked achievements"""
        return self.user_achievement_repo.get_by_user_id(user_id)
    
    def get_achievement_progress(self, user_id: int):
        """Get user's progress on all achievements"""
        request = GetAchievementProgressRequest(user_id=user_id)
        return self._get_achievement_progress_use_case.execute(request)
    
    async def process_sighting(self, sighting_event: SightingEvent):
        """Process a new sighting and return any newly unlocked achievements"""
        request = ProcessSightingRequest(sighting_event=sighting_event)
        return await self._process_sighting_use_case.execute(request)
    
    def get_all_achievements(self) -> List[Achievement]:
        """Get all available achievements"""
        request = GetAllAchievementsRequest()
        return self._manage_achievements_use_case.get_all_achievements(request)
    
    def get_achievement(self, achievement_id: int) -> Optional[Achievement]:
        """Get specific achievement details"""
        request = GetAchievementRequest(achievement_id=achievement_id)
        return self._manage_achievements_use_case.get_achievement(request)
    
    def create_achievement(self, name: str, description: str, category: str,
                          criteria_data: dict, xp_reward: int, icon: Optional[str] = None) -> Achievement:
        """Create a new achievement (admin endpoint)"""
        request = CreateAchievementRequest(
            name=name, description=description, category=category,
            criteria_data=criteria_data, xp_reward=xp_reward, icon=icon
        )
        return self._manage_achievements_use_case.create_achievement(request)
    
    def get_all_species(self) -> List[str]:
        """Get list of all bird species that have been sighted"""
        return self.bird_collection_repo.get_all_species()
    
    def get_users_with_species(self, species_name: str) -> List[int]:
        """Get list of user IDs who have sighted a specific species"""
        return self.bird_collection_repo.get_users_with_species(species_name)
    
    def get_species_leaderboard(self, limit: int = 10):
        """Get leaderboard of users by unique species count"""
        leaderboard = self.user_stats_repo.get_leaderboard_by_species(limit)
        return [
            {
                "user_id": stats.user_id,
                "unique_species": stats.unique_species,
                "total_sightings": stats.total_sightings,
                "level": stats.current_level,
                "rank": idx + 1
            }
            for idx, stats in enumerate(leaderboard)
        ]
    
    def get_xp_leaderboard(self, limit: int = 10):
        """Get leaderboard of users by total XP"""
        leaderboard = self.user_stats_repo.get_leaderboard_by_xp(limit)
        return [
            {
                "user_id": stats.user_id,
                "total_xp": stats.total_xp,
                "level": stats.current_level,
                "achievements_unlocked": stats.achievements_unlocked,
                "rank": idx + 1
            }
            for idx, stats in enumerate(leaderboard)
        ]
    
    def initialize_default_achievements(self):
        """Initialize default achievements on startup"""
        return self._manage_achievements_use_case.create_default_achievements()