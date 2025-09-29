from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from ...domain.entities.species import Species, UserSpecies, Collection, RarityLevel
from ...domain.repositories.species_repository import SpeciesRepository, UserSpeciesRepository, CollectionRepository
from .models import SpeciesModel, UserSpeciesModel, CollectionModel
from datetime import datetime, timedelta


class SQLAlchemySpeciesRepository(SpeciesRepository):
    """SQLAlchemy implementation of SpeciesRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, species_id: int) -> Optional[Species]:
        """Get species by ID."""
        result = await self.session.execute(
            select(SpeciesModel).where(SpeciesModel.id == species_id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_by_scientific_name(self, scientific_name: str) -> Optional[Species]:
        """Get species by scientific name."""
        result = await self.session.execute(
            select(SpeciesModel).where(SpeciesModel.scientific_name == scientific_name)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Species]:
        """Get all species with pagination."""
        result = await self.session.execute(
            select(SpeciesModel).offset(offset).limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_rarity(self, rarity_level: RarityLevel) -> List[Species]:
        """Get species by rarity level."""
        result = await self.session.execute(
            select(SpeciesModel).where(SpeciesModel.rarity_level == rarity_level.value)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def search_by_name(self, query: str, limit: int = 20) -> List[Species]:
        """Search species by common or scientific name."""
        search_term = f"%{query}%"
        result = await self.session.execute(
            select(SpeciesModel).where(
                or_(
                    SpeciesModel.common_name.ilike(search_term),
                    SpeciesModel.common_name_es.ilike(search_term),
                    SpeciesModel.scientific_name.ilike(search_term)
                )
            ).limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def create(self, species: Species) -> Species:
        """Create a new species."""
        model = self._entity_to_model(species)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def update(self, species: Species) -> Species:
        """Update an existing species."""
        result = await self.session.execute(
            select(SpeciesModel).where(SpeciesModel.id == species.id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Species with id {species.id} not found")
        
        # Update fields
        model.scientific_name = species.scientific_name
        model.common_name = species.common_name
        model.common_name_es = species.common_name_es
        model.family = species.family
        model.description = species.description
        model.habitat = species.habitat
        model.rarity_level = species.rarity_level.value
        model.conservation_status = species.conservation_status
        model.image_url = species.image_url
        model.audio_url = species.audio_url
        model.size_cm = species.size_cm
        model.weight_g = species.weight_g
        model.wingspan_cm = species.wingspan_cm
        model.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, species_id: int) -> bool:
        """Delete a species."""
        result = await self.session.execute(
            select(SpeciesModel).where(SpeciesModel.id == species_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    def _model_to_entity(self, model: SpeciesModel) -> Species:
        """Convert SQLAlchemy model to domain entity."""
        return Species(
            id=model.id,
            scientific_name=model.scientific_name,
            common_name=model.common_name,
            common_name_es=model.common_name_es,
            family=model.family,
            description=model.description,
            habitat=model.habitat,
            rarity_level=RarityLevel(model.rarity_level),
            conservation_status=model.conservation_status,
            image_url=model.image_url,
            audio_url=model.audio_url,
            size_cm=model.size_cm,
            weight_g=model.weight_g,
            wingspan_cm=model.wingspan_cm,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Species) -> SpeciesModel:
        """Convert domain entity to SQLAlchemy model."""
        return SpeciesModel(
            id=entity.id,
            scientific_name=entity.scientific_name,
            common_name=entity.common_name,
            common_name_es=entity.common_name_es,
            family=entity.family,
            description=entity.description,
            habitat=entity.habitat,
            rarity_level=entity.rarity_level.value,
            conservation_status=entity.conservation_status,
            image_url=entity.image_url,
            audio_url=entity.audio_url,
            size_cm=entity.size_cm,
            weight_g=entity.weight_g,
            wingspan_cm=entity.wingspan_cm,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


class SQLAlchemyUserSpeciesRepository(UserSpeciesRepository):
    """SQLAlchemy implementation of UserSpeciesRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_species_id: int) -> Optional[UserSpecies]:
        """Get user species by ID."""
        result = await self.session.execute(
            select(UserSpeciesModel).where(UserSpeciesModel.id == user_species_id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_user_species(self, user_id: str, limit: int = 100, offset: int = 0) -> List[UserSpecies]:
        """Get all species discovered by a user."""
        result = await self.session.execute(
            select(UserSpeciesModel)
            .where(UserSpeciesModel.user_id == user_id)
            .order_by(UserSpeciesModel.discovered_at.desc())
            .offset(offset)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_user_species_by_rarity(self, user_id: str, rarity_level: RarityLevel) -> List[UserSpecies]:
        """Get user's species filtered by rarity."""
        result = await self.session.execute(
            select(UserSpeciesModel)
            .join(SpeciesModel)
            .where(
                and_(
                    UserSpeciesModel.user_id == user_id,
                    SpeciesModel.rarity_level == rarity_level.value
                )
            )
            .order_by(UserSpeciesModel.discovered_at.desc())
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def has_user_discovered_species(self, user_id: str, species_id: int) -> bool:
        """Check if user has already discovered a species."""
        result = await self.session.execute(
            select(UserSpeciesModel).where(
                and_(
                    UserSpeciesModel.user_id == user_id,
                    UserSpeciesModel.species_id == species_id
                )
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def get_user_discovery_count(self, user_id: str) -> int:
        """Get total number of species discovered by user."""
        result = await self.session.execute(
            select(func.count(UserSpeciesModel.id)).where(UserSpeciesModel.user_id == user_id)
        )
        return result.scalar() or 0
    
    async def get_user_discoveries_by_date_range(
        self, 
        user_id: str, 
        start_date: str, 
        end_date: str
    ) -> List[UserSpecies]:
        """Get user discoveries within date range."""
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        result = await self.session.execute(
            select(UserSpeciesModel).where(
                and_(
                    UserSpeciesModel.user_id == user_id,
                    UserSpeciesModel.discovered_at >= start_dt,
                    UserSpeciesModel.discovered_at <= end_dt
                )
            ).order_by(UserSpeciesModel.discovered_at.desc())
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_recent_discoveries(self, user_id: str, days: int = 7) -> List[UserSpecies]:
        """Get user's recent discoveries."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = await self.session.execute(
            select(UserSpeciesModel).where(
                and_(
                    UserSpeciesModel.user_id == user_id,
                    UserSpeciesModel.discovered_at >= cutoff_date
                )
            ).order_by(UserSpeciesModel.discovered_at.desc())
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def create(self, user_species: UserSpecies) -> UserSpecies:
        """Create a new user species discovery."""
        model = self._entity_to_model(user_species)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def update(self, user_species: UserSpecies) -> UserSpecies:
        """Update an existing user species."""
        result = await self.session.execute(
            select(UserSpeciesModel).where(UserSpeciesModel.id == user_species.id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"UserSpecies with id {user_species.id} not found")
        
        # Update fields
        model.location_lat = user_species.location_lat
        model.location_lng = user_species.location_lng
        model.location_name = user_species.location_name
        model.confidence_score = user_species.confidence_score
        model.photo_url = user_species.photo_url
        model.audio_url = user_species.audio_url
        model.notes = user_species.notes
        model.verified = user_species.verified
        model.verification_source = user_species.verification_source
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, user_species_id: int) -> bool:
        """Delete a user species discovery."""
        result = await self.session.execute(
            select(UserSpeciesModel).where(UserSpeciesModel.id == user_species_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    def _model_to_entity(self, model: UserSpeciesModel) -> UserSpecies:
        """Convert SQLAlchemy model to domain entity."""
        return UserSpecies(
            id=model.id,
            user_id=model.user_id,
            species_id=model.species_id,
            discovered_at=model.discovered_at,
            location_lat=model.location_lat,
            location_lng=model.location_lng,
            location_name=model.location_name,
            confidence_score=model.confidence_score,
            photo_url=model.photo_url,
            audio_url=model.audio_url,
            notes=model.notes,
            verified=model.verified,
            verification_source=model.verification_source,
            created_at=model.created_at
        )
    
    def _entity_to_model(self, entity: UserSpecies) -> UserSpeciesModel:
        """Convert domain entity to SQLAlchemy model."""
        return UserSpeciesModel(
            id=entity.id,
            user_id=entity.user_id,
            species_id=entity.species_id,
            discovered_at=entity.discovered_at,
            location_lat=entity.location_lat,
            location_lng=entity.location_lng,
            location_name=entity.location_name,
            confidence_score=entity.confidence_score,
            photo_url=entity.photo_url,
            audio_url=entity.audio_url,
            notes=entity.notes,
            verified=entity.verified,
            verification_source=entity.verification_source,
            created_at=entity.created_at
        )


class SQLAlchemyCollectionRepository(CollectionRepository):
    """SQLAlchemy implementation of CollectionRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, collection_id: int) -> Optional[Collection]:
        """Get collection by ID."""
        result = await self.session.execute(
            select(CollectionModel).where(CollectionModel.id == collection_id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_system_collections(self) -> List[Collection]:
        """Get all system-defined collections."""
        result = await self.session.execute(
            select(CollectionModel).where(CollectionModel.is_system_collection == True)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_user_collections(self, user_id: str) -> List[Collection]:
        """Get collections created by a user."""
        result = await self.session.execute(
            select(CollectionModel).where(CollectionModel.created_by == user_id)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_all_collections(self, limit: int = 50, offset: int = 0) -> List[Collection]:
        """Get all collections with pagination."""
        result = await self.session.execute(
            select(CollectionModel).offset(offset).limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def create(self, collection: Collection) -> Collection:
        """Create a new collection."""
        model = self._entity_to_model(collection)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def update(self, collection: Collection) -> Collection:
        """Update an existing collection."""
        result = await self.session.execute(
            select(CollectionModel).where(CollectionModel.id == collection.id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Collection with id {collection.id} not found")
        
        # Update fields
        model.name = collection.name
        model.description = collection.description
        model.icon = collection.icon
        model.color = collection.color
        model.species_ids = collection.species_ids
        model.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, collection_id: int) -> bool:
        """Delete a collection."""
        result = await self.session.execute(
            select(CollectionModel).where(CollectionModel.id == collection_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    async def add_species_to_collection(self, collection_id: int, species_id: int) -> bool:
        """Add a species to a collection."""
        result = await self.session.execute(
            select(CollectionModel).where(CollectionModel.id == collection_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        if species_id not in model.species_ids:
            model.species_ids = model.species_ids + [species_id]
            model.updated_at = datetime.utcnow()
            await self.session.commit()
        
        return True
    
    async def remove_species_from_collection(self, collection_id: int, species_id: int) -> bool:
        """Remove a species from a collection."""
        result = await self.session.execute(
            select(CollectionModel).where(CollectionModel.id == collection_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        if species_id in model.species_ids:
            species_ids = model.species_ids.copy()
            species_ids.remove(species_id)
            model.species_ids = species_ids
            model.updated_at = datetime.utcnow()
            await self.session.commit()
        
        return True
    
    def _model_to_entity(self, model: CollectionModel) -> Collection:
        """Convert SQLAlchemy model to domain entity."""
        return Collection(
            id=model.id,
            name=model.name,
            description=model.description,
            icon=model.icon,
            color=model.color,
            species_ids=model.species_ids or [],
            is_system_collection=model.is_system_collection,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Collection) -> CollectionModel:
        """Convert domain entity to SQLAlchemy model."""
        return CollectionModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            icon=entity.icon,
            color=entity.color,
            species_ids=entity.species_ids,
            is_system_collection=entity.is_system_collection,
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )