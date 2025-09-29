from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class AchievementDTO:
    """Data Transfer Object for Achievement."""
    id: Optional[int]
    name: str
    description: str
    achievement_type: str
    tier: str
    icon: str
    points: int
    total_points: int
    requirement_value: int
    requirement_description: str
    is_hidden: bool
    is_repeatable: bool
    created_at: Optional[datetime] = None


@dataclass
class UserAchievementDTO:
    """Data Transfer Object for UserAchievement."""
    id: Optional[int]
    user_id: str
    achievement: AchievementDTO
    unlocked_at: datetime
    progress_value: int
    is_completed: bool
    completion_date: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass
class UserProgressDTO:
    """Data Transfer Object for UserProgress."""
    id: Optional[int]
    user_id: str
    total_species_discovered: int
    total_points: int
    current_streak_days: int
    longest_streak_days: int
    last_discovery_date: Optional[datetime]
    achievements_unlocked: int
    rare_species_count: int
    collections_completed: int
    total_identifications: int
    high_confidence_identifications: int
    accuracy_rate: float
    average_points_per_species: float
    rank: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class LeaderboardEntryDTO:
    """Data Transfer Object for leaderboard entries."""
    user_id: str
    rank: int
    total_points: int
    total_species_discovered: int
    achievements_unlocked: int
    current_streak_days: int


@dataclass
class UserStatisticsDTO:
    """Data Transfer Object for comprehensive user statistics."""
    user_progress: UserProgressDTO
    recent_achievements: List[UserAchievementDTO]
    recent_discoveries: List['UserSpeciesDTO']  # Forward reference
    collection_progress: List['UserCollectionProgressDTO']  # Forward reference
    leaderboard_position: Optional[LeaderboardEntryDTO] = None


@dataclass
class AchievementProgressDTO:
    """Data Transfer Object for tracking achievement progress."""
    achievement: AchievementDTO
    current_progress: int
    required_progress: int
    completion_percentage: float
    is_completed: bool
    estimated_completion: Optional[str] = None  # e.g., "2 more discoveries needed"