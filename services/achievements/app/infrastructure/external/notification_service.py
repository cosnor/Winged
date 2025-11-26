import logging
from typing import List
from ...application.interfaces.external_services import NotificationService, EventPublisher
from ...domain.entities.user_achievement import UserAchievement

logger = logging.getLogger(__name__)


class LoggingNotificationService(NotificationService):
    """Simple logging implementation of notification service"""
    
    async def notify_achievement_unlocked(self, user_id: int, achievement: UserAchievement) -> None:
        """Send notification when user unlocks an achievement"""
        logger.info(
            f"Achievement unlocked for user {user_id}: "
            f"{achievement.achievement.name if achievement.achievement else 'Unknown'}"
        )
    
    async def notify_level_up(self, user_id: int, new_level: int) -> None:
        """Send notification when user levels up"""
        logger.info(f"User {user_id} leveled up to level {new_level}")


class LoggingEventPublisher(EventPublisher):
    """Simple logging implementation of event publisher"""
    
    async def publish_achievements_unlocked(self, user_id: int, achievements: List[UserAchievement]) -> None:
        """Publish event when achievements are unlocked"""
        achievement_names = [
            a.achievement.name if a.achievement else 'Unknown' 
            for a in achievements
        ]
        logger.info(
            f"Published achievements unlocked event for user {user_id}: "
            f"{', '.join(achievement_names)}"
        )
    
    async def publish_stats_updated(self, user_id: int, stats: dict) -> None:
        """Publish event when user stats are updated"""
        logger.info(f"Published stats updated event for user {user_id}: {stats}")


# TODO: Implement actual notification service integrations
# class WebSocketNotificationService(NotificationService):
#     """WebSocket implementation for real-time notifications"""
#     pass

# class EmailNotificationService(NotificationService):
#     """Email implementation for notifications"""
#     pass

# class PushNotificationService(NotificationService):
#     """Push notification implementation"""
#     pass