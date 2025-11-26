import pytest
from datetime import datetime
import numpy as np
from app.services.prediction_service import predict_species, predict_distribution
from app.models.predictor import model, species_cols, feature_cols, zonas

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
    monkeypatch.setattr("app.services.prediction_service.model", mock)
    return mock

def test_predict_species_returns_correct_structure(sample_location):
    """Test que predict_species retorna la estructura correcta de datos"""
    result = predict_species(
        sample_location["lat"],
        sample_location["lon"],
        sample_location["timestamp"]
    )
    
    assert isinstance(result, dict)
    assert "zone" in result
    assert "location" in result
    assert "datetime" in result
    assert "species_probabilities" in result
    assert isinstance(result["species_probabilities"], list)
    assert len(result["species_probabilities"]) > 0

def test_predict_species_probabilities_are_valid(sample_location):
    """Test que las probabilidades están en el rango correcto"""
    result = predict_species(
        sample_location["lat"],
        sample_location["lon"],
        sample_location["timestamp"]
    )
    
    # En un modelo multi-label, verificamos que cada probabilidad
    # esté en el rango [0,1]
    probs = [sp["probability"] for sp in result["species_probabilities"]]
    assert all(0 <= p <= 1 for p in probs)
    # Verificar que hay al menos una probabilidad > 0
    assert any(p > 0 for p in probs)

def test_predict_species_location_matches_input(sample_location):
    """Test que la ubicación en la respuesta coincide con la entrada"""
    result = predict_species(
        sample_location["lat"],
        sample_location["lon"],
        sample_location["timestamp"]
    )
    
    assert result["location"]["lat"] == sample_location["lat"]
    assert result["location"]["lon"] == sample_location["lon"]

def test_predict_species_with_mock_model(sample_location, mock_model):
    """Test predict_species usando un modelo simulado"""
    result = predict_species(
        sample_location["lat"],
        sample_location["lon"],
        sample_location["timestamp"]
    )
    
    # Con nuestro mock_model, todas las especies deberían tener
    # probabilidad 0.7 o 0.3
    probs = [sp["probability"] for sp in result["species_probabilities"]]
    assert all(p in [0.7, 0.3] for p in probs)

