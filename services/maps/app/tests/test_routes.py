import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app  # asumiendo que tu app FastAPI está en main.py

client = TestClient(app)

def test_predict_endpoint_success():
    """Test que el endpoint /predict funciona correctamente"""
    response = client.post(
        "/predict",
        json={
            "latitude": 10.9878,
            "longitude": -74.7889,
            "timestamp": "2025-10-20T14:30:00"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "zone" in data
    assert "location" in data
    assert "datetime" in data
    assert "species_probabilities" in data
    assert isinstance(data["species_probabilities"], list)


def test_distribution_zone_endpoint_success():
    """Test que el endpoint /distribution-zone funciona correctamente"""
    response = client.post(
        "/distribution-zone",
        json={
            "lat": 10.9878,
            "lon": -74.7889,
            "datetime": "2025-10-20T14:30:00",
            "grid_size": 0.001
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Verificar que hay al menos una especie en el resultado
    assert len(data) > 0

