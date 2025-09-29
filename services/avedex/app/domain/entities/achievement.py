from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class AchievementType(Enum):
    DISCOVERY = "discovery"  # First species, milestone discoveries
    STREAK = "streak"  # Daily/weekly streaks
    COLLECTION = "collection"  # Complete collections
    RARITY = "rarity"  # Discover rare species
    LOCATION = "location"  # Geographic achievements
    SOCIAL = "social"  # Community interactions
    EXPERTISE = "expertise"  # High confidence identifications


class AchievementTier(Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


@dataclass
class Achievement:
    """Domain entity representing a gamification achievement."""
    
    id: Optional[int]
    name: str
    description: str
    achievement_type: AchievementType
    tier: AchievementTier
    icon: str
    points: int
    requirement_value: int  # e.g., 10 for "discover 10 species"
    requirement_description: str
    is_hidden: bool = False  # Hidden until unlocked
    is_repeatable: bool = False
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    @property
    def tier_multiplier(self) -> float:
        """Get point multiplier based on tier."""
        multipliers = {
            AchievementTier.BRONZE: 1.0,
            AchievementTier.SILVER: 1.5,
            AchievementTier.GOLD: 2.0,
            AchievementTier.PLATINUM: 3.0,
            AchievementTier.DIAMOND: 5.0
        }
        return multipliers[self.tier]
    
    @property
    def total_points(self) -> int:
        """Calculate total points including tier multiplier."""
        return int(self.points * self.tier_multiplier)


@dataclass
class UserAchievement:
    """Domain entity representing a user's unlocked achievement."""
    
    id: Optional[int]
    user_id: str
    achievement_id: int
    unlocked_at: datetime
    progress_value: int  # Current progress towards requirement
    is_completed: bool = False
    completion_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def complete_achievement(self) -> None:
        """Mark achievement as completed."""
        self.is_completed = True
        self.completion_date = datetime.utcnow()
    
    def update_progress(self, new_value: int) -> bool:
        """Update progress and return True if achievement should be completed."""
        self.progress_value = new_value
        return new_value >= self.progress_value  # This would need the requirement_value from Achievement


@dataclass
class UserProgress:
    """Domain entity representing overall user progress and statistics."""
    
    id: Optional[int]
    user_id: str
    total_species_discovered: int = 0
    total_points: int = 0
    current_streak_days: int = 0
    longest_streak_days: int = 0
    last_discovery_date: Optional[datetime] = None
    achievements_unlocked: int = 0
    rare_species_count: int = 0
    collections_completed: int = 0
    total_identifications: int = 0
    high_confidence_identifications: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    @property
    def accuracy_rate(self) -> float:
        """Calculate identification accuracy rate."""
        if self.total_identifications == 0:
            return 0.0
        return self.high_confidence_identifications / self.total_identifications
    
    @property
    def average_points_per_species(self) -> float:
        """Calculate average points earned per species."""
        if self.total_species_discovered == 0:
            return 0.0
        return self.total_points / self.total_species_discovered
    
    def add_species_discovery(self, species_points: int, is_high_confidence: bool = False) -> None:
        """Update progress when a new species is discovered."""
        self.total_species_discovered += 1
        self.total_points += species_points
        self.total_identifications += 1
        
        if is_high_confidence:
            self.high_confidence_identifications += 1
        
        # Update streak
        now = datetime.utcnow()
        if self.last_discovery_date:
            days_since_last = (now - self.last_discovery_date).days
            if days_since_last == 1:
                self.current_streak_days += 1
            elif days_since_last > 1:
                self.current_streak_days = 1
        else:
            self.current_streak_days = 1
        
        if self.current_streak_days > self.longest_streak_days:
            self.longest_streak_days = self.current_streak_days
        
        self.last_discovery_date = now
        self.updated_at = now
    
    def add_achievement(self, points: int) -> None:
        """Update progress when an achievement is unlocked."""
        self.achievements_unlocked += 1
        self.total_points += points
        self.updated_at = datetime.utcnow()
    
    def increment_rare_species(self) -> None:
        """Increment rare species counter."""
        self.rare_species_count += 1
        self.updated_at = datetime.utcnow()
    
    def complete_collection(self) -> None:
        """Increment completed collections counter."""
        self.collections_completed += 1
        self.updated_at = datetime.utcnow()