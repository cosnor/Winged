from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Location:
    """Value object for geographical location"""
    latitude: float
    longitude: float
    
    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")
    
    @classmethod
    def from_coordinates(cls, lat: Optional[float], lon: Optional[float]) -> Optional['Location']:
        """Create location from optional coordinates"""
        if lat is not None and lon is not None:
            return cls(latitude=lat, longitude=lon)
        return None
    
    def distance_to(self, other: 'Location') -> float:
        """Calculate distance to another location in kilometers using Haversine formula"""
        import math
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [self.latitude, self.longitude, 
                                                    other.latitude, other.longitude])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        return c * r
    
    def __str__(self) -> str:
        return f"({self.latitude}, {self.longitude})"