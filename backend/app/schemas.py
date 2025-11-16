from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserSignupRequest(BaseModel):
    name: str
    email: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "strongPassword123!"
            }
        }

class UserLoginRequest(BaseModel):
    email: str
    password: str
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "strongPassword123!"
            }
        }

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    xp: int = 0
    level: int = 1
    is_active: bool = True
    created_at: Optional[datetime] = None


class SightingRequest(BaseModel):
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: float
    lat: float
    lon: float
    timestamp: Optional[datetime] = None
    audio_url: Optional[str] = None


class SightingResponse(BaseModel):
    id: int
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: float
    location_lat: float
    location_lon: float
    timestamp: datetime
    status: str = "processed"
    achievements_unlocked: List[dict] = []


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None


class SignupResponse(BaseModel):
    success: bool
    message: str
    data: Optional[UserResponse] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None


class AchievementUnlocked(BaseModel):
    achievement_id: int
    title: str
    description: Optional[str] = None
    unlocked_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "achievement_id": 1,
                "title": "First Sighting",
                "description": "Awarded for your first sighting",
                "unlocked_at": "2025-11-15T12:34:56"
            }
        }


class AchievementDefinition(BaseModel):
    id: int
    title: str
    description: Optional[str] = None


class AchievementCollectionResponse(BaseModel):
    user_id: int
    achievements: List[AchievementUnlocked]


class SpeciesLeaderboardEntry(BaseModel):
    species_name: str
    sightings_count: int


class XPLeaderboardEntry(BaseModel):
    user_id: int
    name: str
    xp: int
    rank: Optional[int] = None


class HeatmapPoint(BaseModel):
    lat: float
    lon: float
    weight: Optional[float] = 1.0


class HeatmapResponse(BaseModel):
    points: List[HeatmapPoint]

