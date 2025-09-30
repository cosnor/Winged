from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import httpx
import uvicorn
import os

app = FastAPI(title="Sightings Service", version="1.0.0")

# Configuration
ACHIEVEMENTS_URL = os.getenv("ACHIEVEMENTS_URL", "http://achievements:8006")

class SightingCreate(BaseModel):
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: float
    location_lat: float
    location_lon: float
    timestamp: Optional[datetime] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None

class SightingResponse(BaseModel):
    id: int
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: float
    location_lat: float
    location_lon: float
    timestamp: datetime
    status: str = "processed"
    achievements_unlocked: List[dict] = []

@app.get("/")
def read_root():
    return {"message": "Sightings service is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/sightings", response_model=SightingResponse)
async def create_sighting(sighting: SightingCreate):
    """Create a new bird sighting and process achievements"""
    
    # Set timestamp if not provided
    if not sighting.timestamp:
        sighting.timestamp = datetime.utcnow()
    
    # In a real implementation, this would save to database
    # For now, we'll simulate a sighting ID
    sighting_id = 12345
    
    # Notify achievements service
    achievements_unlocked = []
    try:
        async with httpx.AsyncClient() as client:
            achievement_data = {
                "user_id": sighting.user_id,
                "species_name": sighting.species_name,
                "common_name": sighting.common_name,
                "confidence_score": sighting.confidence_score,
                "location_lat": sighting.location_lat,
                "location_lon": sighting.location_lon,
                "timestamp": sighting.timestamp.isoformat()
            }
            
            response = await client.post(
                f"{ACHIEVEMENTS_URL}/sightings/process",
                json=achievement_data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                achievements_unlocked = response.json()
            else:
                print(f"Failed to process achievements: {response.status_code}")
                
    except Exception as e:
        print(f"Error communicating with achievements service: {e}")
        # Don't fail the sighting creation if achievements service is down
    
    return SightingResponse(
        id=sighting_id,
        user_id=sighting.user_id,
        species_name=sighting.species_name,
        common_name=sighting.common_name,
        confidence_score=sighting.confidence_score,
        location_lat=sighting.location_lat,
        location_lon=sighting.location_lon,
        timestamp=sighting.timestamp,
        achievements_unlocked=achievements_unlocked
    )

@app.get("/sightings/{sighting_id}", response_model=SightingResponse)
def get_sighting(sighting_id: int):
    """Get a specific sighting by ID"""
    # In a real implementation, this would query the database
    # For now, return a mock response
    return SightingResponse(
        id=sighting_id,
        user_id=1,
        species_name="Turdus ignobilis",
        common_name="Black-billed Thrush",
        confidence_score=0.92,
        location_lat=10.4806,
        location_lon=-75.5138,
        timestamp=datetime.utcnow(),
        status="processed"
    )

@app.get("/users/{user_id}/sightings")
def get_user_sightings(user_id: int, limit: int = 50):
    """Get sightings for a specific user"""
    # In a real implementation, this would query the database
    # For now, return a mock response
    return {
        "user_id": user_id,
        "sightings": [
            {
                "id": 1,
                "species_name": "Turdus ignobilis",
                "common_name": "Black-billed Thrush",
                "confidence_score": 0.92,
                "timestamp": datetime.utcnow().isoformat()
            }
        ],
        "total": 1
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)