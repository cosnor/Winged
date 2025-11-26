from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..value_objects.achievement_criteria import AchievementCriteria


@dataclass
class Achievement:
    """Achievement domain entity"""
    id: Optional[int]
    name: str
    description: str
    category: str
    criteria: AchievementCriteria
    xp_reward: int
    icon: Optional[str]
    is_active: bool
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def is_criteria_met(self, user_stats: 'UserStats', user_collection: list) -> bool:
        """Check if achievement criteria is met for given user data"""
        return self.criteria.is_met(user_stats, user_collection, self.category)
    
    def calculate_progress(self, user_stats: 'UserStats', user_collection: list) -> float:
        """Calculate progress towards achievement (0.0 to 1.0)"""
        return self.criteria.calculate_progress(user_stats, user_collection, self.category)