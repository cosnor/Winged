from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import time
import asyncio
from typing import Dict
import httpx
import uvicorn
import os

app = FastAPI(title="Sightings Service", version="1.0.0")

# Configuration
ACHIEVEMENTS_URL = os.getenv("ACHIEVEMENTS_URL", "http://achievements:8006")

# Simple in-memory store to simulate persistence for created sightings.
# Keyed by sighting id -> dict representing the sighting. Protected by an
# asyncio.Lock to be safe for concurrent requests in the same process.
_SIGHTINGS_DB: Dict[int, dict] = {}
_SIGHTINGS_LOCK = asyncio.Lock()

class SightingCreate(BaseModel):
    user_id: int
    species_name: str  # Scientific name
    common_name: Optional[str] = None  # Common name
    timestamp: Optional[datetime] = None

class SightingResponse(BaseModel):
    id: int
    user_id: int
    species_name: str
    common_name: Optional[str] = None
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
    
    # In a real implementation, this would save to a database and return
    # an auto-incremented integer ID. For this demo we generate a unique
    # positive integer using the current time in milliseconds. This keeps
    # the `id` field as int (compatible with SightingResponse) while being
    # reasonably unique across rapid calls.
    sighting_id = int(time.time() * 1000)
    
    # Notify achievements service with simplified payload
    achievements_unlocked = []
    try:
        async with httpx.AsyncClient() as client:
            achievement_data = {
                "user_id": sighting.user_id,
                "species_name": sighting.species_name,
                "common_name": sighting.common_name,
                "timestamp": sighting.timestamp.isoformat()
            }
            
            print(f"📤 Sending to achievements: {achievement_data}")
            
            response = await client.post(
                f"{ACHIEVEMENTS_URL}/users/{sighting.user_id}/sightings",
                json=achievement_data,
                timeout=10.0
            )
            
            print(f"📥 Response from achievements: {response.status_code}")
            
            if response.status_code == 200:
                # The /users/{user_id}/sightings endpoint returns:
                # {"message": "...", "newly_unlocked_achievements": [...]}
                try:
                    body = response.json()
                    print(f"📦 Response body: {body}")
                except ValueError:
                    body = None

                if isinstance(body, dict):
                    # Extract newly_unlocked_achievements from response
                    unlocked = body.get("newly_unlocked_achievements", [])
                    if isinstance(unlocked, list):
                        achievements_unlocked = unlocked
                    else:
                        achievements_unlocked = []
                else:
                    achievements_unlocked = []
            else:
                print(f"❌ Failed to process achievements: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"❌ Error communicating with achievements service: {e}")
        # Don't fail the sighting creation if achievements service is down
    
    # Build the sighting object that we'll persist in the in-memory DB and
    # return to the caller. Keep timestamp as a datetime object so Pydantic
    # serializes it properly in responses.
    sighting_obj = {
        "id": sighting_id,
        "user_id": sighting.user_id,
        "species_name": sighting.species_name,
        "common_name": sighting.common_name,
        "timestamp": sighting.timestamp,
        "status": "processed",
        "achievements_unlocked": achievements_unlocked,
    }

    # Persist in memory
    async with _SIGHTINGS_LOCK:
        _SIGHTINGS_DB[sighting_id] = sighting_obj

    print(f"✅ Sighting created: ID={sighting_id}, Species={sighting.species_name}")
    return SightingResponse(**sighting_obj)

@app.get("/sightings/{sighting_id}", response_model=SightingResponse)
def get_sighting(sighting_id: int):
    """Get a specific sighting by ID"""
    # Lookup in our in-memory store.
    sighting = _SIGHTINGS_DB.get(sighting_id)
    if not sighting:
        raise HTTPException(status_code=404, detail="Sighting not found")

    return SightingResponse(**sighting)

@app.get("/users/{user_id}/sightings")
def get_user_sightings(user_id: int, limit: int = 50):
    """Get sightings for a specific user"""
    # Collect sightings from the in-memory store for this user.
    results = []
    for s in _SIGHTINGS_DB.values():
        if s.get("user_id") == user_id:
            # Provide a lightweight representation for the listing
            results.append({
                "id": s["id"],
                "species_name": s["species_name"],
                "common_name": s.get("common_name"),
                "timestamp": s["timestamp"].isoformat() if isinstance(s["timestamp"], datetime) else s["timestamp"],
            })
            if len(results) >= limit:
                break

    return {"user_id": user_id, "sightings": results, "total": len(results)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)