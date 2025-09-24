from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AchievementBase(BaseModel):
    name: str
    description: str
    category: str
    criteria: Optional[str] = None
    xp_reward: int = 0
    icon: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserAchievementBase(BaseModel):
    user_id: int
    achievement_id: int
    progress: float = 0.0

class UserAchievementCreate(UserAchievementBase):
    pass

class UserAchievement(UserAchievementBase):
    id: int
    unlocked_at: datetime
    achievement: Achievement
    
    class Config:
        from_attributes = True

class BirdCollectionBase(BaseModel):
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: Optional[float] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None

class BirdCollectionCreate(BirdCollectionBase):
    pass

class BirdCollection(BirdCollectionBase):
    id: int
    first_sighted_at: datetime
    sighting_count: int
    last_sighted_at: datetime
    
    class Config:
        from_attributes = True

class UserStatsBase(BaseModel):
    user_id: int
    total_sightings: int = 0
    unique_species: int = 0
    total_xp: int = 0
    current_level: int = 1
    achievements_unlocked: int = 0
    longest_streak: int = 0
    current_streak: int = 0

class UserStatsCreate(UserStatsBase):
    pass

class UserStats(UserStatsBase):
    id: int
    first_sighting_date: Optional[datetime] = None
    last_sighting_date: Optional[datetime] = None
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SightingEvent(BaseModel):
    """Schema for receiving sighting events from other services"""
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: float
    location_lat: float
    location_lon: float
    timestamp: datetime

class UserCollectionResponse(BaseModel):
    """Response schema for user's bird collection"""
    user_id: int
    birds: List[BirdCollection]
    stats: UserStats
    recent_achievements: List[UserAchievement]

class AchievementProgress(BaseModel):
    """Schema for achievement progress"""
    achievement: Achievement
    progress: float
    is_unlocked: bool
    unlocked_at: Optional[datetime] = None