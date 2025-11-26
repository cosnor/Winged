from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class UserStats:
    """User statistics domain entity"""
    id: Optional[int]
    user_id: int
    total_sightings: int = 0
    unique_species: int = 0
    total_xp: int = 0
    current_level: int = 1
    achievements_unlocked: int = 0
    first_sighting_date: Optional[datetime] = None
    last_sighting_date: Optional[datetime] = None
    longest_streak: int = 0
    current_streak: int = 0
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def add_sighting(self, sighting_date: datetime, is_new_species: bool = False) -> None:
        """Add a new sighting and update stats"""
        self.total_sightings += 1
        
        if is_new_species:
            self.unique_species += 1
        
        if not self.first_sighting_date:
            self.first_sighting_date = sighting_date
        
        self.last_sighting_date = sighting_date
        self._update_streak(sighting_date)
        self.updated_at = datetime.utcnow()
    
    def add_xp(self, xp_amount: int) -> None:
        """Add XP and update level"""
        self.total_xp += xp_amount
        self.current_level = self._calculate_level(self.total_xp)
        self.updated_at = datetime.utcnow()
    
    def unlock_achievement(self) -> None:
        """Increment achievement count"""
        self.achievements_unlocked += 1
        self.updated_at = datetime.utcnow()
    
    def _update_streak(self, sighting_date: datetime) -> None:
        """Update sighting streak"""
        if not self.last_sighting_date:
            self.current_streak = 1
        else:
            days_diff = (sighting_date.date() - self.last_sighting_date.date()).days
            if days_diff == 1:
                # Consecutive day
                self.current_streak += 1
            elif days_diff == 0:
                # Same day, no change to streak
                pass
            else:
                # Streak broken
                self.current_streak = 1
        
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
    
    def _calculate_level(self, total_xp: int) -> int:
        """Calculate user level based on total XP"""
        import math
        return int(math.sqrt(total_xp / 100)) + 1