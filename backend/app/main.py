from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
import os

app = FastAPI(title="Winged BFF", version="0.1.0")

# Service URLs
USERS_URL = os.getenv("USERS_URL", "http://users:8001")
SIGHTINGS_URL = os.getenv("SIGHTINGS_URL", "http://sightings:8002")
ACHIEVEMENTS_URL = os.getenv("ACHIEVEMENTS_URL", "http://achievements:8006")
ML_WORKER_URL = os.getenv("ML_WORKER_URL", "http://ml_worker:8003")
MAPS_URL = os.getenv("MAPS_URL", "http://maps:8004")
ROUTES_URL = os.getenv("ROUTES_URL", "http://routes:8005")

# -------------------------------
# MODELOS (para request/response)
# -------------------------------
class UserSignupRequest(BaseModel):
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    xp: int = 0
    level: int = 1

class SightingRequest(BaseModel):
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: float
    lat: float
    lon: float
    timestamp: Optional[datetime] = None
    audio_url: Optional[str] = None


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


# ENDPOINTS USERS
@app.post("/users/signup", response_model=UserResponse)
def signup_user(request: UserSignupRequest):
    return UserResponse(id=1, email=request.email)


@app.post("/users/login")
async def login_user(request: UserLoginRequest):
    """Forward login to Users Service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{USERS_SERVICE_URL}/login",
                json={"email": request.email, "password": request.password}
            )
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

@app.get("/users/me")
async def get_me(authorization: str = Header(None)):
    """Forward profile request to Users Service with auth token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    async with httpx.AsyncClient() as client:
        try:
            # Reenviar el token en los headers
            headers = {"Authorization": authorization}
            response = await client.get(
                f"{USERS_SERVICE_URL}/profile",
                headers=headers
            )
            
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            elif response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error from users service")
                
            return response.json()
            
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")
# -------------------------------
# ENDPOINTS SIGHTINGS (Mock por ahora)
# -------------------------------
@app.post("/sightings", response_model=SightingResponse)
async def create_sighting(request: SightingRequest):
    """Create a new bird sighting"""
    async with httpx.AsyncClient() as client:
        sighting_data = {
            "user_id": request.user_id,
            "species_name": request.species_name,
            "common_name": request.common_name,
            "confidence_score": request.confidence_score,
            "location_lat": request.lat,
            "location_lon": request.lon,
            "timestamp": request.timestamp.isoformat() if request.timestamp else None,
            "audio_url": request.audio_url
        }
        
        try:
            response = await client.post(f"{SIGHTINGS_URL}/sightings", json=sighting_data)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to create sighting")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Sightings service unavailable")


@app.get("/sightings/{sighting_id}", response_model=SightingResponse)
async def get_sighting(sighting_id: int):
    """Get a specific sighting"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SIGHTINGS_URL}/sightings/{sighting_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Sighting not found")
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get sighting")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Sightings service unavailable")



# ENDPOINTS ACHIEVEMENTS
@app.get("/users/{user_id}/collection")
async def get_user_collection(user_id: int):
    """Get user's bird collection with stats and achievements"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/collection")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get user collection")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Achievements service unavailable")

@app.get("/users/{user_id}/achievements")
async def get_user_achievements(user_id: int):
    """Get user's unlocked achievements"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/achievements")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get user achievements")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Achievements service unavailable")

@app.get("/users/{user_id}/achievements/progress")
async def get_achievement_progress(user_id: int):
    """Get user's progress on all achievements"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/achievements/progress")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get achievement progress")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Achievements service unavailable")

@app.get("/users/{user_id}/stats")
async def get_user_stats(user_id: int):
    """Get user statistics"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ACHIEVEMENTS_URL}/users/{user_id}/stats")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get user stats")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Achievements service unavailable")

@app.get("/leaderboard/species")
async def get_species_leaderboard(limit: int = 10):
    """Get species leaderboard"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ACHIEVEMENTS_URL}/leaderboard/species?limit={limit}")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get leaderboard")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Achievements service unavailable")

@app.get("/leaderboard/xp")
async def get_xp_leaderboard(limit: int = 10):
    """Get XP leaderboard"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ACHIEVEMENTS_URL}/leaderboard/xp?limit={limit}")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get leaderboard")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Achievements service unavailable")

@app.get("/achievements")
async def get_all_achievements():
    """Get all available achievements"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ACHIEVEMENTS_URL}/achievements")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to get achievements")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Achievements service unavailable")

# ENDPOINTS MAPS
@app.get("/maps/heatmap")
def get_heatmap(bbox: str, species: Optional[str] = None):
    return {
        "heatmap": [
            {"lat": 4.6, "lon": -74.1, "density": 12},
            {"lat": 4.7, "lon": -74.2, "density": 8},
        ]
    }

# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/health")
async def health_check():
    """Check health of all services"""
    services_health = {}
    
    # Check Users Service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USERS_SERVICE_URL}/health", timeout=5.0)
            services_health["users"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_health["users"] = "unavailable"
    
    return {
        "api_gateway": "healthy",
        "services": services_health
    }
