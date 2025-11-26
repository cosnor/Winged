"""
Unit tests for Sightings service API endpoints
"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from datetime import datetime


class TestSightingsAPI:
    """Test cases for sightings API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_create_sighting_success(self, client, sample_sighting_data, mock_achievements_service_success):
        """Test successful sighting creation"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_achievements_service_success
            
            response = client.post("/sightings", json=sample_sighting_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] is not None
            assert data["user_id"] == sample_sighting_data["user_id"]
            assert data["species_name"] == sample_sighting_data["species_name"]
            assert data["confidence_score"] == sample_sighting_data["confidence_score"]
            assert "achievements_unlocked" in data
    
    def test_create_sighting_minimal_data(self, client, sample_sighting_minimal, mock_achievements_service_success):
        """Test sighting creation with minimal required data"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_achievements_service_success
            
            response = client.post("/sightings", json=sample_sighting_minimal)
            
            assert response.status_code == 200
            data = response.json()
            assert data["user_id"] == sample_sighting_minimal["user_id"]
            assert data["species_name"] == sample_sighting_minimal["species_name"]
            assert data["common_name"] is None  # Optional field
            assert data["timestamp"] is not None  # Should be auto-generated
    
    def test_create_sighting_invalid_data(self, client):
        """Test sighting creation with invalid data"""
        invalid_data = {
            "user_id": "invalid",  # Should be int
            "species_name": "",    # Empty string
            "confidence_score": 1.5,  # Invalid confidence > 1.0
            "location_lat": "invalid",  # Should be float
            "location_lon": "invalid"   # Should be float
        }
        
        response = client.post("/sightings", json=invalid_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_sighting_missing_required_fields(self, client):
        """Test sighting creation with missing required fields"""
        incomplete_data = {
            "user_id": 1,
            # Missing species_name, confidence_score, location fields
        }
        
        response = client.post("/sightings", json=incomplete_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_sighting_achievements_service_failure(self, client, sample_sighting_data, mock_achievements_service_failure):
        """Test sighting creation when achievements service fails"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_achievements_service_failure
            
            response = client.post("/sightings", json=sample_sighting_data)
            
            # Should still succeed even if achievements service fails
            assert response.status_code == 200
            data = response.json()
            assert data["id"] is not None
            assert data["achievements_unlocked"] == []  # No achievements due to service failure
    
    def test_create_sighting_achievements_service_timeout(self, client, sample_sighting_data, mock_achievements_service_timeout):
        """Test sighting creation when achievements service times out"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_achievements_service_timeout
            
            response = client.post("/sightings", json=sample_sighting_data)
            
            # Should still succeed even if achievements service times out
            assert response.status_code == 200
            data = response.json()
            assert data["id"] is not None
            assert data["achievements_unlocked"] == []  # No achievements due to timeout
    
    def test_get_sighting_by_id(self, client):
        """Test retrieving sighting by ID"""
        sighting_id = 123
        
        response = client.get(f"/sightings/{sighting_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sighting_id
        assert "species_name" in data
        assert "user_id" in data
        assert "timestamp" in data
    
    def test_get_user_sightings(self, client):
        """Test retrieving sightings for a user"""
        user_id = 1
        
        response = client.get(f"/users/{user_id}/sightings")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert "sightings" in data
        assert "total" in data
        assert isinstance(data["sightings"], list)
    
    def test_get_user_sightings_with_limit(self, client):
        """Test retrieving user sightings with limit parameter"""
        user_id = 1
        limit = 10
        
        response = client.get(f"/users/{user_id}/sightings?limit={limit}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id


class TestSightingModels:
    """Test cases for sighting data models"""
    
    def test_sighting_create_model_validation(self):
        """Test SightingCreate model validation"""
        from ...app.main import SightingCreate
        from datetime import datetime
        
        # Valid sighting data
        valid_data = {
            "user_id": 1,
            "species_name": "Turdus ignobilis",
            "common_name": "Black-billed Thrush",
            "confidence_score": 0.92,
            "location_lat": 10.4806,
            "location_lon": -75.5138,
            "timestamp": datetime.utcnow(),
            "audio_url": "https://example.com/audio.mp3",
            "image_url": "https://example.com/image.jpg"
        }
        
        sighting = SightingCreate(**valid_data)
        assert sighting.user_id == 1
        assert sighting.species_name == "Turdus ignobilis"
        assert sighting.confidence_score == 0.92
    
    def test_sighting_create_invalid_confidence(self):
        """Test SightingCreate with invalid confidence score"""
        from ...app.main import SightingCreate
        from pydantic import ValidationError
        
        invalid_data = {
            "user_id": 1,
            "species_name": "Test Bird",
            "confidence_score": 1.5,  # Invalid: > 1.0
            "location_lat": 10.0,
            "location_lon": -75.0
        }
        
        with pytest.raises(ValidationError):
            SightingCreate(**invalid_data)
    
    def test_sighting_create_negative_confidence(self):
        """Test SightingCreate with negative confidence score"""
        from ...app.main import SightingCreate
        from pydantic import ValidationError
        
        invalid_data = {
            "user_id": 1,
            "species_name": "Test Bird",
            "confidence_score": -0.1,  # Invalid: < 0.0
            "location_lat": 10.0,
            "location_lon": -75.0
        }
        
        with pytest.raises(ValidationError):
            SightingCreate(**invalid_data)
    
    def test_sighting_response_model(self):
        """Test SightingResponse model"""
        from ...app.main import SightingResponse
        from datetime import datetime
        
        response_data = {
            "id": 123,
            "user_id": 1,
            "species_name": "Turdus ignobilis",
            "common_name": "Black-billed Thrush",
            "confidence_score": 0.92,
            "location_lat": 10.4806,
            "location_lon": -75.5138,
            "timestamp": datetime.utcnow(),
            "status": "processed"
        }
        
        response = SightingResponse(**response_data)
        assert response.id == 123
        assert response.user_id == 1
        assert response.status == "processed"


class TestSightingBusinessLogic:
    """Test cases for sighting business logic"""
    
    def test_timestamp_auto_generation(self, client, sample_sighting_minimal, mock_achievements_service_success):
        """Test that timestamp is automatically generated when not provided"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_achievements_service_success
            
            # Remove timestamp from data
            data_without_timestamp = sample_sighting_minimal.copy()
            if "timestamp" in data_without_timestamp:
                del data_without_timestamp["timestamp"]
            
            response = client.post("/sightings", json=data_without_timestamp)
            
            assert response.status_code == 200
            result = response.json()
            assert result["timestamp"] is not None
            # Timestamp should be recent (within last minute)
            timestamp = datetime.fromisoformat(result["timestamp"].replace('Z', '+00:00'))
            time_diff = datetime.now(timestamp.tzinfo) - timestamp
            assert time_diff.total_seconds() < 60
    
    def test_achievements_notification_payload(self, client, sample_sighting_data, mock_achievements_service_success):
        """Test that correct data is sent to achievements service"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_client = mock_achievements_service_success
            mock_async_client.return_value.__aenter__.return_value = mock_client
            
            response = client.post("/sightings", json=sample_sighting_data)
            
            assert response.status_code == 200
            
            # Verify achievements service was called
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args
            
            # Check URL
            assert "/species/detect" in call_args[1]["url"]
            
            # Check payload
            payload = call_args[1]["json"]
            assert payload["user_id"] == sample_sighting_data["user_id"]
            assert payload["species_name"] == sample_sighting_data["species_name"]
            assert payload["confidence"] == sample_sighting_data["confidence_score"]
            assert "location" in payload
            assert "detection_time" in payload
    
    def test_sighting_id_generation(self, client, sample_sighting_minimal, mock_achievements_service_success):
        """Test that sighting ID is generated for new sightings"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_achievements_service_success
            
            response = client.post("/sightings", json=sample_sighting_minimal)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] is not None
            assert isinstance(data["id"], int)
            assert data["id"] > 0