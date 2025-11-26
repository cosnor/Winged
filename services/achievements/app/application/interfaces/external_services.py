from abc import ABC, abstractmethod
from typing import List
from ...domain.entities.user_achievement import UserAchievement


class NotificationService(ABC):
    """Interface for external notification service"""
    
    @abstractmethod
    async def notify_achievement_unlocked(self, user_id: int, achievement: UserAchievement) -> None:
        """Send notification when user unlocks an achievement"""
        pass
    
    @abstractmethod
    async def notify_level_up(self, user_id: int, new_level: int) -> None:
        """Send notification when user levels up"""
        pass


class EventPublisher(ABC):
    """Interface for publishing domain events"""
    
    @abstractmethod
    async def publish_achievements_unlocked(self, user_id: int, achievements: List[UserAchievement]) -> None:
        """Publish event when achievements are unlocked"""
        pass
    
    @abstractmethod
    async def publish_stats_updated(self, user_id: int, stats: dict) -> None:
        """Publish event when user stats are updated"""
        pass