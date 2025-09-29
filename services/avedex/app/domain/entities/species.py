from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class RarityLevel(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    VERY_RARE = "very_rare"
    LEGENDARY = "legendary"


@dataclass
class Species:
    """Domain entity representing a bird species."""
    
    id: Optional[int]
    scientific_name: str
    common_name: str
    common_name_es: Optional[str]  # Spanish common name
    family: str
    description: Optional[str]
    habitat: Optional[str]
    rarity_level: RarityLevel
    conservation_status: Optional[str]
    image_url: Optional[str]
    audio_url: Optional[str]
    size_cm: Optional[float]
    weight_g: Optional[float]
    wingspan_cm: Optional[float]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    @property
    def rarity_points(self) -> int:
        """Calculate points based on rarity level."""
        rarity_points_map = {
            RarityLevel.COMMON: 10,
            RarityLevel.UNCOMMON: 25,
            RarityLevel.RARE: 50,
            RarityLevel.VERY_RARE: 100,
            RarityLevel.LEGENDARY: 200
        }
        return rarity_points_map[self.rarity_level]
    
    def is_endemic_to_caribbean(self) -> bool:
        """Check if species is endemic to Caribbean region."""
        # This would be determined by habitat or specific flags
        return "caribbean" in (self.habitat or "").lower()


@dataclass
class UserSpecies:
    """Domain entity representing a user's discovered species."""
    
    id: Optional[int]
    user_id: str
    species_id: int
    discovered_at: datetime
    location_lat: Optional[float]
    location_lng: Optional[float]
    location_name: Optional[str]
    confidence_score: float  # BirdNet confidence (0.0 to 1.0)
    photo_url: Optional[str]
    audio_url: Optional[str]
    notes: Optional[str]
    verified: bool = False
    verification_source: Optional[str] = None  # "expert", "community", "ai"
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    @property
    def is_high_confidence(self) -> bool:
        """Check if detection has high confidence."""
        return self.confidence_score >= 0.8
    
    @property
    def location_coordinates(self) -> Optional[tuple[float, float]]:
        """Get location as coordinate tuple."""
        if self.location_lat is not None and self.location_lng is not None:
            return (self.location_lat, self.location_lng)
        return None


@dataclass
class Collection:
    """Domain entity representing a themed collection of species."""
    
    id: Optional[int]
    name: str
    description: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    species_ids: list[int]
    is_system_collection: bool = False  # System vs user-created collections
    created_by: Optional[str] = None  # User ID who created it
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    @property
    def species_count(self) -> int:
        """Get total number of species in collection."""
        return len(self.species_ids)
    
    def contains_species(self, species_id: int) -> bool:
        """Check if collection contains a specific species."""
        return species_id in self.species_ids
    
    def add_species(self, species_id: int) -> None:
        """Add species to collection if not already present."""
        if species_id not in self.species_ids:
            self.species_ids.append(species_id)
            self.updated_at = datetime.utcnow()
    
    def remove_species(self, species_id: int) -> None:
        """Remove species from collection."""
        if species_id in self.species_ids:
            self.species_ids.remove(species_id)
            self.updated_at = datetime.utcnow()