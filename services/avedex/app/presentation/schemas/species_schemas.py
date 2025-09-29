from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class RarityLevelSchema(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    VERY_RARE = "very_rare"
    LEGENDARY = "legendary"


class SpeciesResponse(BaseModel):
    """Response schema for Species."""
    id: int
    scientific_name: str
    common_name: str
    common_name_es: Optional[str] = None
    family: str
    description: Optional[str] = None
    habitat: Optional[str] = None
    rarity_level: RarityLevelSchema
    conservation_status: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    size_cm: Optional[float] = None
    weight_g: Optional[float] = None
    wingspan_cm: Optional[float] = None
    rarity_points: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSpeciesResponse(BaseModel):
    """Response schema for UserSpecies."""
    id: int
    user_id: str
    species_id: int
    species: Optional[SpeciesResponse] = None
    discovered_at: datetime
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    location_name: Optional[str] = None
    confidence_score: float = Field(ge=0.0, le=1.0)
    photo_url: Optional[str] = None
    audio_url: Optional[str] = None
    notes: Optional[str] = None
    verified: bool = False
    verification_source: Optional[str] = None
    is_high_confidence: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CollectionResponse(BaseModel):
    """Response schema for Collection."""
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    species_count: int
    is_system_collection: bool
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CollectionWithSpeciesResponse(BaseModel):
    """Response schema for Collection with species details."""
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    species: List[SpeciesResponse]
    is_system_collection: bool
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCollectionProgressResponse(BaseModel):
    """Response schema for user's progress on a collection."""
    collection: CollectionResponse
    total_species: int
    discovered_species: int
    completion_percentage: float = Field(ge=0.0, le=100.0)
    discovered_species_list: List[UserSpeciesResponse]
    missing_species: List[SpeciesResponse]

    class Config:
        from_attributes = True


class AddSpeciesRequest(BaseModel):
    """Request schema for adding a species to user's collection."""
    species_id: int = Field(gt=0)
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lng: Optional[float] = Field(None, ge=-180, le=180)
    location_name: Optional[str] = Field(None, max_length=255)
    confidence_score: float = Field(1.0, ge=0.0, le=1.0)
    photo_url: Optional[str] = Field(None, max_length=500)
    audio_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)


class SpeciesSearchRequest(BaseModel):
    """Request schema for searching species."""
    query: str = Field(min_length=1, max_length=255)
    rarity_level: Optional[RarityLevelSchema] = None
    family: Optional[str] = Field(None, max_length=100)
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)


class BirdNetIdentificationRequest(BaseModel):
    """Request schema for BirdNet species identification."""
    audio_url: str = Field(max_length=500)
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lng: Optional[float] = Field(None, ge=-180, le=180)
    location_name: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)


class BirdNetIdentificationResponse(BaseModel):
    """Response schema for BirdNet species identification."""
    species: SpeciesResponse
    confidence_score: float = Field(ge=0.0, le=1.0)
    user_species: Optional[UserSpeciesResponse] = None
    is_new_discovery: bool
    message: str