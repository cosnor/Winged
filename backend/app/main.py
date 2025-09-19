from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Winged BFF", version="0.1.0")


# -------------------------------
# MODELOS (para request/response)
# -------------------------------
class UserSignupRequest(BaseModel):
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


# ENDPOINTS USERS
@app.post("/users/signup", response_model=UserResponse)
def signup_user(request: UserSignupRequest):
    return UserResponse(id=1, email=request.email)


@app.post("/users/login")
def login_user(request: UserSignupRequest):
    return {"access_token": "fake_token_123"}


@app.get("/users/me", response_model=UserResponse)
def get_me():
    return UserResponse(id=1, email="test@example.com", xp=150, level=3)


# ENDPOINTS SIGHTINGS
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



# ENDPOINTS MAPS
@app.get("/maps/heatmap")
def get_heatmap(bbox: str, species: Optional[str] = None):
    return {
        "heatmap": [
            {"lat": 4.6, "lon": -74.1, "density": 12},
            {"lat": 4.7, "lon": -74.2, "density": 8},
        ]
    }


