"""
Unit tests for Achievements API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json

from ....app.main import app


class TestAchievementsAPI:
    """Test cases for achievements API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Winged Achievements Service"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"


class TestSpeciesDetectionEndpoints:
    """Test cases for species detection endpoints"""
    
    def test_species_detect_success(self, client, sample_species_detection):
        """Test successful species detection"""
        with patch('services.achievements.app.main.SQLAlchemyAchievementRepository') as mock_repo_class, \
             patch('services.achievements.app.main.ManageAchievementsUseCase') as mock_use_case_class:
            
            # Mock repository and use case
            mock_repo = Mock()
            mock_use_case = Mock()
            mock_repo_class.return_value = mock_repo
            mock_use_case_class.return_value = mock_use_case
            
            # Mock achievement result
            mock_achievement = Mock()
            mock_achievement.id = 1
            mock_achievement.title = "First Bird"
            mock_achievement.description = "Identify your first bird"
            mock_achievement.achievement_type = "discovery"
            mock_achievement.category = "milestone"
            
            mock_use_case.process_species_detection.return_value = [mock_achievement]
            
            response = client.post("/species/detect", json=sample_species_detection)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "Colibrí Coliazul" in data["message"]
            assert len(data["triggered_achievements"]) == 1
            assert data["species_detected"]["name"] == "Colibrí Coliazul"
    
    def test_species_detect_invalid_data(self, client):
        """Test species detection with invalid data"""
        invalid_data = {
            "user_id": "invalid",  # Should be int
            "species_name": "",    # Empty string
            "confidence": 1.5,     # Invalid confidence > 1.0
        }
        
        response = client.post("/species/detect", json=invalid_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_species_detect_missing_required_fields(self, client):
        """Test species detection with missing required fields"""
        incomplete_data = {
            "user_id": 1,
            # Missing required fields
        }
        
        response = client.post("/species/detect", json=incomplete_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_species_detect_service_error(self, client, sample_species_detection):
        """Test species detection when service throws error"""
        with patch('services.achievements.app.main.SQLAlchemyAchievementRepository') as mock_repo_class, \
             patch('services.achievements.app.main.ManageAchievementsUseCase') as mock_use_case_class:
            
            mock_repo_class.return_value = Mock()
            mock_use_case = Mock()
            mock_use_case_class.return_value = mock_use_case
            
            # Mock service error
            mock_use_case.process_species_detection.side_effect = Exception("Database error")
            
            response = client.post("/species/detect", json=sample_species_detection)
            
            assert response.status_code == 200  # Still returns 200 but with error in response
            data = response.json()
            assert data["success"] is False
            assert "error" in data["message"].lower()
    
    def test_batch_species_detect_success(self, client, sample_batch_detection):
        """Test successful batch species detection"""
        with patch('services.achievements.app.main.SQLAlchemyAchievementRepository') as mock_repo_class, \
             patch('services.achievements.app.main.ManageAchievementsUseCase') as mock_use_case_class:
            
            mock_repo = Mock()
            mock_use_case = Mock()
            mock_repo_class.return_value = mock_repo
            mock_use_case_class.return_value = mock_use_case
            
            # Mock different achievements for each detection
            mock_achievement1 = Mock()
            mock_achievement1.id = 1
            mock_achievement1.title = "Seabird Spotter"
            mock_achievement1.description = "Identify a seabird"
            mock_achievement1.achievement_type = "family"
            mock_achievement1.category = "discovery"
            
            mock_achievement2 = Mock()
            mock_achievement2.id = 2
            mock_achievement2.title = "Beach Explorer"
            mock_achievement2.description = "Find birds at the beach"
            mock_achievement2.achievement_type = "location"
            mock_achievement2.category = "exploration"
            
            # Return different achievements for each detection
            mock_use_case.process_species_detection.side_effect = [
                [mock_achievement1],  # First detection
                [mock_achievement2]   # Second detection
            ]
            
            response = client.post("/species/detect/batch", json=sample_batch_detection)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["total_processed"] == 2
            assert data["total_achievements_triggered"] == 2
            assert len(data["processed_detections"]) == 2
    
    def test_batch_species_detect_partial_success(self, client, sample_batch_detection):
        """Test batch species detection with some failures"""
        with patch('services.achievements.app.main.SQLAlchemyAchievementRepository') as mock_repo_class, \
             patch('services.achievements.app.main.ManageAchievementsUseCase') as mock_use_case_class:
            
            mock_repo_class.return_value = Mock()
            mock_use_case = Mock()
            mock_use_case_class.return_value = mock_use_case
            
            # Mock first detection success, second fails
            mock_achievement = Mock()
            mock_achievement.id = 1
            mock_achievement.title = "Test Achievement"
            mock_achievement.description = "Test description"
            mock_achievement.achievement_type = "test"
            mock_achievement.category = "test"
            
            mock_use_case.process_species_detection.side_effect = [
                [mock_achievement],           # First succeeds
                Exception("Service error")   # Second fails
            ]
            
            response = client.post("/species/detect/batch", json=sample_batch_detection)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True  # Overall success even with partial failures
            assert data["total_processed"] == 2
            assert len(data["processed_detections"]) == 2
            
            # Check that one succeeded and one failed
            success_count = sum(1 for d in data["processed_detections"] if d.get("success", False))
            assert success_count == 1
    
    def test_batch_species_detect_empty_list(self, client):
        """Test batch species detection with empty detection list"""
        empty_batch = {"detections": []}
        
        response = client.post("/species/detect/batch", json=empty_batch)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_processed"] == 0
        assert data["total_achievements_triggered"] == 0


class TestAchievementSchemas:
    """Test cases for achievement request/response schemas"""
    
    def test_species_detection_request_validation(self):
        """Test SpeciesDetectionRequest validation"""
        from ....app.presentation.schemas.requests import SpeciesDetectionRequest
        from datetime import datetime
        
        # Valid request
        valid_data = {
            "user_id": 1,
            "species_name": "Colibrí Coliazul",
            "confidence": 0.95,
            "location": {
                "latitude": 10.4036,
                "longitude": -75.5144,
                "address": "Cartagena, Colombia"
            },
            "detection_time": datetime.utcnow()
        }
        
        request = SpeciesDetectionRequest(**valid_data)
        assert request.user_id == 1
        assert request.species_name == "Colibrí Coliazul"
        assert request.confidence == 0.95
    
    def test_species_detection_request_invalid_confidence(self):
        """Test SpeciesDetectionRequest with invalid confidence"""
        from ....app.presentation.schemas.requests import SpeciesDetectionRequest
        from pydantic import ValidationError
        from datetime import datetime
        
        invalid_data = {
            "user_id": 1,
            "species_name": "Test Bird",
            "confidence": 1.5,  # Invalid: > 1.0
            "location": {
                "latitude": 10.4036,
                "longitude": -75.5144,
                "address": "Test Location"
            },
            "detection_time": datetime.utcnow()
        }
        
        with pytest.raises(ValidationError):
            SpeciesDetectionRequest(**invalid_data)
    
    def test_species_detection_response_creation(self):
        """Test SpeciesDetectionResponse creation"""
        from ....app.presentation.schemas.responses import SpeciesDetectionResponse
        
        response = SpeciesDetectionResponse(
            success=True,
            message="Detection processed successfully",
            triggered_achievements=[
                {
                    "id": 1,
                    "title": "First Bird",
                    "description": "Identify your first bird",
                    "type": "discovery",
                    "category": "milestone"
                }
            ],
            species_detected={
                "name": "Colibrí Coliazul",
                "confidence": 0.95,
                "location": {"latitude": 10.4036, "longitude": -75.5144},
                "timestamp": "2023-10-21T10:30:00Z"
            }
        )
        
        assert response.success is True
        assert len(response.triggered_achievements) == 1
        assert response.species_detected["name"] == "Colibrí Coliazul"