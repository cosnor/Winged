from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AchievementResponse(BaseModel):
    """Response schema for achievements"""
    id: int
    name: str
    description: str
    category: str
    criteria: Optional[str] = None
    xp_reward: int
    icon: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    """Response schema for user achievements"""
    id: int
    user_id: int
    achievement_id: int
    unlocked_at: datetime
    progress: float
    achievement: AchievementResponse
    
    class Config:
        from_attributes = True


class BirdCollectionResponse(BaseModel):
    """Response schema for bird collection entries"""
    id: int
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    first_sighted_at: datetime
    sighting_count: int
    last_sighted_at: datetime
    confidence_score: Optional[float] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    
    class Config:
        from_attributes = True


class UserStatsResponse(BaseModel):
    """Response schema for user statistics"""
    id: int
    user_id: int
    total_sightings: int
    unique_species: int
    total_xp: int
    current_level: int
    achievements_unlocked: int
    first_sighting_date: Optional[datetime] = None
    last_sighting_date: Optional[datetime] = None
    longest_streak: int
    current_streak: int
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserCollectionResponse(BaseModel):
    """Response schema for user's bird collection"""
    user_id: int
    birds: List[BirdCollectionResponse]
    stats: UserStatsResponse
    recent_achievements: List[UserAchievementResponse]


class AchievementProgressResponse(BaseModel):
    """Response schema for achievement progress"""
    achievement: AchievementResponse
    progress: float
    is_unlocked: bool
    unlocked_at: Optional[datetime] = None


class LeaderboardEntryResponse(BaseModel):
    """Response schema for leaderboard entries"""
    user_id: int
    rank: int
    unique_species: Optional[int] = None
    total_sightings: Optional[int] = None
    total_xp: Optional[int] = None
    level: int
    achievements_unlocked: Optional[int] = None


class SpeciesDetectionResponse(BaseModel):
    """Response schema for species detection processing"""
    user_id: int
    species_detected: str
    achievements_triggered: List[AchievementResponse]
    new_achievements_count: int
    total_achievements_count: int
    xp_earned: int
    total_xp: int


class BatchSpeciesDetectionResponse(BaseModel):
    """Response schema for batch species detection processing"""
    processed_count: int
    success_count: int
    error_count: int
    total_achievements_triggered: int
    total_xp_earned: int
    results: List[SpeciesDetectionResponse]
    errors: Optional[List[str]] = None