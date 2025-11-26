import pytest
from datetime import datetime
import numpy as np
from app.models.predictor import model, species_cols

@pytest.fixture
def sample_location():
    """Fixture con una ubicación de prueba en Barranquilla"""
    return {
        "lat": 10.9878,
        "lon": -74.7889,
        "timestamp": datetime(2025, 10, 20, 14, 30)
    }

@pytest.fixture
def mock_model(monkeypatch):
    """Fixture que simula el modelo de predicción"""
    class MockEstimator:
        def predict_proba(self, X):
            # Retorna probabilidades simuladas
            return np.array([[0.7, 0.3]])

    class MockModel:
        def __init__(self):
            self.estimators_ = [MockEstimator() for _ in range(len(species_cols))]

    mock = MockModel()
    monkeypatch.setattr("app.models.predictor.model", mock)
    return mock

@pytest.fixture
def test_client():
    """Fixture que proporciona un cliente de prueba para la API"""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)