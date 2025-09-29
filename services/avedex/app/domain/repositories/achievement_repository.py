from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.achievement import Achievement, UserAchievement, UserProgress, AchievementType, AchievementTier


class AchievementRepository(ABC):
    """Abstract repository for Achievement entity."""
    
    @abstractmethod
    async def get_by_id(self, achievement_id: int) -> Optional[Achievement]:
        """Get achievement by ID."""
        pass
    
    @abstractmethod
    async def get_all(self, include_hidden: bool = False) -> List[Achievement]:
        """Get all achievements."""
        pass
    
    @abstractmethod
    async def get_by_type(self, achievement_type: AchievementType) -> List[Achievement]:
        """Get achievements by type."""
        pass
    
    @abstractmethod
    async def get_by_tier(self, tier: AchievementTier) -> List[Achievement]:
        """Get achievements by tier."""
        pass
    
    @abstractmethod
    async def create(self, achievement: Achievement) -> Achievement:
        """Create a new achievement."""
        pass
    
    @abstractmethod
    async def update(self, achievement: Achievement) -> Achievement:
        """Update an existing achievement."""
        pass
    
    @abstractmethod
    async def delete(self, achievement_id: int) -> bool:
        """Delete an achievement."""
        pass


class UserAchievementRepository(ABC):
    """Abstract repository for UserAchievement entity."""
    
    @abstractmethod
    async def get_by_id(self, user_achievement_id: int) -> Optional[UserAchievement]:
        """Get user achievement by ID."""
        pass
    
    @abstractmethod
    async def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """Get all achievements for a user."""
        pass
    
    @abstractmethod
    async def get_user_completed_achievements(self, user_id: str) -> List[UserAchievement]:
        """Get completed achievements for a user."""
        pass
    
    @abstractmethod
    async def get_user_in_progress_achievements(self, user_id: str) -> List[UserAchievement]:
        """Get in-progress achievements for a user."""
        pass
    
    @abstractmethod
    async def has_user_unlocked_achievement(self, user_id: str, achievement_id: int) -> bool:
        """Check if user has unlocked a specific achievement."""
        pass
    
    @abstractmethod
    async def get_user_achievement_progress(
        self, 
        user_id: str, 
        achievement_id: int
    ) -> Optional[UserAchievement]:
        """Get user's progress on a specific achievement."""
        pass
    
    @abstractmethod
    async def create(self, user_achievement: UserAchievement) -> UserAchievement:
        """Create a new user achievement."""
        pass
    
    @abstractmethod
    async def update(self, user_achievement: UserAchievement) -> UserAchievement:
        """Update user achievement progress."""
        pass
    
    @abstractmethod
    async def delete(self, user_achievement_id: int) -> bool:
        """Delete a user achievement."""
        pass


class UserProgressRepository(ABC):
    """Abstract repository for UserProgress entity."""
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[UserProgress]:
        """Get user progress by user ID."""
        pass
    
    @abstractmethod
    async def get_leaderboard(self, limit: int = 10, metric: str = "total_points") -> List[UserProgress]:
        """Get leaderboard based on specified metric."""
        pass
    
    @abstractmethod
    async def get_users_by_streak(self, min_streak_days: int) -> List[UserProgress]:
        """Get users with streak above minimum."""
        pass
    
    @abstractmethod
    async def create(self, user_progress: UserProgress) -> UserProgress:
        """Create new user progress record."""
        pass
    
    @abstractmethod
    async def update(self, user_progress: UserProgress) -> UserProgress:
        """Update user progress."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete user progress."""
        pass
    
    @abstractmethod
    async def get_user_rank(self, user_id: str, metric: str = "total_points") -> Optional[int]:
        """Get user's rank in leaderboard for specified metric."""
        pass