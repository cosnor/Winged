from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from ...domain.entities.species import RarityLevel


@dataclass
class SpeciesDTO:
    """Data Transfer Object for Species."""
    id: Optional[int]
    scientific_name: str
    common_name: str
    common_name_es: Optional[str]
    family: str
    description: Optional[str]
    habitat: Optional[str]
    rarity_level: str
    conservation_status: Optional[str]
    image_url: Optional[str]
    audio_url: Optional[str]
    size_cm: Optional[float]
    weight_g: Optional[float]
    wingspan_cm: Optional[float]
    rarity_points: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserSpeciesDTO:
    """Data Transfer Object for UserSpecies."""
    id: Optional[int]
    user_id: str
    species_id: int
    species: Optional[SpeciesDTO]
    discovered_at: datetime
    location_lat: Optional[float]
    location_lng: Optional[float]
    location_name: Optional[str]
    confidence_score: float
    photo_url: Optional[str]
    audio_url: Optional[str]
    notes: Optional[str]
    verified: bool
    verification_source: Optional[str]
    is_high_confidence: bool
    created_at: Optional[datetime] = None


@dataclass
class CollectionDTO:
    """Data Transfer Object for Collection."""
    id: Optional[int]
    name: str
    description: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    species_count: int
    is_system_collection: bool
    created_by: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CollectionWithSpeciesDTO:
    """Data Transfer Object for Collection with species details."""
    id: Optional[int]
    name: str
    description: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    species: List[SpeciesDTO]
    is_system_collection: bool
    created_by: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserCollectionProgressDTO:
    """Data Transfer Object for user's progress on a collection."""
    collection: CollectionDTO
    total_species: int
    discovered_species: int
    completion_percentage: float
    discovered_species_list: List[UserSpeciesDTO]
    missing_species: List[SpeciesDTO]


@dataclass
class AddSpeciesRequest:
    """Request DTO for adding a species to user's collection."""
    user_id: str
    species_id: int
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    location_name: Optional[str] = None
    confidence_score: float = 1.0
    photo_url: Optional[str] = None
    audio_url: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class SpeciesSearchRequest:
    """Request DTO for searching species."""
    query: str
    rarity_level: Optional[str] = None
    family: Optional[str] = None
    limit: int = 20
    offset: int = 0