# Colombian Caribbean bird species mapping for BirdNet integration
# This mapping helps convert BirdNet species codes to Winged species data

SPECIES_MAPPING = {
    # Hummingbirds - Trochilidae
    "RUBHUM": {
        "common_name": "Ruby-throated Hummingbird",
        "scientific_name": "Archilochus colubris",
        "family": "Trochilidae",
        "conservation_status": "LC",  # Least Concern
        "habitat": "Gardens, forests, parks",
        "endemic_to_colombia": False,
        "migration": "Migratory"
    },
    "ANGHUM": {
        "common_name": "Anna's Hummingbird", 
        "scientific_name": "Calypte anna",
        "family": "Trochilidae",
        "conservation_status": "LC",
        "habitat": "Coastal areas, parks, gardens",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    
    # Corvids - Corvidae
    "AMECRO": {
        "common_name": "American Crow",
        "scientific_name": "Corvus brachyrhynchos", 
        "family": "Corvidae",
        "conservation_status": "LC",
        "habitat": "Urban areas, farmlands, forests",
        "endemic_to_colombia": False,
        "migration": "Resident/Partial migrant"
    },
    "BLUJAY": {
        "common_name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "family": "Corvidae", 
        "conservation_status": "LC",
        "habitat": "Deciduous and mixed forests",
        "endemic_to_colombia": False,
        "migration": "Resident/Partial migrant"
    },
    
    # Cardinals - Cardinalidae
    "NORCAD": {
        "common_name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "family": "Cardinalidae",
        "conservation_status": "LC", 
        "habitat": "Woodlands, gardens, shrublands",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    
    # Finches - Fringillidae
    "AMEGFI": {
        "common_name": "American Goldfinch",
        "scientific_name": "Spinus tristis",
        "family": "Fringillidae",
        "conservation_status": "LC",
        "habitat": "Open country, gardens, fields",
        "endemic_to_colombia": False,
        "migration": "Partial migrant"
    },
    "HOUFIN": {
        "common_name": "House Finch", 
        "scientific_name": "Haemorhous mexicanus",
        "family": "Fringillidae",
        "conservation_status": "LC",
        "habitat": "Urban areas, farmlands, deserts",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    
    # Warblers - Parulidae
    "MOUWAR": {
        "common_name": "Mourning Warbler",
        "scientific_name": "Geothlypis philadelphia", 
        "family": "Parulidae",
        "conservation_status": "LC",
        "habitat": "Dense undergrowth, forest edges",
        "endemic_to_colombia": False,
        "migration": "Migratory"
    },
    "YELWAR": {
        "common_name": "Yellow Warbler",
        "scientific_name": "Setophaga petechia",
        "family": "Parulidae",
        "conservation_status": "LC",
        "habitat": "Riparian areas, gardens, mangroves",
        "endemic_to_colombia": False,
        "migration": "Migratory"
    },
    
    # Woodpeckers - Picidae  
    "REHWOO": {
        "common_name": "Red-headed Woodpecker",
        "scientific_name": "Melanerpes erythrocephalus",
        "family": "Picidae",
        "conservation_status": "NT",  # Near Threatened
        "habitat": "Open woodlands, parks, farmlands",
        "endemic_to_colombia": False,
        "migration": "Resident/Partial migrant"
    },
    "DOWWOO": {
        "common_name": "Downy Woodpecker", 
        "scientific_name": "Picoides pubescens",
        "family": "Picidae",
        "conservation_status": "LC",
        "habitat": "Deciduous forests, parks, orchards",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    
    # Colombian Caribbean Endemics and Regional Species
    "BACHUM": {
        "common_name": "Bahama Hummingbird",
        "scientific_name": "Riccordia ricordii",
        "family": "Trochilidae",
        "conservation_status": "LC",
        "habitat": "Coastal areas, gardens, dry forests",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    "CARBLA": {
        "common_name": "Caribbean Blackbird",
        "scientific_name": "Euphagus caribaeus",
        "family": "Icteridae",
        "conservation_status": "LC",
        "habitat": "Coastal wetlands, mangroves",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    "TROKIT": {
        "common_name": "Tropical Kite",
        "scientific_name": "Ictinia plumbea", 
        "family": "Accipitridae",
        "conservation_status": "LC",
        "habitat": "Tropical forests, forest edges",
        "endemic_to_colombia": False,
        "migration": "Migratory"
    },
    
    # Tyrant Flycatchers - Tyrannidae
    "GRKFLY": {
        "common_name": "Great Kiskadee",
        "scientific_name": "Pitangus sulphuratus",
        "family": "Tyrannidae", 
        "conservation_status": "LC",
        "habitat": "Open areas near water, parks",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    "TROFLY": {
        "common_name": "Tropical Flycatcher",
        "scientific_name": "Myiarchus tuberculifer",
        "family": "Tyrannidae",
        "conservation_status": "LC", 
        "habitat": "Forest edges, open woodlands",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    
    # Tanagers - Thraupidae
    "PALTAN": {
        "common_name": "Palm Tanager",
        "scientific_name": "Thraupis palmarum",
        "family": "Thraupidae",
        "conservation_status": "LC",
        "habitat": "Open areas with palms, parks",
        "endemic_to_colombia": False, 
        "migration": "Resident"
    },
    "BLUGRATAN": {
        "common_name": "Blue-gray Tanager",
        "scientific_name": "Thraupis episcopus",
        "family": "Thraupidae",
        "conservation_status": "LC",
        "habitat": "Open woodlands, gardens, parks",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    
    # Doves - Columbidae
    "RULDOV": {
        "common_name": "Ruddy Ground Dove",
        "scientific_name": "Columbina talpacoti",
        "family": "Columbidae",
        "conservation_status": "LC",
        "habitat": "Open areas, gardens, farmlands",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    "EARDOV": {
        "common_name": "Eared Dove",
        "scientific_name": "Zenaida auriculata", 
        "family": "Columbidae",
        "conservation_status": "LC",
        "habitat": "Open country, agricultural areas",
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    
    # Seabirds and Coastal Species
    "BROPEL": {
        "common_name": "Brown Pelican",
        "scientific_name": "Pelecanus occidentalis",
        "family": "Pelecanidae",
        "conservation_status": "LC",
        "habitat": "Coastal waters, beaches, mangroves", 
        "endemic_to_colombia": False,
        "migration": "Resident"
    },
    "MAGFRI": {
        "common_name": "Magnificent Frigatebird",
        "scientific_name": "Fregata magnificens",
        "family": "Fregatidae",
        "conservation_status": "LC",
        "habitat": "Coastal waters, islands",
        "endemic_to_colombia": False,
        "migration": "Resident"
    }
}

# Family information for grouping species
BIRD_FAMILIES = {
    "Trochilidae": {
        "common_name": "Hummingbirds",
        "description": "Small, nectar-feeding birds with rapid wingbeat",
        "typical_habitat": "Gardens, forests, flowering plants"
    },
    "Corvidae": {
        "common_name": "Crows and Jays", 
        "description": "Intelligent, social birds with strong bills",
        "typical_habitat": "Forests, urban areas, open country"
    },
    "Cardinalidae": {
        "common_name": "Cardinals and Grosbeaks",
        "description": "Seed-eating birds with thick, strong bills", 
        "typical_habitat": "Woodlands, gardens, shrublands"
    },
    "Fringillidae": {
        "common_name": "Finches",
        "description": "Small seed-eating birds with conical bills",
        "typical_habitat": "Open country, gardens, forests"
    },
    "Parulidae": {
        "common_name": "New World Warblers",
        "description": "Small insect-eating birds, often brightly colored",
        "typical_habitat": "Forests, woodland edges, gardens"
    },
    "Picidae": {
        "common_name": "Woodpeckers",
        "description": "Tree-climbing birds with strong bills for drilling",
        "typical_habitat": "Forests, woodlands, parks with trees"
    },
    "Tyrannidae": {
        "common_name": "Tyrant Flycatchers", 
        "description": "Insect-catching birds that hunt from perches",
        "typical_habitat": "Forest edges, open areas, parks"
    },
    "Thraupidae": {
        "common_name": "Tanagers",
        "description": "Colorful fruit and insect-eating birds",
        "typical_habitat": "Tropical forests, gardens, open woodlands"
    },
    "Columbidae": {
        "common_name": "Doves and Pigeons",
        "description": "Ground-feeding birds that eat seeds and fruits",
        "typical_habitat": "Open areas, gardens, agricultural land"
    },
    "Icteridae": {
        "common_name": "Blackbirds and Orioles",
        "description": "Medium-sized birds, often with bright colors or all black",
        "typical_habitat": "Open areas, wetlands, forests"
    }
}

def get_species_info(species_code: str) -> dict:
    """
    Get detailed information about a species by its code
    
    Args:
        species_code: The BirdNet species code (e.g., 'RUBHUM')
        
    Returns:
        Dictionary with species information, or empty dict if not found
    """
    return SPECIES_MAPPING.get(species_code, {
        "common_name": f"Unknown Species ({species_code})",
        "scientific_name": "Unknown",
        "family": "Unknown",
        "conservation_status": "Unknown",
        "habitat": "Unknown",
        "endemic_to_colombia": False,
        "migration": "Unknown"
    })

def get_family_info(family_name: str) -> dict:
    """
    Get information about a bird family
    
    Args:
        family_name: The scientific family name (e.g., 'Trochilidae')
        
    Returns:
        Dictionary with family information, or empty dict if not found
    """
    return BIRD_FAMILIES.get(family_name, {
        "common_name": f"Unknown Family ({family_name})",
        "description": "No description available",
        "typical_habitat": "Unknown"
    })

def get_species_by_family(family_name: str) -> list:
    """
    Get all species in a particular family
    
    Args:
        family_name: The scientific family name
        
    Returns:
        List of species codes in that family
    """
    return [
        code for code, info in SPECIES_MAPPING.items() 
        if info.get("family") == family_name
    ]

def get_endemic_species() -> list:
    """
    Get all species endemic to Colombia
    
    Returns:
        List of species codes for endemic species
    """
    return [
        code for code, info in SPECIES_MAPPING.items() 
        if info.get("endemic_to_colombia", False)
    ]

def get_migratory_species() -> list:
    """
    Get all migratory species
    
    Returns:
        List of species codes for migratory species
    """
    migratory_keywords = ["Migratory", "Partial migrant"]
    return [
        code for code, info in SPECIES_MAPPING.items() 
        if any(keyword in info.get("migration", "") for keyword in migratory_keywords)
    ]

def get_conservation_status_species(status: str) -> list:
    """
    Get all species with a particular conservation status
    
    Args:
        status: Conservation status (LC, NT, VU, EN, CR, etc.)
        
    Returns:
        List of species codes with that conservation status
    """
    return [
        code for code, info in SPECIES_MAPPING.items() 
        if info.get("conservation_status") == status
    ]

def search_species_by_name(search_term: str) -> list:
    """
    Search for species by common or scientific name
    
    Args:
        search_term: Term to search for (case insensitive)
        
    Returns:
        List of matching species codes
    """
    search_term = search_term.lower()
    matches = []
    
    for code, info in SPECIES_MAPPING.items():
        common_name = info.get("common_name", "").lower()
        scientific_name = info.get("scientific_name", "").lower()
        
        if (search_term in common_name or 
            search_term in scientific_name or
            search_term in code.lower()):
            matches.append(code)
    
    return matches

# Achievement-relevant groupings
ACHIEVEMENT_GROUPS = {
    "hummingbirds": get_species_by_family("Trochilidae"),
    "woodpeckers": get_species_by_family("Picidae"), 
    "corvids": get_species_by_family("Corvidae"),
    "tanagers": get_species_by_family("Thraupidae"),
    "warblers": get_species_by_family("Parulidae"),
    "endemic_species": get_endemic_species(),
    "migratory_species": get_migratory_species(),
    "conservation_concern": get_conservation_status_species("NT") + get_conservation_status_species("VU")
}

def get_achievement_group_species(group_name: str) -> list:
    """
    Get species codes for an achievement group
    
    Args:
        group_name: Name of the achievement group
        
    Returns:
        List of species codes in that group
    """
    return ACHIEVEMENT_GROUPS.get(group_name, [])

def is_species_in_group(species_code: str, group_name: str) -> bool:
    """
    Check if a species is part of an achievement group
    
    Args:
        species_code: The species code to check
        group_name: The achievement group name
        
    Returns:
        True if species is in the group, False otherwise
    """
    return species_code in ACHIEVEMENT_GROUPS.get(group_name, [])