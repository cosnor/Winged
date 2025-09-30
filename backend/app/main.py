from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
from fastapi import Header

app = FastAPI(title="Winged BFF", version="0.1.0")

# Configuración de microservicios
USERS_SERVICE_URL = "http://users:8001"
# SIGHTINGS_SERVICE_URL = "http://sightings:8002"  # Para futuro
# MAPS_SERVICE_URL = "http://maps:8003"       # Para futuro

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
    lat: float
    lon: float
    timestamp: datetime
    audio_url: str

class SightingResponse(BaseModel):
    id: int
    species: Optional[str] = None
    confidence: Optional[float] = None
    status: str

# -------------------------------
# ENDPOINTS USERS (Forward to Users Service)
# -------------------------------

@app.post("/users/signup", response_model=dict)
async def signup_user(request: UserSignupRequest):
    """Forward signup to Users Service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{USERS_SERVICE_URL}/register",
                json={"email": request.email, "password": request.password}
            )
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Users service unavailable")

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
def create_sighting(request: SightingRequest):
    return SightingResponse(id=123, status="processing")

@app.get("/sightings/{sighting_id}", response_model=SightingResponse)
def get_sighting(sighting_id: int):
    return SightingResponse(
        id=sighting_id,
        species="Turdus ignobilis",
        confidence=0.92,
        status="processed",
    )

# -------------------------------
# ENDPOINTS MAPS (Mock por ahora)
# -------------------------------
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
