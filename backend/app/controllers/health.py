import os
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    # Simple health that reports configured service URLs
    return {
        "status": "ok",
        "users_url": os.getenv("USERS_URL", "http://users:8001"),
        "sightings_url": os.getenv("SIGHTINGS_URL", "http://sightings:8002"),
        "achievements_url": os.getenv("ACHIEVEMENTS_URL", "http://achievements:8003"),
        "maps_url": os.getenv("MAPS_URL", "http://maps:8004"),
    }
