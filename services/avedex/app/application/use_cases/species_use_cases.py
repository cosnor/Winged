from typing import List, Optional
from datetime import datetime
from ...domain.entities.species import Species, UserSpecies, Collection, RarityLevel
from ...domain.repositories.species_repository import SpeciesRepository, UserSpeciesRepository, CollectionRepository
from ...domain.services.gamification_service import GamificationService
from ..dtos.species_dto import (
    SpeciesDTO, UserSpeciesDTO, CollectionDTO, CollectionWithSpeciesDTO,
    UserCollectionProgressDTO, AddSpeciesRequest, SpeciesSearchRequest
)


class SpeciesUseCases:
    """Application use cases for species management."""
    
    def __init__(
        self,
        species_repo: SpeciesRepository,
        user_species_repo: UserSpeciesRepository,
        collection_repo: CollectionRepository,
        gamification_service: GamificationService
    ):
        self.species_repo = species_repo
        self.user_species_repo = user_species_repo
        self.collection_repo = collection_repo
        self.gamification_service = gamification_service
    
    async def add_species_to_user_collection(self, request: AddSpeciesRequest) -> UserSpeciesDTO:
        """Add a discovered species to user's collection."""
        
        # Check if user already discovered this species
        already_discovered = await self.user_species_repo.has_user_discovered_species(
            request.user_id, request.species_id
        )
        
        if already_discovered:
            raise ValueError("Species already discovered by user")
        
        # Get species details
        species = await self.species_repo.get_by_id(request.species_id)
        if not species:
            raise ValueError("Species not found")
        
        # Create user species record
        user_species = UserSpecies(
            id=None,
            user_id=request.user_id,
            species_id=request.species_id,
            discovered_at=datetime.utcnow(),
            location_lat=request.location_lat,
            location_lng=request.location_lng,
            location_name=request.location_name,
            confidence_score=request.confidence_score,
            photo_url=request.photo_url,
            audio_url=request.audio_url,
            notes=request.notes
        )
        
        # Save to repository
        saved_user_species = await self.user_species_repo.create(user_species)
        
        # Process gamification (achievements, progress)
        newly_unlocked_achievements = await self.gamification_service.process_species_discovery(
            request.user_id, species, saved_user_species
        )
        
        # Convert to DTO
        species_dto = self._species_to_dto(species)
        user_species_dto = self._user_species_to_dto(saved_user_species, species_dto)
        
        return user_species_dto
    
    async def get_user_collection(
        self, 
        user_id: str, 
        rarity_filter: Optional[str] = None,
        limit: int = 100, 
        offset: int = 0
    ) -> List[UserSpeciesDTO]:
        """Get user's discovered species collection."""
        
        if rarity_filter:
            try:
                rarity_level = RarityLevel(rarity_filter)
                user_species_list = await self.user_species_repo.get_user_species_by_rarity(
                    user_id, rarity_level
                )
            except ValueError:
                raise ValueError(f"Invalid rarity level: {rarity_filter}")
        else:
            user_species_list = await self.user_species_repo.get_user_species(
                user_id, limit, offset
            )
        
        # Get species details for each user species
        result = []
        for user_species in user_species_list:
            species = await self.species_repo.get_by_id(user_species.species_id)
            if species:
                species_dto = self._species_to_dto(species)
                user_species_dto = self._user_species_to_dto(user_species, species_dto)
                result.append(user_species_dto)
        
        return result
    
    async def get_species_details(self, species_id: int) -> Optional[SpeciesDTO]:
        """Get detailed information about a specific species."""
        species = await self.species_repo.get_by_id(species_id)
        if not species:
            return None
        
        return self._species_to_dto(species)
    
    async def search_species(self, request: SpeciesSearchRequest) -> List[SpeciesDTO]:
        """Search for species by name or other criteria."""
        species_list = await self.species_repo.search_by_name(request.query, request.limit)
        
        # Apply additional filters
        if request.rarity_level:
            try:
                rarity_level = RarityLevel(request.rarity_level)
                species_list = [s for s in species_list if s.rarity_level == rarity_level]
            except ValueError:
                pass  # Ignore invalid rarity level
        
        if request.family:
            species_list = [s for s in species_list if s.family.lower() == request.family.lower()]
        
        return [self._species_to_dto(species) for species in species_list]
    
    async def get_collection_details(self, collection_id: int) -> Optional[CollectionWithSpeciesDTO]:
        """Get collection with all its species."""
        collection = await self.collection_repo.get_by_id(collection_id)
        if not collection:
            return None
        
        # Get species details
        species_list = []
        for species_id in collection.species_ids:
            species = await self.species_repo.get_by_id(species_id)
            if species:
                species_list.append(self._species_to_dto(species))
        
        return CollectionWithSpeciesDTO(
            id=collection.id,
            name=collection.name,
            description=collection.description,
            icon=collection.icon,
            color=collection.color,
            species=species_list,
            is_system_collection=collection.is_system_collection,
            created_by=collection.created_by,
            created_at=collection.created_at,
            updated_at=collection.updated_at
        )
    
    async def get_user_collection_progress(
        self, 
        user_id: str, 
        collection_id: int
    ) -> Optional[UserCollectionProgressDTO]:
        """Get user's progress on a specific collection."""
        collection = await self.collection_repo.get_by_id(collection_id)
        if not collection:
            return None
        
        # Get user's discovered species in this collection
        user_species_list = await self.user_species_repo.get_user_species(user_id)
        user_species_ids = {us.species_id for us in user_species_list}
        
        discovered_species = []
        missing_species = []
        
        for species_id in collection.species_ids:
            species = await self.species_repo.get_by_id(species_id)
            if not species:
                continue
            
            species_dto = self._species_to_dto(species)
            
            if species_id in user_species_ids:
                # Find the user species record
                user_species = next(us for us in user_species_list if us.species_id == species_id)
                user_species_dto = self._user_species_to_dto(user_species, species_dto)
                discovered_species.append(user_species_dto)
            else:
                missing_species.append(species_dto)
        
        total_species = len(collection.species_ids)
        discovered_count = len(discovered_species)
        completion_percentage = (discovered_count / total_species * 100) if total_species > 0 else 0
        
        collection_dto = CollectionDTO(
            id=collection.id,
            name=collection.name,
            description=collection.description,
            icon=collection.icon,
            color=collection.color,
            species_count=total_species,
            is_system_collection=collection.is_system_collection,
            created_by=collection.created_by,
            created_at=collection.created_at,
            updated_at=collection.updated_at
        )
        
        return UserCollectionProgressDTO(
            collection=collection_dto,
            total_species=total_species,
            discovered_species=discovered_count,
            completion_percentage=completion_percentage,
            discovered_species_list=discovered_species,
            missing_species=missing_species
        )
    
    async def get_all_collections(self) -> List[CollectionDTO]:
        """Get all available collections."""
        collections = await self.collection_repo.get_all_collections()
        return [self._collection_to_dto(collection) for collection in collections]
    
    def _species_to_dto(self, species: Species) -> SpeciesDTO:
        """Convert Species entity to DTO."""
        return SpeciesDTO(
            id=species.id,
            scientific_name=species.scientific_name,
            common_name=species.common_name,
            common_name_es=species.common_name_es,
            family=species.family,
            description=species.description,
            habitat=species.habitat,
            rarity_level=species.rarity_level.value,
            conservation_status=species.conservation_status,
            image_url=species.image_url,
            audio_url=species.audio_url,
            size_cm=species.size_cm,
            weight_g=species.weight_g,
            wingspan_cm=species.wingspan_cm,
            rarity_points=species.rarity_points,
            created_at=species.created_at,
            updated_at=species.updated_at
        )
    
    def _user_species_to_dto(self, user_species: UserSpecies, species_dto: SpeciesDTO) -> UserSpeciesDTO:
        """Convert UserSpecies entity to DTO."""
        return UserSpeciesDTO(
            id=user_species.id,
            user_id=user_species.user_id,
            species_id=user_species.species_id,
            species=species_dto,
            discovered_at=user_species.discovered_at,
            location_lat=user_species.location_lat,
            location_lng=user_species.location_lng,
            location_name=user_species.location_name,
            confidence_score=user_species.confidence_score,
            photo_url=user_species.photo_url,
            audio_url=user_species.audio_url,
            notes=user_species.notes,
            verified=user_species.verified,
            verification_source=user_species.verification_source,
            is_high_confidence=user_species.is_high_confidence,
            created_at=user_species.created_at
        )
    
    def _collection_to_dto(self, collection: Collection) -> CollectionDTO:
        """Convert Collection entity to DTO."""
        return CollectionDTO(
            id=collection.id,
            name=collection.name,
            description=collection.description,
            icon=collection.icon,
            color=collection.color,
            species_count=collection.species_count,
            is_system_collection=collection.is_system_collection,
            created_by=collection.created_by,
            created_at=collection.created_at,
            updated_at=collection.updated_at
        )