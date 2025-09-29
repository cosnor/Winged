from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ...infrastructure.database.connection import get_database_session
from ...infrastructure.database.species_repository_impl import (
    SQLAlchemySpeciesRepository, SQLAlchemyUserSpeciesRepository, SQLAlchemyCollectionRepository
)
from ...infrastructure.database.achievement_repository_impl import (
    SQLAlchemyAchievementRepository, SQLAlchemyUserAchievementRepository, SQLAlchemyUserProgressRepository
)
from ...domain.services.gamification_service import GamificationService
from ...application.use_cases.species_use_cases import SpeciesUseCases
from ...application.dtos.species_dto import AddSpeciesRequest as AddSpeciesRequestDTO, SpeciesSearchRequest as SpeciesSearchRequestDTO
from ..schemas.species_schemas import (
    SpeciesResponse, UserSpeciesResponse, CollectionResponse, CollectionWithSpeciesResponse,
    UserCollectionProgressResponse, AddSpeciesRequest, SpeciesSearchRequest, RarityLevelSchema,
    BirdNetIdentificationRequest, BirdNetIdentificationResponse
)

router = APIRouter(prefix="/species", tags=["Species"])


async def get_species_use_cases(session: AsyncSession = Depends(get_database_session)) -> SpeciesUseCases:
    """Dependency to get SpeciesUseCases with all dependencies."""
    species_repo = SQLAlchemySpeciesRepository(session)
    user_species_repo = SQLAlchemyUserSpeciesRepository(session)
    collection_repo = SQLAlchemyCollectionRepository(session)
    
    # Achievement repositories for gamification
    achievement_repo = SQLAlchemyAchievementRepository(session)
    user_achievement_repo = SQLAlchemyUserAchievementRepository(session)
    user_progress_repo = SQLAlchemyUserProgressRepository(session)
    
    gamification_service = GamificationService(
        achievement_repo, user_achievement_repo, user_progress_repo, user_species_repo
    )
    
    return SpeciesUseCases(species_repo, user_species_repo, collection_repo, gamification_service)


@router.get("/", response_model=List[SpeciesResponse])
async def get_all_species(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get all species with pagination."""
    try:
        species_dtos = await use_cases.species_repo.get_all(limit, offset)
        return [SpeciesResponse(**dto.__dict__) for dto in [use_cases._species_to_dto(s) for s in species_dtos]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving species: {str(e)}")


@router.get("/search", response_model=List[SpeciesResponse])
async def search_species(
    query: str = Query(min_length=1, max_length=255),
    rarity_level: Optional[RarityLevelSchema] = Query(None),
    family: Optional[str] = Query(None, max_length=100),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Search for species by name or other criteria."""
    try:
        search_request = SpeciesSearchRequestDTO(
            query=query,
            rarity_level=rarity_level.value if rarity_level else None,
            family=family,
            limit=limit,
            offset=offset
        )
        species_dtos = await use_cases.search_species(search_request)
        return [SpeciesResponse(**dto.__dict__) for dto in species_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching species: {str(e)}")


@router.get("/{species_id}", response_model=SpeciesResponse)
async def get_species_details(
    species_id: int = Path(gt=0),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get detailed information about a specific species."""
    try:
        species_dto = await use_cases.get_species_details(species_id)
        if not species_dto:
            raise HTTPException(status_code=404, detail="Species not found")
        return SpeciesResponse(**species_dto.__dict__)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving species: {str(e)}")


@router.post("/users/{user_id}/collection", response_model=UserSpeciesResponse)
async def add_species_to_user_collection(
    user_id: str = Path(min_length=1, max_length=255),
    request: AddSpeciesRequest = ...,
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Add a discovered species to user's collection."""
    try:
        add_request = AddSpeciesRequestDTO(
            user_id=user_id,
            species_id=request.species_id,
            location_lat=request.location_lat,
            location_lng=request.location_lng,
            location_name=request.location_name,
            confidence_score=request.confidence_score,
            photo_url=request.photo_url,
            audio_url=request.audio_url,
            notes=request.notes
        )
        user_species_dto = await use_cases.add_species_to_user_collection(add_request)
        return UserSpeciesResponse(**user_species_dto.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding species to collection: {str(e)}")


@router.get("/users/{user_id}/collection", response_model=List[UserSpeciesResponse])
async def get_user_collection(
    user_id: str = Path(min_length=1, max_length=255),
    rarity_filter: Optional[RarityLevelSchema] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get user's discovered species collection."""
    try:
        user_species_dtos = await use_cases.get_user_collection(
            user_id, 
            rarity_filter.value if rarity_filter else None,
            limit, 
            offset
        )
        return [UserSpeciesResponse(**dto.__dict__) for dto in user_species_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user collection: {str(e)}")


@router.get("/collections/", response_model=List[CollectionResponse])
async def get_all_collections(
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get all available collections."""
    try:
        collection_dtos = await use_cases.get_all_collections()
        return [CollectionResponse(**dto.__dict__) for dto in collection_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving collections: {str(e)}")


@router.get("/collections/{collection_id}", response_model=CollectionWithSpeciesResponse)
async def get_collection_details(
    collection_id: int = Path(gt=0),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get collection with all its species."""
    try:
        collection_dto = await use_cases.get_collection_details(collection_id)
        if not collection_dto:
            raise HTTPException(status_code=404, detail="Collection not found")
        return CollectionWithSpeciesResponse(**collection_dto.__dict__)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving collection: {str(e)}")


@router.get("/users/{user_id}/collections/{collection_id}/progress", response_model=UserCollectionProgressResponse)
async def get_user_collection_progress(
    user_id: str = Path(min_length=1, max_length=255),
    collection_id: int = Path(gt=0),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get user's progress on a specific collection."""
    try:
        progress_dto = await use_cases.get_user_collection_progress(user_id, collection_id)
        if not progress_dto:
            raise HTTPException(status_code=404, detail="Collection not found")
        return UserCollectionProgressResponse(**progress_dto.__dict__)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving collection progress: {str(e)}")


@router.get("/rarity/{rarity_level}", response_model=List[SpeciesResponse])
async def get_species_by_rarity(
    rarity_level: RarityLevelSchema = Path(),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get species filtered by rarity level."""
    try:
        from ...domain.entities.species import RarityLevel
        rarity_enum = RarityLevel(rarity_level.value)
        species_list = await use_cases.species_repo.get_by_rarity(rarity_enum)
        species_dtos = [use_cases._species_to_dto(s) for s in species_list]
        return [SpeciesResponse(**dto.__dict__) for dto in species_dtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving species by rarity: {str(e)}")


@router.get("/users/{user_id}/stats", response_model=dict)
async def get_user_species_stats(
    user_id: str = Path(min_length=1, max_length=255),
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Get user's species collection statistics."""
    try:
        user_species_list = await use_cases.get_user_collection(user_id)
        
        # Calculate statistics
        total_species = len(user_species_list)
        rarity_counts = {}
        high_confidence_count = 0
        verified_count = 0
        
        for user_species in user_species_list:
            # Count by rarity
            rarity = user_species.species.rarity_level if user_species.species else "unknown"
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
            
            # Count high confidence and verified
            if user_species.is_high_confidence:
                high_confidence_count += 1
            if user_species.verified:
                verified_count += 1
        
        return {
            "user_id": user_id,
            "total_species_discovered": total_species,
            "rarity_breakdown": rarity_counts,
            "high_confidence_identifications": high_confidence_count,
            "verified_identifications": verified_count,
            "accuracy_rate": high_confidence_count / total_species if total_species > 0 else 0.0,
            "verification_rate": verified_count / total_species if total_species > 0 else 0.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating user stats: {str(e)}")


@router.post("/users/{user_id}/identify", response_model=BirdNetIdentificationResponse)
async def identify_and_add_species(
    user_id: str = Path(min_length=1, max_length=255),
    request: BirdNetIdentificationRequest = ...,
    use_cases: SpeciesUseCases = Depends(get_species_use_cases)
):
    """Identify bird species using BirdNet and add to user's collection."""
    try:
        from ...infrastructure.external.birdnet_service import BirdNetService
        
        # Initialize BirdNet service
        birdnet_service = BirdNetService()
        
        # Identify species using BirdNet
        identification_result = await birdnet_service.identify_species(
            request.audio_url,
            request.location_lat,
            request.location_lng
        )
        
        if not identification_result:
            raise HTTPException(status_code=400, detail="Failed to identify species from audio")
        
        # Parse the result
        parsed_result = birdnet_service.parse_identification_result(identification_result)
        if not parsed_result:
            raise HTTPException(status_code=400, detail="No species identified in audio")
        
        scientific_name = parsed_result["scientific_name"]
        confidence_score = parsed_result["confidence_score"]
        
        # Check if species exists in our database
        species = await use_cases.species_repo.get_by_scientific_name(scientific_name)
        
        if not species:
            raise HTTPException(
                status_code=404, 
                detail=f"Species '{scientific_name}' not found in our database. Please contact support to add this species."
            )
        
        # Check if user already discovered this species
        already_discovered = await use_cases.user_species_repo.has_user_discovered_species(
            user_id, species.id
        )
        
        user_species_dto = None
        is_new_discovery = not already_discovered
        message = ""
        
        if not already_discovered:
            # Add to user's collection
            add_request = AddSpeciesRequestDTO(
                user_id=user_id,
                species_id=species.id,
                location_lat=request.location_lat,
                location_lng=request.location_lng,
                location_name=request.location_name,
                confidence_score=confidence_score,
                photo_url=request.photo_url,
                audio_url=request.audio_url,
                notes=request.notes
            )
            
            user_species_dto = await use_cases.add_species_to_user_collection(add_request)
            message = f"¡Nueva especie descubierta! {species.common_name} ha sido añadida a tu colección."
        else:
            message = f"Ya tienes {species.common_name} en tu colección."
        
        # Convert species to DTO
        species_dto = use_cases._species_to_dto(species)
        
        return BirdNetIdentificationResponse(
            species=SpeciesResponse(**species_dto.__dict__),
            confidence_score=confidence_score,
            user_species=UserSpeciesResponse(**user_species_dto.__dict__) if user_species_dto else None,
            is_new_discovery=is_new_discovery,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing identification: {str(e)}")