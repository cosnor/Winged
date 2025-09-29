from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.species import Species, UserSpecies, Collection, RarityLevel


class SpeciesRepository(ABC):
    """Abstract repository for Species entity."""
    
    @abstractmethod
    async def get_by_id(self, species_id: int) -> Optional[Species]:
        """Get species by ID."""
        pass
    
    @abstractmethod
    async def get_by_scientific_name(self, scientific_name: str) -> Optional[Species]:
        """Get species by scientific name."""
        pass
    
    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Species]:
        """Get all species with pagination."""
        pass
    
    @abstractmethod
    async def get_by_rarity(self, rarity_level: RarityLevel) -> List[Species]:
        """Get species by rarity level."""
        pass
    
    @abstractmethod
    async def search_by_name(self, query: str, limit: int = 20) -> List[Species]:
        """Search species by common or scientific name."""
        pass
    
    @abstractmethod
    async def create(self, species: Species) -> Species:
        """Create a new species."""
        pass
    
    @abstractmethod
    async def update(self, species: Species) -> Species:
        """Update an existing species."""
        pass
    
    @abstractmethod
    async def delete(self, species_id: int) -> bool:
        """Delete a species."""
        pass


class UserSpeciesRepository(ABC):
    """Abstract repository for UserSpecies entity."""
    
    @abstractmethod
    async def get_by_id(self, user_species_id: int) -> Optional[UserSpecies]:
        """Get user species by ID."""
        pass
    
    @abstractmethod
    async def get_user_species(self, user_id: str, limit: int = 100, offset: int = 0) -> List[UserSpecies]:
        """Get all species discovered by a user."""
        pass
    
    @abstractmethod
    async def get_user_species_by_rarity(self, user_id: str, rarity_level: RarityLevel) -> List[UserSpecies]:
        """Get user's species filtered by rarity."""
        pass
    
    @abstractmethod
    async def has_user_discovered_species(self, user_id: str, species_id: int) -> bool:
        """Check if user has already discovered a species."""
        pass
    
    @abstractmethod
    async def get_user_discovery_count(self, user_id: str) -> int:
        """Get total number of species discovered by user."""
        pass
    
    @abstractmethod
    async def get_user_discoveries_by_date_range(
        self, 
        user_id: str, 
        start_date: str, 
        end_date: str
    ) -> List[UserSpecies]:
        """Get user discoveries within date range."""
        pass
    
    @abstractmethod
    async def get_recent_discoveries(self, user_id: str, days: int = 7) -> List[UserSpecies]:
        """Get user's recent discoveries."""
        pass
    
    @abstractmethod
    async def create(self, user_species: UserSpecies) -> UserSpecies:
        """Create a new user species discovery."""
        pass
    
    @abstractmethod
    async def update(self, user_species: UserSpecies) -> UserSpecies:
        """Update an existing user species."""
        pass
    
    @abstractmethod
    async def delete(self, user_species_id: int) -> bool:
        """Delete a user species discovery."""
        pass


class CollectionRepository(ABC):
    """Abstract repository for Collection entity."""
    
    @abstractmethod
    async def get_by_id(self, collection_id: int) -> Optional[Collection]:
        """Get collection by ID."""
        pass
    
    @abstractmethod
    async def get_system_collections(self) -> List[Collection]:
        """Get all system-defined collections."""
        pass
    
    @abstractmethod
    async def get_user_collections(self, user_id: str) -> List[Collection]:
        """Get collections created by a user."""
        pass
    
    @abstractmethod
    async def get_all_collections(self, limit: int = 50, offset: int = 0) -> List[Collection]:
        """Get all collections with pagination."""
        pass
    
    @abstractmethod
    async def create(self, collection: Collection) -> Collection:
        """Create a new collection."""
        pass
    
    @abstractmethod
    async def update(self, collection: Collection) -> Collection:
        """Update an existing collection."""
        pass
    
    @abstractmethod
    async def delete(self, collection_id: int) -> bool:
        """Delete a collection."""
        pass
    
    @abstractmethod
    async def add_species_to_collection(self, collection_id: int, species_id: int) -> bool:
        """Add a species to a collection."""
        pass
    
    @abstractmethod
    async def remove_species_from_collection(self, collection_id: int, species_id: int) -> bool:
        """Remove a species from a collection."""
        pass