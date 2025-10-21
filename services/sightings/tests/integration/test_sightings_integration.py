"""
Integration tests for sightings service
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock

from ...app.main import app


class TestSightingsIntegration:
    """Integration tests for sightings service"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        with TestClient(app) as test_client:
            yield test_client
    
    def test_full_sighting_creation_flow(self, client):
        """Test complete sighting creation and achievement notification flow"""
        # Mock achievements service response
        mock_achievements = [
            {
                "id": 1,
                "name": "First Sighting",
                "description": "Record your first bird sighting",
                "xp_reward": 100
            }
        ]
        
        with patch('httpx.AsyncClient') as mock_async_client:
            # Setup mock response
            mock_client = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_achievements
            mock_client.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client
            
            # Test data
            sighting_data = {
                "user_id": 1,
                "species_name": "Turdus ignobilis",
                "common_name": "Black-billed Thrush",
                "confidence_score": 0.92,
                "location_lat": 10.4806,
                "location_lon": -75.5138,
                "audio_url": "https://example.com/audio.mp3"
            }
            
            # Make request
            response = client.post("/sightings", json=sighting_data)
            
            # Verify sighting creation
            assert response.status_code == 200
            data = response.json()
            assert data["id"] is not None
            assert data["species_name"] == "Turdus ignobilis"
            assert data["achievements_unlocked"] == mock_achievements
            
            # Verify achievements service was notified
            mock_client.post.assert_called_once()
    
    def test_sighting_retrieval_endpoints(self, client):
        """Test sighting retrieval endpoints"""
        # Test get sighting by ID
        response = client.get("/sightings/123")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 123
        
        # Test get user sightings
        response = client.get("/users/1/sightings")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 1
        assert isinstance(data["sightings"], list)
    
    def test_service_resilience_achievements_down(self, client):
        """Test service continues to work when achievements service is down"""
        with patch('httpx.AsyncClient') as mock_async_client:
            # Simulate achievements service being down
            mock_client = AsyncMock()
            mock_client.post.side_effect = Exception("Connection refused")
            mock_async_client.return_value.__aenter__.return_value = mock_client
            
            sighting_data = {
                "user_id": 1,
                "species_name": "Colibrí Coliazul",
                "confidence_score": 0.85,
                "location_lat": 10.4036,
                "location_lon": -75.5144
            }
            
            # Should still create sighting successfully
            response = client.post("/sightings", json=sighting_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] is not None
            assert data["achievements_unlocked"] == []  # No achievements due to service failure
    
    def test_concurrent_sighting_creation(self, client):
        """Test handling multiple concurrent sighting requests"""
        import concurrent.futures
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_client = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_client.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client
            
            def create_sighting(i):
                sighting_data = {
                    "user_id": i,
                    "species_name": f"Species_{i}",
                    "confidence_score": 0.8,
                    "location_lat": 10.0 + i * 0.01,
                    "location_lon": -75.0 + i * 0.01
                }
                return client.post("/sightings", json=sighting_data)
            
            # Create multiple sightings concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(create_sighting, i) for i in range(5)]
                responses = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            # All should succeed
            for response in responses:
                assert response.status_code == 200
    
    def test_sighting_validation_edge_cases(self, client):
        """Test sighting validation with edge cases"""
        test_cases = [
            # Valid edge cases
            {
                "data": {
                    "user_id": 1,
                    "species_name": "A",  # Single character
                    "confidence_score": 0.0,  # Minimum confidence
                    "location_lat": -90.0,  # Minimum latitude
                    "location_lon": -180.0   # Minimum longitude
                },
                "should_succeed": True
            },
            {
                "data": {
                    "user_id": 1,
                    "species_name": "Very Long Species Name That Contains Many Words",
                    "confidence_score": 1.0,  # Maximum confidence
                    "location_lat": 90.0,   # Maximum latitude
                    "location_lon": 180.0    # Maximum longitude
                },
                "should_succeed": True
            },
            # Invalid cases
            {
                "data": {
                    "user_id": 0,  # Invalid user ID
                    "species_name": "Test Bird",
                    "confidence_score": 0.5,
                    "location_lat": 0.0,
                    "location_lon": 0.0
                },
                "should_succeed": False
            }
        ]
        
        for test_case in test_cases:
            with patch('httpx.AsyncClient') as mock_async_client:
                mock_client = AsyncMock()
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = []
                mock_client.post.return_value = mock_response
                mock_async_client.return_value.__aenter__.return_value = mock_client
                
                response = client.post("/sightings", json=test_case["data"])
                
                if test_case["should_succeed"]:
                    assert response.status_code == 200
                else:
                    assert response.status_code == 422
    
    def test_achievements_service_timeout_handling(self, client):
        """Test proper handling of achievements service timeout"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_client = AsyncMock()
            # Simulate timeout
            import httpx
            mock_client.post.side_effect = httpx.TimeoutException("Request timeout")
            mock_async_client.return_value.__aenter__.return_value = mock_client
            
            sighting_data = {
                "user_id": 1,
                "species_name": "Timeout Test Bird",
                "confidence_score": 0.9,
                "location_lat": 10.0,
                "location_lon": -75.0
            }
            
            response = client.post("/sightings", json=sighting_data)
            
            # Should succeed despite timeout
            assert response.status_code == 200
            data = response.json()
            assert data["achievements_unlocked"] == []