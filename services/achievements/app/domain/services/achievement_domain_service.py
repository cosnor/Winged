from typing import List
from ..entities.achievement import Achievement
from ..entities.user_achievement import UserAchievement
from ..entities.user_stats import UserStats
from ..entities.bird_collection import BirdCollection
from ..value_objects.sighting_event import SightingEvent


class AchievementDomainService:
    """Domain service for achievement-related business logic"""
    
    def check_achievements_for_user(self, 
                                  user_stats: UserStats,
                                  user_collection: List[BirdCollection],
                                  available_achievements: List[Achievement],
                                  current_achievements: List[UserAchievement]) -> List[Achievement]:
        """Check which achievements should be unlocked for a user"""
        newly_unlocked = []
        current_achievement_ids = {ua.achievement_id for ua in current_achievements}
        
        for achievement in available_achievements:
            if achievement.id in current_achievement_ids:
                continue
                
            if achievement.is_criteria_met(user_stats, user_collection):
                newly_unlocked.append(achievement)
        
        return newly_unlocked
    
    def calculate_achievement_progress(self,
                                     user_stats: UserStats,
                                     user_collection: List[BirdCollection],
                                     achievement: Achievement) -> float:
        """Calculate progress towards a specific achievement"""
        return achievement.calculate_progress(user_stats, user_collection)
    
    def process_sighting_for_collection(self,
                                      sighting: SightingEvent,
                                      existing_collection: List[BirdCollection]) -> tuple[BirdCollection, bool]:
        """Process a sighting event and update bird collection"""
        # Find existing entry for this species
        existing_bird = None
        for bird in existing_collection:
            if bird.species_name == sighting.species_name and bird.user_id == sighting.user_id:
                existing_bird = bird
                break
        
        is_new_species = existing_bird is None
        
        if existing_bird:
            # Update existing entry
            existing_bird.add_sighting(sighting.confidence_score, sighting.location)
            return existing_bird, is_new_species
        else:
            # Create new entry
            new_bird = BirdCollection(
                id=None,
                user_id=sighting.user_id,
                species_name=sighting.species_name,
                common_name=sighting.common_name,
                first_sighted_at=sighting.timestamp,
                sighting_count=1,
                last_sighted_at=sighting.timestamp,
                confidence_score=sighting.confidence_score,
                location=sighting.location
            )
            return new_bird, is_new_species
    
    def create_user_achievement(self, user_id: int, achievement: Achievement) -> UserAchievement:
        """Create a new user achievement"""
        return UserAchievement(
            id=None,
            user_id=user_id,
            achievement_id=achievement.id,
            unlocked_at=None,  # Will be set in __post_init__
            progress=1.0,
            achievement=achievement
        )