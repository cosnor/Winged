from typing import List, Optional
from ..entities.species import Species, UserSpecies, RarityLevel
from ..entities.achievement import Achievement, UserAchievement, UserProgress, AchievementType
from ..repositories.achievement_repository import AchievementRepository, UserAchievementRepository, UserProgressRepository
from ..repositories.species_repository import UserSpeciesRepository


class GamificationService:
    """Domain service for handling gamification logic."""
    
    def __init__(
        self,
        achievement_repo: AchievementRepository,
        user_achievement_repo: UserAchievementRepository,
        user_progress_repo: UserProgressRepository,
        user_species_repo: UserSpeciesRepository
    ):
        self.achievement_repo = achievement_repo
        self.user_achievement_repo = user_achievement_repo
        self.user_progress_repo = user_progress_repo
        self.user_species_repo = user_species_repo
    
    async def process_species_discovery(
        self, 
        user_id: str, 
        species: Species, 
        user_species: UserSpecies
    ) -> List[Achievement]:
        """Process a new species discovery and return newly unlocked achievements."""
        
        # Get or create user progress
        user_progress = await self.user_progress_repo.get_by_user_id(user_id)
        if not user_progress:
            user_progress = UserProgress(id=None, user_id=user_id)
            user_progress = await self.user_progress_repo.create(user_progress)
        
        # Update user progress
        is_high_confidence = user_species.is_high_confidence
        user_progress.add_species_discovery(species.rarity_points, is_high_confidence)
        
        # Check for rare species
        if species.rarity_level in [RarityLevel.RARE, RarityLevel.VERY_RARE, RarityLevel.LEGENDARY]:
            user_progress.increment_rare_species()
        
        await self.user_progress_repo.update(user_progress)
        
        # Check for newly unlocked achievements
        newly_unlocked = await self._check_achievements(user_id, user_progress)
        
        return newly_unlocked
    
    async def _check_achievements(self, user_id: str, user_progress: UserProgress) -> List[Achievement]:
        """Check and unlock achievements based on user progress."""
        newly_unlocked = []
        
        # Get all achievements
        all_achievements = await self.achievement_repo.get_all(include_hidden=True)
        
        for achievement in all_achievements:
            # Skip if user already has this achievement
            if await self.user_achievement_repo.has_user_unlocked_achievement(user_id, achievement.id):
                continue
            
            # Check if achievement should be unlocked
            should_unlock = await self._should_unlock_achievement(achievement, user_progress, user_id)
            
            if should_unlock:
                # Create user achievement
                user_achievement = UserAchievement(
                    id=None,
                    user_id=user_id,
                    achievement_id=achievement.id,
                    unlocked_at=user_progress.updated_at,
                    progress_value=achievement.requirement_value,
                    is_completed=True,
                    completion_date=user_progress.updated_at
                )
                
                await self.user_achievement_repo.create(user_achievement)
                
                # Update user progress with achievement points
                user_progress.add_achievement(achievement.total_points)
                await self.user_progress_repo.update(user_progress)
                
                newly_unlocked.append(achievement)
        
        return newly_unlocked
    
    async def _should_unlock_achievement(
        self, 
        achievement: Achievement, 
        user_progress: UserProgress, 
        user_id: str
    ) -> bool:
        """Determine if an achievement should be unlocked."""
        
        if achievement.achievement_type == AchievementType.DISCOVERY:
            return user_progress.total_species_discovered >= achievement.requirement_value
        
        elif achievement.achievement_type == AchievementType.STREAK:
            return user_progress.current_streak_days >= achievement.requirement_value
        
        elif achievement.achievement_type == AchievementType.RARITY:
            return user_progress.rare_species_count >= achievement.requirement_value
        
        elif achievement.achievement_type == AchievementType.COLLECTION:
            return user_progress.collections_completed >= achievement.requirement_value
        
        elif achievement.achievement_type == AchievementType.EXPERTISE:
            # High confidence identifications
            return user_progress.high_confidence_identifications >= achievement.requirement_value
        
        elif achievement.achievement_type == AchievementType.LOCATION:
            # This would require checking unique locations from user_species
            unique_locations = await self._count_unique_locations(user_id)
            return unique_locations >= achievement.requirement_value
        
        return False
    
    async def _count_unique_locations(self, user_id: str) -> int:
        """Count unique locations where user has made discoveries."""
        user_species_list = await self.user_species_repo.get_user_species(user_id)
        unique_locations = set()
        
        for user_species in user_species_list:
            if user_species.location_coordinates:
                # Round coordinates to avoid minor GPS variations
                rounded_coords = (
                    round(user_species.location_coordinates[0], 3),
                    round(user_species.location_coordinates[1], 3)
                )
                unique_locations.add(rounded_coords)
        
        return len(unique_locations)
    
    async def calculate_collection_progress(self, user_id: str, collection_id: int) -> dict:
        """Calculate user's progress on a specific collection."""
        from ..repositories.species_repository import CollectionRepository
        
        # This would need to be injected, but for now we'll return a placeholder
        # In a real implementation, we'd inject CollectionRepository
        return {
            "collection_id": collection_id,
            "total_species": 0,
            "discovered_species": 0,
            "completion_percentage": 0.0,
            "missing_species": []
        }
    
    async def get_user_statistics(self, user_id: str) -> dict:
        """Get comprehensive user statistics."""
        user_progress = await self.user_progress_repo.get_by_user_id(user_id)
        if not user_progress:
            return {}
        
        user_rank = await self.user_progress_repo.get_user_rank(user_id)
        
        return {
            "total_species": user_progress.total_species_discovered,
            "total_points": user_progress.total_points,
            "current_streak": user_progress.current_streak_days,
            "longest_streak": user_progress.longest_streak_days,
            "achievements_unlocked": user_progress.achievements_unlocked,
            "rare_species_count": user_progress.rare_species_count,
            "accuracy_rate": user_progress.accuracy_rate,
            "rank": user_rank,
            "collections_completed": user_progress.collections_completed
        }