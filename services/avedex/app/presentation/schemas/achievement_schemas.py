from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .species_schemas import UserSpeciesResponse, UserCollectionProgressResponse


class AchievementTypeSchema(str, Enum):
    DISCOVERY = "discovery"
    STREAK = "streak"
    COLLECTION = "collection"
    RARITY = "rarity"
    LOCATION = "location"
    SOCIAL = "social"
    EXPERTISE = "expertise"


class AchievementTierSchema(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class AchievementResponse(BaseModel):
    """Response schema for Achievement."""
    id: int
    name: str
    description: str
    achievement_type: AchievementTypeSchema
    tier: AchievementTierSchema
    icon: str
    points: int
    total_points: int
    requirement_value: int
    requirement_description: str
    is_hidden: bool
    is_repeatable: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    """Response schema for UserAchievement."""
    id: int
    user_id: str
    achievement: AchievementResponse
    unlocked_at: datetime
    progress_value: int
    is_completed: bool
    completion_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserProgressResponse(BaseModel):
    """Response schema for UserProgress."""
    id: int
    user_id: str
    total_species_discovered: int
    total_points: int
    current_streak_days: int
    longest_streak_days: int
    last_discovery_date: Optional[datetime] = None
    achievements_unlocked: int
    rare_species_count: int
    collections_completed: int
    total_identifications: int
    high_confidence_identifications: int
    accuracy_rate: float = Field(ge=0.0, le=1.0)
    average_points_per_species: float
    rank: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeaderboardEntryResponse(BaseModel):
    """Response schema for leaderboard entries."""
    user_id: str
    rank: int
    total_points: int
    total_species_discovered: int
    achievements_unlocked: int
    current_streak_days: int

    class Config:
        from_attributes = True


class UserStatisticsResponse(BaseModel):
    """Response schema for comprehensive user statistics."""
    user_progress: UserProgressResponse
    recent_achievements: List[UserAchievementResponse]
    recent_discoveries: List['UserSpeciesResponse']  # Forward reference
    collection_progress: List['UserCollectionProgressResponse']  # Forward reference
    leaderboard_position: Optional[LeaderboardEntryResponse] = None

    class Config:
        from_attributes = True


class AchievementProgressResponse(BaseModel):
    """Response schema for tracking achievement progress."""
    achievement: AchievementResponse
    current_progress: int
    required_progress: int
    completion_percentage: float = Field(ge=0.0, le=100.0)
    is_completed: bool
    estimated_completion: Optional[str] = None

    class Config:
        from_attributes = True


class AchievementUnlockedNotification(BaseModel):
    """Schema for achievement unlocked notifications."""
    achievement: AchievementResponse
    user_id: str
    unlocked_at: datetime
    points_earned: int
    message: str = "¡Nuevo logro desbloqueado!"

    class Config:
        from_attributes = True