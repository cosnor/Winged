import pytest
from datetime import datetime
from app.models.schemas import (
    PredictionRequest,
    PredictionResponse,
    SpeciesProbability,
    DistributionRequest,
    DistributionZoneRequest,
    PolygonArea,
    SpeciesDistribution
)

def test_prediction_request_valid():
    """Test que la creación de PredictionRequest funciona con datos válidos"""
    request = PredictionRequest(
        latitude=10.9878,
        longitude=-74.7889,
        timestamp=datetime.now()
    )
    assert isinstance(request, PredictionRequest)
    assert isinstance(request.timestamp, datetime)
    assert -90 <= request.latitude <= 90
    assert -180 <= request.longitude <= 180




def test_species_probability_valid():
    """Test que SpeciesProbability acepta datos válidos"""
    prob = SpeciesProbability(
        species="Columba livia",
        probability=0.75
    )
    assert isinstance(prob, SpeciesProbability)
    assert 0 <= prob.probability <= 1
    assert isinstance(prob.species, str)


def test_prediction_response_valid():
    """Test que PredictionResponse acepta un formato válido completo"""
    response = PredictionResponse(
        zone="Norte Centro Histórico",
        location={"lat": 10.9878, "lon": -74.7889},
        datetime=datetime.now(),
        species_probabilities=[
            SpeciesProbability(species="Columba livia", probability=0.75),
            SpeciesProbability(species="Zenaida auriculata", probability=0.25)
        ]
    )
    assert isinstance(response, PredictionResponse)
    assert len(response.species_probabilities) > 0
    assert sum(sp.probability for sp in response.species_probabilities) > 0

def test_distribution_request_valid():
    """Test que DistributionRequest acepta parámetros opcionales"""
    request = DistributionRequest(
        lat=10.9878,
        lon=-74.7889,
        datetime="2025-10-20T14:30:00",
        radius=1000,
        grid_size=0.002
    )
    assert isinstance(request, DistributionRequest)
    assert request.radius > 0
    assert request.grid_size > 0

def test_distribution_request_defaults():
    """Test que DistributionRequest usa valores por defecto correctamente"""
    request = DistributionRequest(
        lat=10.9878,
        lon=-74.7889,
        datetime="2025-10-20T14:30:00"
    )
    assert request.radius == 500  # valor por defecto
    assert request.grid_size == 0.001  # valor por defecto

def test_distribution_zone_request_valid():
    """Test que DistributionZoneRequest funciona correctamente"""
    request = DistributionZoneRequest(
        lat=10.9878,
        lon=-74.7889,
        datetime="2025-10-20T14:30:00",
        grid_size=0.001
    )
    assert isinstance(request, DistributionZoneRequest)
    assert request.grid_size > 0