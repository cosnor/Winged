from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .achievement import Achievement


@dataclass
class UserAchievement:
    """User achievement domain entity"""
    id: Optional[int]
    user_id: int
    achievement_id: int
    unlocked_at: datetime
    progress: float
    achievement: Optional[Achievement] = None
    
    def __post_init__(self):
        if self.unlocked_at is None:
            self.unlocked_at = datetime.utcnow()
    
    def is_unlocked(self) -> bool:
        """Check if achievement is fully unlocked"""
        return self.progress >= 1.0
    
    def update_progress(self, new_progress: float) -> None:
        """Update achievement progress"""
        self.progress = min(1.0, max(0.0, new_progress))