"""
Seed data for Avedex database.
Contains sample species, collections, and achievements for Caribbean birds.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from .models import SpeciesModel, CollectionModel, AchievementModel
from ...domain.entities.species import RarityLevel
from ...domain.entities.achievement import AchievementType, AchievementTier


async def seed_species_data(session: AsyncSession):
    """Seed species data with Caribbean birds."""
    
    species_data = [
        # Common species
        {
            "scientific_name": "Turdus migratorius",
            "common_name": "American Robin",
            "common_name_es": "Petirrojo Americano",
            "family": "Turdidae",
            "description": "A migratory songbird with a distinctive red breast.",
            "habitat": "Gardens, parks, woodlands",
            "rarity_level": RarityLevel.COMMON.value,
            "conservation_status": "Least Concern",
            "size_cm": 25.0,
            "weight_g": 77.0,
            "wingspan_cm": 40.0
        },
        {
            "scientific_name": "Quiscalus niger",
            "common_name": "Greater Antillean Grackle",
            "common_name_es": "Chango",
            "family": "Icteridae",
            "description": "A large blackbird endemic to the Greater Antilles.",
            "habitat": "Urban areas, agricultural lands, mangroves",
            "rarity_level": RarityLevel.COMMON.value,
            "conservation_status": "Least Concern",
            "size_cm": 30.0,
            "weight_g": 120.0,
            "wingspan_cm": 45.0
        },
        {
            "scientific_name": "Coereba flaveola",
            "common_name": "Bananaquit",
            "common_name_es": "Reinita Común",
            "family": "Thraupidae",
            "description": "Small nectar-feeding bird common throughout the Caribbean.",
            "habitat": "Gardens, forest edges, plantations",
            "rarity_level": RarityLevel.COMMON.value,
            "conservation_status": "Least Concern",
            "size_cm": 11.0,
            "weight_g": 10.0,
            "wingspan_cm": 18.0
        },
        
        # Uncommon species
        {
            "scientific_name": "Todus mexicanus",
            "common_name": "Puerto Rican Tody",
            "common_name_es": "San Pedrito",
            "family": "Todidae",
            "description": "Small, colorful bird endemic to Puerto Rico.",
            "habitat": "Tropical forests, coffee plantations",
            "rarity_level": RarityLevel.UNCOMMON.value,
            "conservation_status": "Least Concern",
            "size_cm": 11.0,
            "weight_g": 6.0,
            "wingspan_cm": 15.0
        },
        {
            "scientific_name": "Spindalis portoricensis",
            "common_name": "Puerto Rican Spindalis",
            "common_name_es": "Reina Mora",
            "family": "Spindalidae",
            "description": "Colorful tanager endemic to Puerto Rico.",
            "habitat": "Forests, parks, gardens",
            "rarity_level": RarityLevel.UNCOMMON.value,
            "conservation_status": "Least Concern",
            "size_cm": 17.0,
            "weight_g": 25.0,
            "wingspan_cm": 28.0
        },
        
        # Rare species
        {
            "scientific_name": "Amazona vittata",
            "common_name": "Puerto Rican Parrot",
            "common_name_es": "Cotorra Puertorriqueña",
            "family": "Psittacidae",
            "description": "Critically endangered parrot endemic to Puerto Rico.",
            "habitat": "El Yunque rainforest",
            "rarity_level": RarityLevel.RARE.value,
            "conservation_status": "Critically Endangered",
            "size_cm": 30.0,
            "weight_g": 300.0,
            "wingspan_cm": 55.0
        },
        {
            "scientific_name": "Nesospingus speculiferus",
            "common_name": "Puerto Rican Tanager",
            "common_name_es": "Llorosa",
            "family": "Thraupidae",
            "description": "Endemic tanager found only in Puerto Rico's mountains.",
            "habitat": "Mountain forests above 600m",
            "rarity_level": RarityLevel.RARE.value,
            "conservation_status": "Near Threatened",
            "size_cm": 18.0,
            "weight_g": 30.0,
            "wingspan_cm": 30.0
        },
        
        # Very rare species
        {
            "scientific_name": "Rallus longirostris",
            "common_name": "Clapper Rail",
            "common_name_es": "Gallinuela de Mangle",
            "family": "Rallidae",
            "description": "Secretive marsh bird, very difficult to observe.",
            "habitat": "Mangrove swamps, salt marshes",
            "rarity_level": RarityLevel.VERY_RARE.value,
            "conservation_status": "Vulnerable",
            "size_cm": 35.0,
            "weight_g": 300.0,
            "wingspan_cm": 50.0
        },
        
        # Legendary species
        {
            "scientific_name": "Pterodroma hasitata",
            "common_name": "Black-capped Petrel",
            "common_name_es": "Diablotin",
            "family": "Procellariidae",
            "description": "Extremely rare seabird, breeds only in remote mountain areas.",
            "habitat": "Pelagic waters, mountain cliffs for nesting",
            "rarity_level": RarityLevel.LEGENDARY.value,
            "conservation_status": "Endangered",
            "size_cm": 40.0,
            "weight_g": 400.0,
            "wingspan_cm": 95.0
        }
    ]
    
    for species_data_item in species_data:
        species = SpeciesModel(**species_data_item)
        session.add(species)
    
    await session.commit()


async def seed_collections_data(session: AsyncSession):
    """Seed collections data."""
    
    collections_data = [
        {
            "name": "Endemic Birds of Puerto Rico",
            "description": "Birds found only in Puerto Rico",
            "icon": "🦜",
            "color": "#FF6B6B",
            "species_ids": [4, 5, 6, 7],  # Puerto Rican Tody, Spindalis, Parrot, Tanager
            "is_system_collection": True
        },
        {
            "name": "Common Garden Birds",
            "description": "Birds commonly seen in gardens and urban areas",
            "icon": "🏡",
            "color": "#4ECDC4",
            "species_ids": [1, 2, 3],  # Robin, Grackle, Bananaquit
            "is_system_collection": True
        },
        {
            "name": "Endangered Species",
            "description": "Birds with conservation concerns",
            "icon": "⚠️",
            "color": "#FF9F43",
            "species_ids": [6, 8, 9],  # Puerto Rican Parrot, Clapper Rail, Black-capped Petrel
            "is_system_collection": True
        },
        {
            "name": "Forest Dwellers",
            "description": "Birds that prefer forested habitats",
            "icon": "🌲",
            "color": "#26DE81",
            "species_ids": [4, 5, 7],  # Puerto Rican Tody, Spindalis, Tanager
            "is_system_collection": True
        },
        {
            "name": "Seabirds and Coastal Species",
            "description": "Birds associated with marine environments",
            "icon": "🌊",
            "color": "#3742FA",
            "species_ids": [8, 9],  # Clapper Rail, Black-capped Petrel
            "is_system_collection": True
        }
    ]
    
    for collection_data in collections_data:
        collection = CollectionModel(**collection_data)
        session.add(collection)
    
    await session.commit()


async def seed_achievements_data(session: AsyncSession):
    """Seed achievements data."""
    
    achievements_data = [
        # Discovery achievements
        {
            "name": "First Steps",
            "description": "Discover your first bird species",
            "achievement_type": AchievementType.DISCOVERY.value,
            "tier": AchievementTier.BRONZE.value,
            "icon": "🐣",
            "points": 50,
            "requirement_value": 1,
            "requirement_description": "Discover 1 species"
        },
        {
            "name": "Getting Started",
            "description": "Discover 5 different bird species",
            "achievement_type": AchievementType.DISCOVERY.value,
            "tier": AchievementTier.BRONZE.value,
            "icon": "🐦",
            "points": 100,
            "requirement_value": 5,
            "requirement_description": "Discover 5 species"
        },
        {
            "name": "Birdwatcher",
            "description": "Discover 25 different bird species",
            "achievement_type": AchievementType.DISCOVERY.value,
            "tier": AchievementTier.SILVER.value,
            "icon": "🔍",
            "points": 250,
            "requirement_value": 25,
            "requirement_description": "Discover 25 species"
        },
        {
            "name": "Ornithologist",
            "description": "Discover 100 different bird species",
            "achievement_type": AchievementType.DISCOVERY.value,
            "tier": AchievementTier.GOLD.value,
            "icon": "🎓",
            "points": 500,
            "requirement_value": 100,
            "requirement_description": "Discover 100 species"
        },
        
        # Streak achievements
        {
            "name": "Daily Birder",
            "description": "Discover birds for 3 consecutive days",
            "achievement_type": AchievementType.STREAK.value,
            "tier": AchievementTier.BRONZE.value,
            "icon": "📅",
            "points": 75,
            "requirement_value": 3,
            "requirement_description": "3-day streak"
        },
        {
            "name": "Dedicated Observer",
            "description": "Discover birds for 7 consecutive days",
            "achievement_type": AchievementType.STREAK.value,
            "tier": AchievementTier.SILVER.value,
            "icon": "🗓️",
            "points": 150,
            "requirement_value": 7,
            "requirement_description": "7-day streak"
        },
        {
            "name": "Committed Naturalist",
            "description": "Discover birds for 30 consecutive days",
            "achievement_type": AchievementType.STREAK.value,
            "tier": AchievementTier.GOLD.value,
            "icon": "🏆",
            "points": 400,
            "requirement_value": 30,
            "requirement_description": "30-day streak"
        },
        
        # Rarity achievements
        {
            "name": "Rare Find",
            "description": "Discover your first rare bird",
            "achievement_type": AchievementType.RARITY.value,
            "tier": AchievementTier.SILVER.value,
            "icon": "💎",
            "points": 200,
            "requirement_value": 1,
            "requirement_description": "Discover 1 rare species"
        },
        {
            "name": "Treasure Hunter",
            "description": "Discover 5 rare bird species",
            "achievement_type": AchievementType.RARITY.value,
            "tier": AchievementTier.GOLD.value,
            "icon": "🏴‍☠️",
            "points": 500,
            "requirement_value": 5,
            "requirement_description": "Discover 5 rare species"
        },
        {
            "name": "Legend Seeker",
            "description": "Discover a legendary bird species",
            "achievement_type": AchievementType.RARITY.value,
            "tier": AchievementTier.DIAMOND.value,
            "icon": "⭐",
            "points": 1000,
            "requirement_value": 1,
            "requirement_description": "Discover 1 legendary species",
            "is_hidden": True
        },
        
        # Collection achievements
        {
            "name": "Collector",
            "description": "Complete your first collection",
            "achievement_type": AchievementType.COLLECTION.value,
            "tier": AchievementTier.SILVER.value,
            "icon": "📚",
            "points": 300,
            "requirement_value": 1,
            "requirement_description": "Complete 1 collection"
        },
        
        # Expertise achievements
        {
            "name": "Sharp Eye",
            "description": "Make 10 high-confidence identifications",
            "achievement_type": AchievementType.EXPERTISE.value,
            "tier": AchievementTier.BRONZE.value,
            "icon": "👁️",
            "points": 100,
            "requirement_value": 10,
            "requirement_description": "10 high-confidence identifications"
        },
        {
            "name": "Expert Observer",
            "description": "Make 50 high-confidence identifications",
            "achievement_type": AchievementType.EXPERTISE.value,
            "tier": AchievementTier.SILVER.value,
            "icon": "🎯",
            "points": 250,
            "requirement_value": 50,
            "requirement_description": "50 high-confidence identifications"
        },
        
        # Location achievements
        {
            "name": "Explorer",
            "description": "Discover birds in 5 different locations",
            "achievement_type": AchievementType.LOCATION.value,
            "tier": AchievementTier.BRONZE.value,
            "icon": "🗺️",
            "points": 150,
            "requirement_value": 5,
            "requirement_description": "Discover birds in 5 locations"
        },
        {
            "name": "Island Hopper",
            "description": "Discover birds in 20 different locations",
            "achievement_type": AchievementType.LOCATION.value,
            "tier": AchievementTier.GOLD.value,
            "icon": "🏝️",
            "points": 400,
            "requirement_value": 20,
            "requirement_description": "Discover birds in 20 locations"
        }
    ]
    
    for achievement_data in achievements_data:
        achievement = AchievementModel(**achievement_data)
        session.add(achievement)
    
    await session.commit()


async def seed_all_data(session: AsyncSession):
    """Seed all data."""
    await seed_species_data(session)
    await seed_collections_data(session)
    await seed_achievements_data(session)