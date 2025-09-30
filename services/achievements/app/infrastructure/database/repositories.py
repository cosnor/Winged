from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ...application.interfaces.repositories import (
    AchievementRepository,
    UserAchievementRepository,
    BirdCollectionRepository,
    UserStatsRepository
)
from ...domain.entities.achievement import Achievement
from ...domain.entities.user_achievement import UserAchievement
from ...domain.entities.bird_collection import BirdCollection
from ...domain.entities.user_stats import UserStats
from ...domain.value_objects.achievement_criteria import AchievementCriteria
from ...domain.value_objects.location import Location
from .models import AchievementModel, UserAchievementModel, BirdCollectionModel, UserStatsModel


class SQLAlchemyAchievementRepository(AchievementRepository):
    """SQLAlchemy implementation of AchievementRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_active(self) -> List[Achievement]:
        """Get all active achievements"""
        models = self.db.query(AchievementModel).filter(AchievementModel.is_active == True).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_by_id(self, achievement_id: int) -> Optional[Achievement]:
        """Get achievement by ID"""
        model = self.db.query(AchievementModel).filter(AchievementModel.id == achievement_id).first()
        return self._model_to_entity(model) if model else None
    
    def create(self, achievement: Achievement) -> Achievement:
        """Create a new achievement"""
        model = self._entity_to_model(achievement)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, achievement: Achievement) -> Achievement:
        """Update an existing achievement"""
        model = self.db.query(AchievementModel).filter(AchievementModel.id == achievement.id).first()
        if model:
            model.name = achievement.name
            model.description = achievement.description
            model.category = achievement.category
            model.criteria = achievement.criteria.to_json()
            model.xp_reward = achievement.xp_reward
            model.icon = achievement.icon
            model.is_active = achievement.is_active
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)
        raise ValueError(f"Achievement with id {achievement.id} not found")
    
    def _model_to_entity(self, model: AchievementModel) -> Achievement:
        """Convert SQLAlchemy model to domain entity"""
        criteria = AchievementCriteria.from_json(model.criteria)
        return Achievement(
            id=model.id,
            name=model.name,
            description=model.description,
            category=model.category,
            criteria=criteria,
            xp_reward=model.xp_reward,
            icon=model.icon,
            is_active=model.is_active,
            created_at=model.created_at
        )
    
    def _entity_to_model(self, entity: Achievement) -> AchievementModel:
        """Convert domain entity to SQLAlchemy model"""
        return AchievementModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            category=entity.category,
            criteria=entity.criteria.to_json(),
            xp_reward=entity.xp_reward,
            icon=entity.icon,
            is_active=entity.is_active,
            created_at=entity.created_at
        )


class SQLAlchemyUserAchievementRepository(UserAchievementRepository):
    """SQLAlchemy implementation of UserAchievementRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_user_id(self, user_id: int) -> List[UserAchievement]:
        """Get all achievements for a user"""
        models = self.db.query(UserAchievementModel).filter(
            UserAchievementModel.user_id == user_id
        ).join(AchievementModel).order_by(UserAchievementModel.unlocked_at.desc()).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_by_user_and_achievement(self, user_id: int, achievement_id: int) -> Optional[UserAchievement]:
        """Get specific user achievement"""
        model = self.db.query(UserAchievementModel).filter(
            and_(
                UserAchievementModel.user_id == user_id,
                UserAchievementModel.achievement_id == achievement_id
            )
        ).first()
        return self._model_to_entity(model) if model else None
    
    def create(self, user_achievement: UserAchievement) -> UserAchievement:
        """Create a new user achievement"""
        model = self._entity_to_model(user_achievement)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, user_achievement: UserAchievement) -> UserAchievement:
        """Update user achievement progress"""
        model = self.db.query(UserAchievementModel).filter(
            UserAchievementModel.id == user_achievement.id
        ).first()
        if model:
            model.progress = user_achievement.progress
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)
        raise ValueError(f"UserAchievement with id {user_achievement.id} not found")
    
    def _model_to_entity(self, model: UserAchievementModel) -> UserAchievement:
        """Convert SQLAlchemy model to domain entity"""
        achievement = None
        if model.achievement:
            criteria = AchievementCriteria.from_json(model.achievement.criteria)
            achievement = Achievement(
                id=model.achievement.id,
                name=model.achievement.name,
                description=model.achievement.description,
                category=model.achievement.category,
                criteria=criteria,
                xp_reward=model.achievement.xp_reward,
                icon=model.achievement.icon,
                is_active=model.achievement.is_active,
                created_at=model.achievement.created_at
            )
        
        return UserAchievement(
            id=model.id,
            user_id=model.user_id,
            achievement_id=model.achievement_id,
            unlocked_at=model.unlocked_at,
            progress=model.progress,
            achievement=achievement
        )
    
    def _entity_to_model(self, entity: UserAchievement) -> UserAchievementModel:
        """Convert domain entity to SQLAlchemy model"""
        return UserAchievementModel(
            id=entity.id,
            user_id=entity.user_id,
            achievement_id=entity.achievement_id,
            unlocked_at=entity.unlocked_at,
            progress=entity.progress
        )


class SQLAlchemyBirdCollectionRepository(BirdCollectionRepository):
    """SQLAlchemy implementation of BirdCollectionRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_user_id(self, user_id: int) -> List[BirdCollection]:
        """Get user's bird collection"""
        models = self.db.query(BirdCollectionModel).filter(
            BirdCollectionModel.user_id == user_id
        ).order_by(BirdCollectionModel.first_sighted_at.desc()).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_by_user_and_species(self, user_id: int, species_name: str) -> Optional[BirdCollection]:
        """Get specific bird entry for user"""
        model = self.db.query(BirdCollectionModel).filter(
            and_(
                BirdCollectionModel.user_id == user_id,
                BirdCollectionModel.species_name == species_name
            )
        ).first()
        return self._model_to_entity(model) if model else None
    
    def create(self, bird_collection: BirdCollection) -> BirdCollection:
        """Create a new bird collection entry"""
        model = self._entity_to_model(bird_collection)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, bird_collection: BirdCollection) -> BirdCollection:
        """Update bird collection entry"""
        model = self.db.query(BirdCollectionModel).filter(
            BirdCollectionModel.id == bird_collection.id
        ).first()
        if model:
            model.sighting_count = bird_collection.sighting_count
            model.last_sighted_at = bird_collection.last_sighted_at
            model.confidence_score = bird_collection.confidence_score
            if bird_collection.location:
                model.location_lat = bird_collection.location.latitude
                model.location_lon = bird_collection.location.longitude
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)
        raise ValueError(f"BirdCollection with id {bird_collection.id} not found")
    
    def get_all_species(self) -> List[str]:
        """Get list of all species that have been sighted"""
        species = self.db.query(BirdCollectionModel.species_name).distinct().all()
        return [s[0] for s in species]
    
    def get_users_with_species(self, species_name: str) -> List[int]:
        """Get list of user IDs who have sighted a specific species"""
        users = self.db.query(BirdCollectionModel.user_id).filter(
            BirdCollectionModel.species_name == species_name
        ).distinct().all()
        return [u[0] for u in users]
    
    def _model_to_entity(self, model: BirdCollectionModel) -> BirdCollection:
        """Convert SQLAlchemy model to domain entity"""
        location = None
        if model.location_lat is not None and model.location_lon is not None:
            location = Location(latitude=model.location_lat, longitude=model.location_lon)
        
        return BirdCollection(
            id=model.id,
            user_id=model.user_id,
            species_name=model.species_name,
            common_name=model.common_name,
            first_sighted_at=model.first_sighted_at,
            sighting_count=model.sighting_count,
            last_sighted_at=model.last_sighted_at,
            confidence_score=model.confidence_score,
            location=location
        )
    
    def _entity_to_model(self, entity: BirdCollection) -> BirdCollectionModel:
        """Convert domain entity to SQLAlchemy model"""
        location_lat = entity.location.latitude if entity.location else None
        location_lon = entity.location.longitude if entity.location else None
        
        return BirdCollectionModel(
            id=entity.id,
            user_id=entity.user_id,
            species_name=entity.species_name,
            common_name=entity.common_name,
            first_sighted_at=entity.first_sighted_at,
            sighting_count=entity.sighting_count,
            last_sighted_at=entity.last_sighted_at,
            confidence_score=entity.confidence_score,
            location_lat=location_lat,
            location_lon=location_lon
        )


class SQLAlchemyUserStatsRepository(UserStatsRepository):
    """SQLAlchemy implementation of UserStatsRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_user_id(self, user_id: int) -> Optional[UserStats]:
        """Get user statistics"""
        model = self.db.query(UserStatsModel).filter(UserStatsModel.user_id == user_id).first()
        return self._model_to_entity(model) if model else None
    
    def create(self, user_stats: UserStats) -> UserStats:
        """Create new user statistics"""
        model = self._entity_to_model(user_stats)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, user_stats: UserStats) -> UserStats:
        """Update user statistics"""
        model = self.db.query(UserStatsModel).filter(UserStatsModel.user_id == user_stats.user_id).first()
        if model:
            model.total_sightings = user_stats.total_sightings
            model.unique_species = user_stats.unique_species
            model.total_xp = user_stats.total_xp
            model.current_level = user_stats.current_level
            model.achievements_unlocked = user_stats.achievements_unlocked
            model.first_sighting_date = user_stats.first_sighting_date
            model.last_sighting_date = user_stats.last_sighting_date
            model.longest_streak = user_stats.longest_streak
            model.current_streak = user_stats.current_streak
            model.updated_at = user_stats.updated_at
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)
        raise ValueError(f"UserStats for user {user_stats.user_id} not found")
    
    def get_leaderboard_by_species(self, limit: int = 10) -> List[UserStats]:
        """Get leaderboard ordered by unique species count"""
        models = self.db.query(UserStatsModel).order_by(
            UserStatsModel.unique_species.desc()
        ).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_leaderboard_by_xp(self, limit: int = 10) -> List[UserStats]:
        """Get leaderboard ordered by total XP"""
        models = self.db.query(UserStatsModel).order_by(
            UserStatsModel.total_xp.desc()
        ).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    def _model_to_entity(self, model: UserStatsModel) -> UserStats:
        """Convert SQLAlchemy model to domain entity"""
        return UserStats(
            id=model.id,
            user_id=model.user_id,
            total_sightings=model.total_sightings,
            unique_species=model.unique_species,
            total_xp=model.total_xp,
            current_level=model.current_level,
            achievements_unlocked=model.achievements_unlocked,
            first_sighting_date=model.first_sighting_date,
            last_sighting_date=model.last_sighting_date,
            longest_streak=model.longest_streak,
            current_streak=model.current_streak,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: UserStats) -> UserStatsModel:
        """Convert domain entity to SQLAlchemy model"""
        return UserStatsModel(
            id=entity.id,
            user_id=entity.user_id,
            total_sightings=entity.total_sightings,
            unique_species=entity.unique_species,
            total_xp=entity.total_xp,
            current_level=entity.current_level,
            achievements_unlocked=entity.achievements_unlocked,
            first_sighting_date=entity.first_sighting_date,
            last_sighting_date=entity.last_sighting_date,
            longest_streak=entity.longest_streak,
            current_streak=entity.current_streak,
            updated_at=entity.updated_at
        )