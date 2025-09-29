from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from ...domain.entities.achievement import Achievement, UserAchievement, UserProgress, AchievementType, AchievementTier
from ...domain.repositories.achievement_repository import AchievementRepository, UserAchievementRepository, UserProgressRepository
from .models import AchievementModel, UserAchievementModel, UserProgressModel
from datetime import datetime


class SQLAlchemyAchievementRepository(AchievementRepository):
    """SQLAlchemy implementation of AchievementRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, achievement_id: int) -> Optional[Achievement]:
        """Get achievement by ID."""
        result = await self.session.execute(
            select(AchievementModel).where(AchievementModel.id == achievement_id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_all(self, include_hidden: bool = False) -> List[Achievement]:
        """Get all achievements."""
        query = select(AchievementModel)
        if not include_hidden:
            query = query.where(AchievementModel.is_hidden == False)
        
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_type(self, achievement_type: AchievementType) -> List[Achievement]:
        """Get achievements by type."""
        result = await self.session.execute(
            select(AchievementModel).where(AchievementModel.achievement_type == achievement_type.value)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_tier(self, tier: AchievementTier) -> List[Achievement]:
        """Get achievements by tier."""
        result = await self.session.execute(
            select(AchievementModel).where(AchievementModel.tier == tier.value)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def create(self, achievement: Achievement) -> Achievement:
        """Create a new achievement."""
        model = self._entity_to_model(achievement)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def update(self, achievement: Achievement) -> Achievement:
        """Update an existing achievement."""
        result = await self.session.execute(
            select(AchievementModel).where(AchievementModel.id == achievement.id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Achievement with id {achievement.id} not found")
        
        # Update fields
        model.name = achievement.name
        model.description = achievement.description
        model.achievement_type = achievement.achievement_type.value
        model.tier = achievement.tier.value
        model.icon = achievement.icon
        model.points = achievement.points
        model.requirement_value = achievement.requirement_value
        model.requirement_description = achievement.requirement_description
        model.is_hidden = achievement.is_hidden
        model.is_repeatable = achievement.is_repeatable
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, achievement_id: int) -> bool:
        """Delete an achievement."""
        result = await self.session.execute(
            select(AchievementModel).where(AchievementModel.id == achievement_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    def _model_to_entity(self, model: AchievementModel) -> Achievement:
        """Convert SQLAlchemy model to domain entity."""
        return Achievement(
            id=model.id,
            name=model.name,
            description=model.description,
            achievement_type=AchievementType(model.achievement_type),
            tier=AchievementTier(model.tier),
            icon=model.icon,
            points=model.points,
            requirement_value=model.requirement_value,
            requirement_description=model.requirement_description,
            is_hidden=model.is_hidden,
            is_repeatable=model.is_repeatable,
            created_at=model.created_at
        )
    
    def _entity_to_model(self, entity: Achievement) -> AchievementModel:
        """Convert domain entity to SQLAlchemy model."""
        return AchievementModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            achievement_type=entity.achievement_type.value,
            tier=entity.tier.value,
            icon=entity.icon,
            points=entity.points,
            requirement_value=entity.requirement_value,
            requirement_description=entity.requirement_description,
            is_hidden=entity.is_hidden,
            is_repeatable=entity.is_repeatable,
            created_at=entity.created_at
        )


class SQLAlchemyUserAchievementRepository(UserAchievementRepository):
    """SQLAlchemy implementation of UserAchievementRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_achievement_id: int) -> Optional[UserAchievement]:
        """Get user achievement by ID."""
        result = await self.session.execute(
            select(UserAchievementModel).where(UserAchievementModel.id == user_achievement_id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """Get all achievements for a user."""
        result = await self.session.execute(
            select(UserAchievementModel)
            .where(UserAchievementModel.user_id == user_id)
            .order_by(desc(UserAchievementModel.unlocked_at))
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_user_completed_achievements(self, user_id: str) -> List[UserAchievement]:
        """Get completed achievements for a user."""
        result = await self.session.execute(
            select(UserAchievementModel)
            .where(
                and_(
                    UserAchievementModel.user_id == user_id,
                    UserAchievementModel.is_completed == True
                )
            )
            .order_by(desc(UserAchievementModel.completion_date))
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_user_in_progress_achievements(self, user_id: str) -> List[UserAchievement]:
        """Get in-progress achievements for a user."""
        result = await self.session.execute(
            select(UserAchievementModel)
            .where(
                and_(
                    UserAchievementModel.user_id == user_id,
                    UserAchievementModel.is_completed == False
                )
            )
            .order_by(desc(UserAchievementModel.unlocked_at))
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def has_user_unlocked_achievement(self, user_id: str, achievement_id: int) -> bool:
        """Check if user has unlocked a specific achievement."""
        result = await self.session.execute(
            select(UserAchievementModel).where(
                and_(
                    UserAchievementModel.user_id == user_id,
                    UserAchievementModel.achievement_id == achievement_id
                )
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def get_user_achievement_progress(
        self, 
        user_id: str, 
        achievement_id: int
    ) -> Optional[UserAchievement]:
        """Get user's progress on a specific achievement."""
        result = await self.session.execute(
            select(UserAchievementModel).where(
                and_(
                    UserAchievementModel.user_id == user_id,
                    UserAchievementModel.achievement_id == achievement_id
                )
            )
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def create(self, user_achievement: UserAchievement) -> UserAchievement:
        """Create a new user achievement."""
        model = self._entity_to_model(user_achievement)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def update(self, user_achievement: UserAchievement) -> UserAchievement:
        """Update user achievement progress."""
        result = await self.session.execute(
            select(UserAchievementModel).where(UserAchievementModel.id == user_achievement.id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"UserAchievement with id {user_achievement.id} not found")
        
        # Update fields
        model.progress_value = user_achievement.progress_value
        model.is_completed = user_achievement.is_completed
        model.completion_date = user_achievement.completion_date
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, user_achievement_id: int) -> bool:
        """Delete a user achievement."""
        result = await self.session.execute(
            select(UserAchievementModel).where(UserAchievementModel.id == user_achievement_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    def _model_to_entity(self, model: UserAchievementModel) -> UserAchievement:
        """Convert SQLAlchemy model to domain entity."""
        return UserAchievement(
            id=model.id,
            user_id=model.user_id,
            achievement_id=model.achievement_id,
            unlocked_at=model.unlocked_at,
            progress_value=model.progress_value,
            is_completed=model.is_completed,
            completion_date=model.completion_date,
            created_at=model.created_at
        )
    
    def _entity_to_model(self, entity: UserAchievement) -> UserAchievementModel:
        """Convert domain entity to SQLAlchemy model."""
        return UserAchievementModel(
            id=entity.id,
            user_id=entity.user_id,
            achievement_id=entity.achievement_id,
            unlocked_at=entity.unlocked_at,
            progress_value=entity.progress_value,
            is_completed=entity.is_completed,
            completion_date=entity.completion_date,
            created_at=entity.created_at
        )


class SQLAlchemyUserProgressRepository(UserProgressRepository):
    """SQLAlchemy implementation of UserProgressRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_user_id(self, user_id: str) -> Optional[UserProgress]:
        """Get user progress by user ID."""
        result = await self.session.execute(
            select(UserProgressModel).where(UserProgressModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_leaderboard(self, limit: int = 10, metric: str = "total_points") -> List[UserProgress]:
        """Get leaderboard based on specified metric."""
        # Map metric names to model attributes
        metric_map = {
            "total_points": UserProgressModel.total_points,
            "total_species_discovered": UserProgressModel.total_species_discovered,
            "achievements_unlocked": UserProgressModel.achievements_unlocked,
            "current_streak_days": UserProgressModel.current_streak_days,
            "longest_streak_days": UserProgressModel.longest_streak_days,
            "rare_species_count": UserProgressModel.rare_species_count
        }
        
        order_column = metric_map.get(metric, UserProgressModel.total_points)
        
        result = await self.session.execute(
            select(UserProgressModel)
            .order_by(desc(order_column))
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_users_by_streak(self, min_streak_days: int) -> List[UserProgress]:
        """Get users with streak above minimum."""
        result = await self.session.execute(
            select(UserProgressModel)
            .where(UserProgressModel.current_streak_days >= min_streak_days)
            .order_by(desc(UserProgressModel.current_streak_days))
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def create(self, user_progress: UserProgress) -> UserProgress:
        """Create new user progress record."""
        model = self._entity_to_model(user_progress)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def update(self, user_progress: UserProgress) -> UserProgress:
        """Update user progress."""
        result = await self.session.execute(
            select(UserProgressModel).where(UserProgressModel.user_id == user_progress.user_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"UserProgress for user {user_progress.user_id} not found")
        
        # Update all fields
        model.total_species_discovered = user_progress.total_species_discovered
        model.total_points = user_progress.total_points
        model.current_streak_days = user_progress.current_streak_days
        model.longest_streak_days = user_progress.longest_streak_days
        model.last_discovery_date = user_progress.last_discovery_date
        model.achievements_unlocked = user_progress.achievements_unlocked
        model.rare_species_count = user_progress.rare_species_count
        model.collections_completed = user_progress.collections_completed
        model.total_identifications = user_progress.total_identifications
        model.high_confidence_identifications = user_progress.high_confidence_identifications
        model.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, user_id: str) -> bool:
        """Delete user progress."""
        result = await self.session.execute(
            select(UserProgressModel).where(UserProgressModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    async def get_user_rank(self, user_id: str, metric: str = "total_points") -> Optional[int]:
        """Get user's rank in leaderboard for specified metric."""
        # Get user's progress
        user_progress = await self.get_by_user_id(user_id)
        if not user_progress:
            return None
        
        # Map metric names to model attributes and user values
        metric_map = {
            "total_points": (UserProgressModel.total_points, user_progress.total_points),
            "total_species_discovered": (UserProgressModel.total_species_discovered, user_progress.total_species_discovered),
            "achievements_unlocked": (UserProgressModel.achievements_unlocked, user_progress.achievements_unlocked),
            "current_streak_days": (UserProgressModel.current_streak_days, user_progress.current_streak_days),
            "longest_streak_days": (UserProgressModel.longest_streak_days, user_progress.longest_streak_days),
            "rare_species_count": (UserProgressModel.rare_species_count, user_progress.rare_species_count)
        }
        
        order_column, user_value = metric_map.get(metric, (UserProgressModel.total_points, user_progress.total_points))
        
        # Count users with better scores
        result = await self.session.execute(
            select(func.count(UserProgressModel.id))
            .where(order_column > user_value)
        )
        better_count = result.scalar() or 0
        
        return better_count + 1  # Rank is 1-based
    
    def _model_to_entity(self, model: UserProgressModel) -> UserProgress:
        """Convert SQLAlchemy model to domain entity."""
        return UserProgress(
            id=model.id,
            user_id=model.user_id,
            total_species_discovered=model.total_species_discovered,
            total_points=model.total_points,
            current_streak_days=model.current_streak_days,
            longest_streak_days=model.longest_streak_days,
            last_discovery_date=model.last_discovery_date,
            achievements_unlocked=model.achievements_unlocked,
            rare_species_count=model.rare_species_count,
            collections_completed=model.collections_completed,
            total_identifications=model.total_identifications,
            high_confidence_identifications=model.high_confidence_identifications,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: UserProgress) -> UserProgressModel:
        """Convert domain entity to SQLAlchemy model."""
        return UserProgressModel(
            id=entity.id,
            user_id=entity.user_id,
            total_species_discovered=entity.total_species_discovered,
            total_points=entity.total_points,
            current_streak_days=entity.current_streak_days,
            longest_streak_days=entity.longest_streak_days,
            last_discovery_date=entity.last_discovery_date,
            achievements_unlocked=entity.achievements_unlocked,
            rare_species_count=entity.rare_species_count,
            collections_completed=entity.collections_completed,
            total_identifications=entity.total_identifications,
            high_confidence_identifications=entity.high_confidence_identifications,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )