from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime


"""Schemas para requests y responses de la API """

"""Schemas para /predict""" 

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
    
"""Schemas para /distribution"""     
    
class DistributionRequest(BaseModel):
    lat: float
    lon: float
    datetime: str
    radius: float = 500   # metros alrededor
    grid_size: float = 0.001  # resolución lat/lon (~100m)

class PolygonArea(BaseModel):
    polygon: List[Dict[str, float]]
    probability: float

class SpeciesDistribution(BaseModel):
    species: str
    max_probability: float
    areas: List[PolygonArea]
    
class DistributionZoneRequest(BaseModel):
    lat: float
    lon: float
    datetime: str
    radius: float = 500   # metros alrededor
    grid_size: float = 0.001   # ~100m