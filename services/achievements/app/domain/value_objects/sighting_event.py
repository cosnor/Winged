from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .location import Location


@dataclass(frozen=True)
class SightingEvent:
    """Value object for bird sighting events"""
    user_id: int
    species_name: str
    common_name: Optional[str]
    confidence_score: float
    location: Location
    timestamp: datetime
    
    def __post_init__(self):
        if not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")
        if self.user_id <= 0:
            raise ValueError("User ID must be positive")
        if not self.species_name.strip():
            raise ValueError("Species name cannot be empty")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SightingEvent':
        """Create sighting event from dictionary"""
        location = Location(
            latitude=data['location_lat'],
            longitude=data['location_lon']
        )
        
        return cls(
            user_id=data['user_id'],
            species_name=data['species_name'],
            common_name=data.get('common_name'),
            confidence_score=data['confidence_score'],
            location=location,
            timestamp=data['timestamp']
        )
    
    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """Check if sighting has high confidence score"""
        return self.confidence_score >= threshold
    
    def is_same_species(self, other: 'SightingEvent') -> bool:
        """Check if this sighting is of the same species as another"""
        return self.species_name == other.species_name
    
    def is_same_day(self, other_timestamp: datetime) -> bool:
        """Check if sighting occurred on the same day as given timestamp"""
        return self.timestamp.date() == other_timestamp.date()