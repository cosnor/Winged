from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from typing import Any, Dict
from typing import Literal


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
    user_id: Optional[int] = None
    species_name: str  # Scientific name
    common_name: Optional[str] = None  # Common name
    timestamp: Optional[datetime] = None


class SightingResponse(BaseModel):
    id: int
    user_id: int
    species_name: str
    common_name: Optional[str] = None
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


# --- Service-mirroring schemas (match the achievements service responses) ---
class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    criteria: Optional[str] = None
    xp_reward: int
    icon: Optional[str] = None
    is_active: bool
    created_at: datetime


class UserAchievementResponse(BaseModel):
    id: int
    user_id: int
    achievement_id: int
    unlocked_at: datetime
    progress: float
    achievement: AchievementResponse


class BirdCollectionResponse(BaseModel):
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


class UserStatsResponse(BaseModel):
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


class UserCollectionResponse(BaseModel):
    user_id: int
    birds: List[BirdCollectionResponse]
    stats: UserStatsResponse
    recent_achievements: List[UserAchievementResponse]


class AchievementProgressResponse(BaseModel):
    achievement: AchievementResponse
    progress: float
    is_unlocked: bool
    unlocked_at: Optional[datetime] = None


class SpeciesLeaderboardEntry(BaseModel):
    species_name: str
    sightings_count: int


class XPLeaderboardEntry(BaseModel):
    user_id: int
    name: str
    xp: int
    rank: Optional[int] = None


class LeaderboardEntryResponse(BaseModel):
    user_id: int
    rank: int
    unique_species: Optional[int] = None
    total_sightings: Optional[int] = None
    total_xp: Optional[int] = None
    level: int
    achievements_unlocked: Optional[int] = None


class SpeciesListResponse(BaseModel):
    species: List[str]


class HeatmapPoint(BaseModel):
    lat: float
    lon: float
    weight: Optional[float] = 1.0


class HeatmapResponse(BaseModel):
    points: List[HeatmapPoint]


class PredictRequest(BaseModel):
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None


class LocationPoint(BaseModel):
    lat: float
    lon: float


class SpeciesProbability(BaseModel):
    species: str
    probability: float


class PredictResponse(BaseModel):
    zone: str
    location: LocationPoint
    datetime: datetime
    species_probabilities: List[SpeciesProbability]


# GeoJSON schemas for zones
class Geometry(BaseModel):
    type: str
    coordinates: Any


class Feature(BaseModel):
    id: Optional[str]
    type: Literal["Feature"]
    properties: Dict[str, Any]
    geometry: Geometry
    bbox: Optional[List[float]] = None


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[Feature]
    bbox: Optional[List[float]] = None


class DistributionRequest(BaseModel):
    lat: float
    lon: float
    # use a python-safe attribute name and accept JSON alias "datetime"
    datetime_: Optional[datetime] = Field(default=None, alias="datetime")
    grid_size: Optional[float] = 0.001


class SpeciesDistribution(BaseModel):
    species: str
    # structure is free-form (could be grid, list of points, etc.)
    distribution: Optional[Dict[str, Any]] = Field(default_factory=dict)


class DistributionResponse(BaseModel):
    zone: str
    location: LocationPoint
    datetime: datetime
    species_distributions: List[SpeciesDistribution]


class BirdIdentificationResponse(BaseModel):
    species: str
    confidence: float
    species_code: Optional[str] = None
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    achievements_triggered: List[str] = []
    sighting_created: bool = False

