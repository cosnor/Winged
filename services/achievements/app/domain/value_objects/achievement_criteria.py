from dataclasses import dataclass
from typing import Dict, Any, List
import json


@dataclass(frozen=True)
class AchievementCriteria:
    """Value object for achievement criteria"""
    criteria_data: Dict[str, Any]
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AchievementCriteria':
        """Create criteria from JSON string"""
        try:
            data = json.loads(json_str) if json_str else {}
        except json.JSONDecodeError:
            data = {}
        return cls(criteria_data=data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AchievementCriteria':
        """Create criteria from dictionary"""
        return cls(criteria_data=data)
    
    def to_json(self) -> str:
        """Convert criteria to JSON string"""
        return json.dumps(self.criteria_data)
    
    def get_count_requirement(self) -> int:
        """Get count requirement from criteria"""
        return self.criteria_data.get("count", 1)
    
    def get_days_requirement(self) -> int:
        """Get days requirement from criteria"""
        return self.criteria_data.get("days", 1)
    
    def get_species_list(self) -> List[str]:
        """Get species list from criteria"""
        return self.criteria_data.get("species", [])
    
    def is_met(self, user_stats: 'UserStats', user_collection: list, category: str) -> bool:
        """Check if criteria is met"""
        if category == "species_count":
            return user_stats.unique_species >= self.get_count_requirement()
        
        elif category == "first_bird":
            return user_stats.unique_species >= 1
        
        elif category == "sighting_count":
            return user_stats.total_sightings >= self.get_count_requirement()
        
        elif category == "streak":
            return user_stats.longest_streak >= self.get_days_requirement()
        
        elif category == "rare_species":
            rare_species = self.get_species_list()
            if rare_species:
                user_species = [bird.species_name for bird in user_collection]
                return any(species in user_species for species in rare_species)
        
        return False
    
    def calculate_progress(self, user_stats: 'UserStats', user_collection: list, category: str) -> float:
        """Calculate progress towards criteria (0.0 to 1.0)"""
        if category == "species_count":
            target_count = self.get_count_requirement()
            return min(1.0, user_stats.unique_species / target_count)
        
        elif category == "sighting_count":
            target_count = self.get_count_requirement()
            return min(1.0, user_stats.total_sightings / target_count)
        
        elif category == "streak":
            target_streak = self.get_days_requirement()
            return min(1.0, user_stats.longest_streak / target_streak)
        
        elif category in ["first_bird", "rare_species"]:
            return 1.0 if self.is_met(user_stats, user_collection, category) else 0.0
        
        return 0.0