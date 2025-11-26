from dataclasses import dataclass
from typing import List, Optional
from ..interfaces.repositories import (
    BirdCollectionRepository, 
    UserStatsRepository, 
    UserAchievementRepository,
    AchievementRepository
)
from ..interfaces.external_services import NotificationService, EventPublisher
from ...domain.entities.user_achievement import UserAchievement
from ...domain.value_objects.sighting_event import SightingEvent
from ...domain.services.achievement_domain_service import AchievementDomainService


@dataclass
class ProcessSightingRequest:
    sighting_event: SightingEvent


@dataclass
class ProcessSightingResponse:
    newly_unlocked_achievements: List[UserAchievement]


class ProcessSightingUseCase:
    """Use case for processing a bird sighting and checking for achievements"""
    
    def __init__(self,
                 bird_collection_repo: BirdCollectionRepository,
                 user_stats_repo: UserStatsRepository,
                 user_achievement_repo: UserAchievementRepository,
                 achievement_repo: AchievementRepository,
                 achievement_domain_service: AchievementDomainService,
                 notification_service: Optional[NotificationService] = None,
                 event_publisher: Optional[EventPublisher] = None):
        self.bird_collection_repo = bird_collection_repo
        self.user_stats_repo = user_stats_repo
        self.user_achievement_repo = user_achievement_repo
        self.achievement_repo = achievement_repo
        self.achievement_domain_service = achievement_domain_service
        self.notification_service = notification_service
        self.event_publisher = event_publisher
    
    async def execute(self, request: ProcessSightingRequest) -> ProcessSightingResponse:
        """Execute the use case"""
        sighting = request.sighting_event
        
        # Get or create user stats
        user_stats = self.user_stats_repo.get_by_user_id(sighting.user_id)
        if not user_stats:
            from ...domain.entities.user_stats import UserStats
            user_stats = UserStats(id=None, user_id=sighting.user_id)
            user_stats = self.user_stats_repo.create(user_stats)
        
        # Get user's current collection
        user_collection = self.bird_collection_repo.get_by_user_id(sighting.user_id)
        
        # Process the sighting for bird collection
        updated_bird, is_new_species = self.achievement_domain_service.process_sighting_for_collection(
            sighting, user_collection
        )
        
        # Save or update bird collection entry
        existing_bird = self.bird_collection_repo.get_by_user_and_species(
            sighting.user_id, sighting.species_name
        )
        if existing_bird:
            self.bird_collection_repo.update(updated_bird)
        else:
            self.bird_collection_repo.create(updated_bird)
            user_collection.append(updated_bird)  # Add to local collection for achievement checking
        
        # Update user stats
        old_level = user_stats.current_level
        user_stats.add_sighting(sighting.timestamp, is_new_species)
        self.user_stats_repo.update(user_stats)
        
        # Check for new achievements
        available_achievements = self.achievement_repo.get_all_active()
        current_achievements = self.user_achievement_repo.get_by_user_id(sighting.user_id)
        
        newly_unlocked_achievements_entities = self.achievement_domain_service.check_achievements_for_user(
            user_stats, user_collection, available_achievements, current_achievements
        )
        
        # Create user achievement records and add XP
        newly_unlocked = []
        for achievement in newly_unlocked_achievements_entities:
            user_achievement = self.achievement_domain_service.create_user_achievement(
                sighting.user_id, achievement
            )
            user_achievement = self.user_achievement_repo.create(user_achievement)
            newly_unlocked.append(user_achievement)
            
            # Add XP and update level
            user_stats.add_xp(achievement.xp_reward)
            user_stats.unlock_achievement()
        
        # Update stats if achievements were unlocked
        if newly_unlocked:
            self.user_stats_repo.update(user_stats)
        
        # Send notifications if service is available
        if self.notification_service:
            for achievement in newly_unlocked:
                await self.notification_service.notify_achievement_unlocked(
                    sighting.user_id, achievement
                )
            
            # Check if user leveled up
            if user_stats.current_level > old_level:
                await self.notification_service.notify_level_up(
                    sighting.user_id, user_stats.current_level
                )
        
        # Publish events if publisher is available
        if self.event_publisher:
            if newly_unlocked:
                await self.event_publisher.publish_achievements_unlocked(
                    sighting.user_id, newly_unlocked
                )
            
            await self.event_publisher.publish_stats_updated(
                sighting.user_id, {
                    'total_sightings': user_stats.total_sightings,
                    'unique_species': user_stats.unique_species,
                    'total_xp': user_stats.total_xp,
                    'current_level': user_stats.current_level
                }
            )
        
        return ProcessSightingResponse(newly_unlocked_achievements=newly_unlocked)