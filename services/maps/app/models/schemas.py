from pydantic import BaseModel
from typing import List
from datetime import datetime

class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime

class SpeciesProbability(BaseModel):
    species: str
    probability: float

class PredictionResponse(BaseModel):
    zone: str
    location: dict
    datetime: datetime
    species_probabilities: List[SpeciesProbability]