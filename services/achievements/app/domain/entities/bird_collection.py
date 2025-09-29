from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..value_objects.location import Location


@dataclass
class BirdCollection:
    """Bird collection domain entity"""
    id: Optional[int]
    user_id: int
    species_name: str
    common_name: Optional[str]
    first_sighted_at: datetime
    sighting_count: int
    last_sighted_at: datetime
    confidence_score: Optional[float]
    location: Optional[Location]
    
    def __post_init__(self):
        if self.first_sighted_at is None:
            self.first_sighted_at = datetime.utcnow()
        if self.last_sighted_at is None:
            self.last_sighted_at = self.first_sighted_at
        if self.sighting_count is None:
            self.sighting_count = 1
    
    def add_sighting(self, confidence_score: Optional[float] = None, 
                    location: Optional[Location] = None) -> None:
        """Add a new sighting of this species"""
        self.sighting_count += 1
        self.last_sighted_at = datetime.utcnow()
        
        if confidence_score and (not self.confidence_score or confidence_score > self.confidence_score):
            self.confidence_score = confidence_score
        
        if location and not self.location:
            self.location = location
    
    def is_rare_species(self, rare_species_list: list[str]) -> bool:
        """Check if this is a rare species"""
        return self.species_name in rare_species_list