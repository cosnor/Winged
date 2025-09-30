from dataclasses import dataclass
from typing import List, Optional
from ..interfaces.repositories import AchievementRepository
from ...domain.entities.achievement import Achievement
from ...domain.value_objects.achievement_criteria import AchievementCriteria


@dataclass
class CreateAchievementRequest:
    name: str
    description: str
    category: str
    criteria_data: dict
    xp_reward: int
    icon: Optional[str] = None


@dataclass
class GetAchievementRequest:
    achievement_id: int


@dataclass
class GetAllAchievementsRequest:
    pass


class ManageAchievementsUseCase:
    """Use case for managing achievements (admin operations)"""
    
    def __init__(self, achievement_repo: AchievementRepository):
        self.achievement_repo = achievement_repo
    
    def create_achievement(self, request: CreateAchievementRequest) -> Achievement:
        """Create a new achievement"""
        criteria = AchievementCriteria.from_dict(request.criteria_data)
        
        achievement = Achievement(
            id=None,
            name=request.name,
            description=request.description,
            category=request.category,
            criteria=criteria,
            xp_reward=request.xp_reward,
            icon=request.icon,
            is_active=True
        )
        
        return self.achievement_repo.create(achievement)
    
    def get_achievement(self, request: GetAchievementRequest) -> Optional[Achievement]:
        """Get a specific achievement"""
        return self.achievement_repo.get_by_id(request.achievement_id)
    
    def get_all_achievements(self, request: GetAllAchievementsRequest) -> List[Achievement]:
        """Get all active achievements"""
        return self.achievement_repo.get_all_active()
    
    def create_default_achievements(self) -> List[Achievement]:
        """Create default achievements if they don't exist"""
        default_achievements_data = [
            {
                "name": "First Flight",
                "description": "Identify your first bird species",
                "category": "first_bird",
                "criteria_data": {},
                "xp_reward": 100,
                "icon": "first_bird"
            },
            {
                "name": "Novice Birder",
                "description": "Identify 5 different bird species",
                "category": "species_count",
                "criteria_data": {"count": 5},
                "xp_reward": 250,
                "icon": "novice"
            },
            {
                "name": "Experienced Birder",
                "description": "Identify 25 different bird species",
                "category": "species_count",
                "criteria_data": {"count": 25},
                "xp_reward": 500,
                "icon": "experienced"
            },
            {
                "name": "Expert Birder",
                "description": "Identify 50 different bird species",
                "category": "species_count",
                "criteria_data": {"count": 50},
                "xp_reward": 1000,
                "icon": "expert"
            },
            {
                "name": "Master Birder",
                "description": "Identify 100 different bird species",
                "category": "species_count",
                "criteria_data": {"count": 100},
                "xp_reward": 2000,
                "icon": "master"
            },
            {
                "name": "Active Observer",
                "description": "Record 50 bird sightings",
                "category": "sighting_count",
                "criteria_data": {"count": 50},
                "xp_reward": 300,
                "icon": "active"
            },
            {
                "name": "Dedicated Watcher",
                "description": "Record sightings for 7 consecutive days",
                "category": "streak",
                "criteria_data": {"days": 7},
                "xp_reward": 400,
                "icon": "streak_7"
            },
            {
                "name": "Committed Birder",
                "description": "Record sightings for 30 consecutive days",
                "category": "streak",
                "criteria_data": {"days": 30},
                "xp_reward": 1000,
                "icon": "streak_30"
            }
        ]
        
        created_achievements = []
        for data in default_achievements_data:
            # Check if achievement already exists by name
            existing_achievements = self.achievement_repo.get_all_active()
            if not any(a.name == data["name"] for a in existing_achievements):
                request = CreateAchievementRequest(**data)
                achievement = self.create_achievement(request)
                created_achievements.append(achievement)
        
        return created_achievements