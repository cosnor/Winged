from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class SightingEventRequest(BaseModel):
    """Request schema for sighting events"""
    user_id: int
    species_name: str
    common_name: Optional[str] = None
    confidence_score: float
    location_lat: float
    location_lon: float
    timestamp: datetime


class CreateAchievementRequest(BaseModel):
    """Request schema for creating achievements"""
    name: str
    description: str
    category: str
    criteria: Optional[Dict[str, Any]] = None
    xp_reward: int = 0
    icon: Optional[str] = None


class SpeciesDetectionRequest(BaseModel):
    """Request schema for species detection from ML worker"""
    user_id: int
    species_name: str
    confidence: float
    location: Optional[Dict[str, Any]] = None
    detection_time: datetime


class BatchSpeciesDetectionRequest(BaseModel):
    """Request schema for batch species detection processing"""
    detections: List[SpeciesDetectionRequest]