from typing import List, Optional
from ...domain.entities.achievement import Achievement, UserAchievement, UserProgress, AchievementType, AchievementTier
from ...domain.repositories.achievement_repository import AchievementRepository, UserAchievementRepository, UserProgressRepository
from ...domain.services.gamification_service import GamificationService
from ..dtos.achievement_dto import (
    AchievementDTO, UserAchievementDTO, UserProgressDTO, LeaderboardEntryDTO,
    UserStatisticsDTO, AchievementProgressDTO
)


class AchievementUseCases:
    """Application use cases for achievement and gamification management."""
    
    def __init__(
        self,
        achievement_repo: AchievementRepository,
        user_achievement_repo: UserAchievementRepository,
        user_progress_repo: UserProgressRepository,
        gamification_service: GamificationService
    ):
        self.achievement_repo = achievement_repo
        self.user_achievement_repo = user_achievement_repo
        self.user_progress_repo = user_progress_repo
        self.gamification_service = gamification_service
    
    async def get_user_achievements(self, user_id: str) -> List[UserAchievementDTO]:
        """Get all achievements unlocked by a user."""
        user_achievements = await self.user_achievement_repo.get_user_achievements(user_id)
        
        result = []
        for user_achievement in user_achievements:
            achievement = await self.achievement_repo.get_by_id(user_achievement.achievement_id)
            if achievement:
                achievement_dto = self._achievement_to_dto(achievement)
                user_achievement_dto = self._user_achievement_to_dto(user_achievement, achievement_dto)
                result.append(user_achievement_dto)
        
        return result
    
    async def get_available_achievements(self, user_id: str) -> List[AchievementDTO]:
        """Get all available achievements (excluding hidden ones not yet unlocked)."""
        all_achievements = await self.achievement_repo.get_all(include_hidden=False)
        user_unlocked = await self.user_achievement_repo.get_user_achievements(user_id)
        unlocked_ids = {ua.achievement_id for ua in user_unlocked}
        
        # Include all non-hidden achievements and hidden ones that are unlocked
        result = []
        for achievement in all_achievements:
            if not achievement.is_hidden or achievement.id in unlocked_ids:
                result.append(self._achievement_to_dto(achievement))
        
        return result
    
    async def get_achievement_progress(self, user_id: str) -> List[AchievementProgressDTO]:
        """Get user's progress on all achievements."""
        all_achievements = await self.achievement_repo.get_all(include_hidden=True)
        user_progress = await self.user_progress_repo.get_by_user_id(user_id)
        
        if not user_progress:
            # Return empty progress for new users
            return []
        
        result = []
        for achievement in all_achievements:
            # Skip if user already completed this achievement
            user_achievement = await self.user_achievement_repo.get_user_achievement_progress(
                user_id, achievement.id
            )
            
            if user_achievement and user_achievement.is_completed:
                continue
            
            # Calculate current progress
            current_progress = await self._calculate_current_progress(achievement, user_progress, user_id)
            completion_percentage = min((current_progress / achievement.requirement_value) * 100, 100)
            
            # Generate estimated completion message
            estimated_completion = self._generate_completion_estimate(
                achievement, current_progress, achievement.requirement_value
            )
            
            progress_dto = AchievementProgressDTO(
                achievement=self._achievement_to_dto(achievement),
                current_progress=current_progress,
                required_progress=achievement.requirement_value,
                completion_percentage=completion_percentage,
                is_completed=False,
                estimated_completion=estimated_completion
            )
            
            result.append(progress_dto)
        
        return result
    
    async def get_user_statistics(self, user_id: str) -> UserStatisticsDTO:
        """Get comprehensive user statistics."""
        user_progress = await self.user_progress_repo.get_by_user_id(user_id)
        if not user_progress:
            # Return empty statistics for new users
            return UserStatisticsDTO(
                user_progress=UserProgressDTO(
                    id=None, user_id=user_id, total_species_discovered=0,
                    total_points=0, current_streak_days=0, longest_streak_days=0,
                    last_discovery_date=None, achievements_unlocked=0,
                    rare_species_count=0, collections_completed=0,
                    total_identifications=0, high_confidence_identifications=0,
                    accuracy_rate=0.0, average_points_per_species=0.0
                ),
                recent_achievements=[],
                recent_discoveries=[],
                collection_progress=[]
            )
        
        # Get user rank
        user_rank = await self.user_progress_repo.get_user_rank(user_id)
        
        # Get recent achievements (last 5)
        user_achievements = await self.user_achievement_repo.get_user_completed_achievements(user_id)
        recent_achievements = sorted(user_achievements, key=lambda x: x.completion_date or x.unlocked_at, reverse=True)[:5]
        
        recent_achievement_dtos = []
        for user_achievement in recent_achievements:
            achievement = await self.achievement_repo.get_by_id(user_achievement.achievement_id)
            if achievement:
                achievement_dto = self._achievement_to_dto(achievement)
                user_achievement_dto = self._user_achievement_to_dto(user_achievement, achievement_dto)
                recent_achievement_dtos.append(user_achievement_dto)
        
        # Create user progress DTO
        user_progress_dto = UserProgressDTO(
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
        
        # Create leaderboard position
        leaderboard_position = None
        if user_rank:
            leaderboard_position = LeaderboardEntryDTO(
                user_id=user_id,
                rank=user_rank,
                total_points=user_progress.total_points,
                total_species_discovered=user_progress.total_species_discovered,
                achievements_unlocked=user_progress.achievements_unlocked,
                current_streak_days=user_progress.current_streak_days
            )
        
        return UserStatisticsDTO(
            user_progress=user_progress_dto,
            recent_achievements=recent_achievement_dtos,
            recent_discoveries=[],  # This would be populated by species use cases
            collection_progress=[],  # This would be populated by species use cases
            leaderboard_position=leaderboard_position
        )
    
    async def get_leaderboard(self, limit: int = 10, metric: str = "total_points") -> List[LeaderboardEntryDTO]:
        """Get leaderboard based on specified metric."""
        leaderboard = await self.user_progress_repo.get_leaderboard(limit, metric)
        
        result = []
        for rank, user_progress in enumerate(leaderboard, 1):
            entry = LeaderboardEntryDTO(
                user_id=user_progress.user_id,
                rank=rank,
                total_points=user_progress.total_points,
                total_species_discovered=user_progress.total_species_discovered,
                achievements_unlocked=user_progress.achievements_unlocked,
                current_streak_days=user_progress.current_streak_days
            )
            result.append(entry)
        
        return result
    
    async def _calculate_current_progress(
        self, 
        achievement: Achievement, 
        user_progress: UserProgress, 
        user_id: str
    ) -> int:
        """Calculate user's current progress towards an achievement."""
        
        if achievement.achievement_type == AchievementType.DISCOVERY:
            return user_progress.total_species_discovered
        
        elif achievement.achievement_type == AchievementType.STREAK:
            return user_progress.current_streak_days
        
        elif achievement.achievement_type == AchievementType.RARITY:
            return user_progress.rare_species_count
        
        elif achievement.achievement_type == AchievementType.COLLECTION:
            return user_progress.collections_completed
        
        elif achievement.achievement_type == AchievementType.EXPERTISE:
            return user_progress.high_confidence_identifications
        
        elif achievement.achievement_type == AchievementType.LOCATION:
            # This would require counting unique locations
            return await self.gamification_service._count_unique_locations(user_id)
        
        return 0
    
    def _generate_completion_estimate(
        self, 
        achievement: Achievement, 
        current_progress: int, 
        required_progress: int
    ) -> str:
        """Generate a human-readable completion estimate."""
        remaining = required_progress - current_progress
        
        if remaining <= 0:
            return "Ready to unlock!"
        
        if achievement.achievement_type == AchievementType.DISCOVERY:
            return f"{remaining} more species needed"
        elif achievement.achievement_type == AchievementType.STREAK:
            return f"{remaining} more days needed"
        elif achievement.achievement_type == AchievementType.RARITY:
            return f"{remaining} more rare species needed"
        elif achievement.achievement_type == AchievementType.COLLECTION:
            return f"{remaining} more collections needed"
        elif achievement.achievement_type == AchievementType.EXPERTISE:
            return f"{remaining} more high-confidence identifications needed"
        elif achievement.achievement_type == AchievementType.LOCATION:
            return f"{remaining} more unique locations needed"
        
        return f"{remaining} more needed"
    
    def _achievement_to_dto(self, achievement: Achievement) -> AchievementDTO:
        """Convert Achievement entity to DTO."""
        return AchievementDTO(
            id=achievement.id,
            name=achievement.name,
            description=achievement.description,
            achievement_type=achievement.achievement_type.value,
            tier=achievement.tier.value,
            icon=achievement.icon,
            points=achievement.points,
            total_points=achievement.total_points,
            requirement_value=achievement.requirement_value,
            requirement_description=achievement.requirement_description,
            is_hidden=achievement.is_hidden,
            is_repeatable=achievement.is_repeatable,
            created_at=achievement.created_at
        )
    
    def _user_achievement_to_dto(
        self, 
        user_achievement: UserAchievement, 
        achievement_dto: AchievementDTO
    ) -> UserAchievementDTO:
        """Convert UserAchievement entity to DTO."""
        return UserAchievementDTO(
            id=user_achievement.id,
            user_id=user_achievement.user_id,
            achievement=achievement_dto,
            unlocked_at=user_achievement.unlocked_at,
            progress_value=user_achievement.progress_value,
            is_completed=user_achievement.is_completed,
            completion_date=user_achievement.completion_date,
            created_at=user_achievement.created_at
        )