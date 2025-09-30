from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.entities.achievement import Achievement
from ...domain.entities.user_achievement import UserAchievement
from ...domain.entities.bird_collection import BirdCollection
from ...domain.entities.user_stats import UserStats


class AchievementRepository(ABC):
    """Repository interface for achievements"""
    
    @abstractmethod
    def get_all_active(self) -> List[Achievement]:
        """Get all active achievements"""
        pass
    
    @abstractmethod
    def get_by_id(self, achievement_id: int) -> Optional[Achievement]:
        """Get achievement by ID"""
        pass
    
    @abstractmethod
    def create(self, achievement: Achievement) -> Achievement:
        """Create a new achievement"""
        pass
    
    @abstractmethod
    def update(self, achievement: Achievement) -> Achievement:
        """Update an existing achievement"""
        pass


class UserAchievementRepository(ABC):
    """Repository interface for user achievements"""
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[UserAchievement]:
        """Get all achievements for a user"""
        pass
    
    @abstractmethod
    def get_by_user_and_achievement(self, user_id: int, achievement_id: int) -> Optional[UserAchievement]:
        """Get specific user achievement"""
        pass
    
    @abstractmethod
    def create(self, user_achievement: UserAchievement) -> UserAchievement:
        """Create a new user achievement"""
        pass
    
    @abstractmethod
    def update(self, user_achievement: UserAchievement) -> UserAchievement:
        """Update user achievement progress"""
        pass


class BirdCollectionRepository(ABC):
    """Repository interface for bird collections"""
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[BirdCollection]:
        """Get user's bird collection"""
        pass
    
    @abstractmethod
    def get_by_user_and_species(self, user_id: int, species_name: str) -> Optional[BirdCollection]:
        """Get specific bird entry for user"""
        pass
    
    @abstractmethod
    def create(self, bird_collection: BirdCollection) -> BirdCollection:
        """Create a new bird collection entry"""
        pass
    
    @abstractmethod
    def update(self, bird_collection: BirdCollection) -> BirdCollection:
        """Update bird collection entry"""
        pass
    
    @abstractmethod
    def get_all_species(self) -> List[str]:
        """Get list of all species that have been sighted"""
        pass
    
    @abstractmethod
    def get_users_with_species(self, species_name: str) -> List[int]:
        """Get list of user IDs who have sighted a specific species"""
        pass


class UserStatsRepository(ABC):
    """Repository interface for user statistics"""
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[UserStats]:
        """Get user statistics"""
        pass
    
    @abstractmethod
    def create(self, user_stats: UserStats) -> UserStats:
        """Create new user statistics"""
        pass
    
    @abstractmethod
    def update(self, user_stats: UserStats) -> UserStats:
        """Update user statistics"""
        pass
    
    @abstractmethod
    def get_leaderboard_by_species(self, limit: int = 10) -> List[UserStats]:
        """Get leaderboard ordered by unique species count"""
        pass
    
    @abstractmethod
    def get_leaderboard_by_xp(self, limit: int = 10) -> List[UserStats]:
        """Get leaderboard ordered by total XP"""
        pass