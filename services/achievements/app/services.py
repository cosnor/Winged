from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
import json

from . import models, schemas

class AchievementService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_stats(self, user_id: int) -> Optional[models.UserStats]:
        """Get or create user stats"""
        stats = self.db.query(models.UserStats).filter(models.UserStats.user_id == user_id).first()
        if not stats:
            stats = models.UserStats(user_id=user_id)
            self.db.add(stats)
            self.db.commit()
            self.db.refresh(stats)
        return stats
    
    def get_user_collection(self, user_id: int) -> List[models.BirdCollection]:
        """Get user's bird collection"""
        return self.db.query(models.BirdCollection).filter(
            models.BirdCollection.user_id == user_id
        ).order_by(models.BirdCollection.first_sighted_at.desc()).all()
    
    def get_user_achievements(self, user_id: int) -> List[models.UserAchievement]:
        """Get user's unlocked achievements"""
        return self.db.query(models.UserAchievement).filter(
            models.UserAchievement.user_id == user_id
        ).join(models.Achievement).order_by(models.UserAchievement.unlocked_at.desc()).all()
    
    def get_achievement_progress(self, user_id: int) -> List[schemas.AchievementProgress]:
        """Get user's progress on all achievements"""
        achievements = self.db.query(models.Achievement).filter(models.Achievement.is_active == True).all()
        progress_list = []
        
        for achievement in achievements:
            user_achievement = self.db.query(models.UserAchievement).filter(
                and_(
                    models.UserAchievement.user_id == user_id,
                    models.UserAchievement.achievement_id == achievement.id
                )
            ).first()
            
            if user_achievement:
                progress_list.append(schemas.AchievementProgress(
                    achievement=achievement,
                    progress=1.0,
                    is_unlocked=True,
                    unlocked_at=user_achievement.unlocked_at
                ))
            else:
                # Calculate progress towards achievement
                progress = self._calculate_achievement_progress(user_id, achievement)
                progress_list.append(schemas.AchievementProgress(
                    achievement=achievement,
                    progress=progress,
                    is_unlocked=False
                ))
        
        return progress_list
    
    def process_sighting(self, sighting: schemas.SightingEvent) -> List[models.UserAchievement]:
        """Process a new sighting and check for achievements"""
        newly_unlocked = []
        
        # Update or create bird collection entry
        bird_entry = self.db.query(models.BirdCollection).filter(
            and_(
                models.BirdCollection.user_id == sighting.user_id,
                models.BirdCollection.species_name == sighting.species_name
            )
        ).first()
        
        is_new_species = False
        if bird_entry:
            # Update existing entry
            bird_entry.sighting_count += 1
            bird_entry.last_sighted_at = sighting.timestamp
            if sighting.confidence_score > (bird_entry.confidence_score or 0):
                bird_entry.confidence_score = sighting.confidence_score
        else:
            # Create new entry
            is_new_species = True
            bird_entry = models.BirdCollection(
                user_id=sighting.user_id,
                species_name=sighting.species_name,
                common_name=sighting.common_name,
                first_sighted_at=sighting.timestamp,
                last_sighted_at=sighting.timestamp,
                confidence_score=sighting.confidence_score,
                location_lat=sighting.location_lat,
                location_lon=sighting.location_lon
            )
            self.db.add(bird_entry)
        
        # Update user stats
        stats = self.get_user_stats(sighting.user_id)
        stats.total_sightings += 1
        if is_new_species:
            stats.unique_species += 1
        
        if not stats.first_sighting_date:
            stats.first_sighting_date = sighting.timestamp
        stats.last_sighting_date = sighting.timestamp
        
        # Update streak
        self._update_user_streak(stats, sighting.timestamp)
        
        self.db.commit()
        
        # Check for new achievements
        newly_unlocked = self._check_achievements(sighting.user_id)
        
        return newly_unlocked
    
    def _update_user_streak(self, stats: models.UserStats, sighting_time: datetime):
        """Update user's sighting streak"""
        if not stats.last_sighting_date:
            stats.current_streak = 1
        else:
            days_diff = (sighting_time.date() - stats.last_sighting_date.date()).days
            if days_diff == 1:
                # Consecutive day
                stats.current_streak += 1
            elif days_diff == 0:
                # Same day, no change to streak
                pass
            else:
                # Streak broken
                stats.current_streak = 1
        
        if stats.current_streak > stats.longest_streak:
            stats.longest_streak = stats.current_streak
    
    def _check_achievements(self, user_id: int) -> List[models.UserAchievement]:
        """Check and unlock new achievements for user"""
        newly_unlocked = []
        stats = self.get_user_stats(user_id)
        
        # Get all active achievements
        achievements = self.db.query(models.Achievement).filter(models.Achievement.is_active == True).all()
        
        for achievement in achievements:
            # Check if user already has this achievement
            existing = self.db.query(models.UserAchievement).filter(
                and_(
                    models.UserAchievement.user_id == user_id,
                    models.UserAchievement.achievement_id == achievement.id
                )
            ).first()
            
            if existing:
                continue
            
            # Check if achievement criteria is met
            if self._is_achievement_unlocked(user_id, achievement, stats):
                user_achievement = models.UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    progress=1.0
                )
                self.db.add(user_achievement)
                newly_unlocked.append(user_achievement)
                
                # Add XP reward
                stats.total_xp += achievement.xp_reward
                stats.achievements_unlocked += 1
                
                # Update level based on XP
                stats.current_level = self._calculate_level(stats.total_xp)
        
        self.db.commit()
        return newly_unlocked
    
    def _is_achievement_unlocked(self, user_id: int, achievement: models.Achievement, stats: models.UserStats) -> bool:
        """Check if achievement criteria is met"""
        try:
            criteria = json.loads(achievement.criteria) if achievement.criteria else {}
        except:
            criteria = {}
        
        if achievement.category == "species_count":
            target_count = criteria.get("count", 1)
            return stats.unique_species >= target_count
        
        elif achievement.category == "first_bird":
            return stats.unique_species >= 1
        
        elif achievement.category == "sighting_count":
            target_count = criteria.get("count", 1)
            return stats.total_sightings >= target_count
        
        elif achievement.category == "streak":
            target_streak = criteria.get("days", 1)
            return stats.longest_streak >= target_streak
        
        elif achievement.category == "rare_species":
            # Check if user has sighted a rare species (high confidence, specific species)
            rare_species = criteria.get("species", [])
            if rare_species:
                user_birds = self.get_user_collection(user_id)
                user_species = [bird.species_name for bird in user_birds]
                return any(species in user_species for species in rare_species)
        
        return False
    
    def _calculate_achievement_progress(self, user_id: int, achievement: models.Achievement) -> float:
        """Calculate progress towards an achievement (0.0 to 1.0)"""
        try:
            criteria = json.loads(achievement.criteria) if achievement.criteria else {}
        except:
            criteria = {}
        
        stats = self.get_user_stats(user_id)
        
        if achievement.category == "species_count":
            target_count = criteria.get("count", 1)
            return min(1.0, stats.unique_species / target_count)
        
        elif achievement.category == "sighting_count":
            target_count = criteria.get("count", 1)
            return min(1.0, stats.total_sightings / target_count)
        
        elif achievement.category == "streak":
            target_streak = criteria.get("days", 1)
            return min(1.0, stats.longest_streak / target_streak)
        
        elif achievement.category in ["first_bird", "rare_species"]:
            return 1.0 if self._is_achievement_unlocked(user_id, achievement, stats) else 0.0
        
        return 0.0
    
    def _calculate_level(self, total_xp: int) -> int:
        """Calculate user level based on total XP"""
        # Simple level calculation: level = sqrt(xp / 100) + 1
        import math
        return int(math.sqrt(total_xp / 100)) + 1
    
    def create_default_achievements(self):
        """Create default achievements if they don't exist"""
        default_achievements = [
            {
                "name": "First Flight",
                "description": "Identify your first bird species",
                "category": "first_bird",
                "criteria": "{}",
                "xp_reward": 100,
                "icon": "first_bird"
            },
            {
                "name": "Novice Birder",
                "description": "Identify 5 different bird species",
                "category": "species_count",
                "criteria": '{"count": 5}',
                "xp_reward": 250,
                "icon": "novice"
            },
            {
                "name": "Experienced Birder",
                "description": "Identify 25 different bird species",
                "category": "species_count",
                "criteria": '{"count": 25}',
                "xp_reward": 500,
                "icon": "experienced"
            },
            {
                "name": "Expert Birder",
                "description": "Identify 50 different bird species",
                "category": "species_count",
                "criteria": '{"count": 50}',
                "xp_reward": 1000,
                "icon": "expert"
            },
            {
                "name": "Master Birder",
                "description": "Identify 100 different bird species",
                "category": "species_count",
                "criteria": '{"count": 100}',
                "xp_reward": 2000,
                "icon": "master"
            },
            {
                "name": "Active Observer",
                "description": "Record 50 bird sightings",
                "category": "sighting_count",
                "criteria": '{"count": 50}',
                "xp_reward": 300,
                "icon": "active"
            },
            {
                "name": "Dedicated Watcher",
                "description": "Record sightings for 7 consecutive days",
                "category": "streak",
                "criteria": '{"days": 7}',
                "xp_reward": 400,
                "icon": "streak_7"
            },
            {
                "name": "Committed Birder",
                "description": "Record sightings for 30 consecutive days",
                "category": "streak",
                "criteria": '{"days": 30}',
                "xp_reward": 1000,
                "icon": "streak_30"
            }
        ]
        
        for achievement_data in default_achievements:
            existing = self.db.query(models.Achievement).filter(
                models.Achievement.name == achievement_data["name"]
            ).first()
            
            if not existing:
                achievement = models.Achievement(**achievement_data)
                self.db.add(achievement)
        
        self.db.commit()