"""
Integration tests for achievements service
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...app.main import app, get_db
from ...app.infrastructure.database.config import Base


class TestAchievementsIntegration:
    """Integration tests with real database"""
    
    @pytest.fixture(scope="class")
    def test_db(self):
        """Create test database"""
        engine = create_engine("sqlite:///./test_integration.db")
        Base.metadata.create_all(bind=engine)
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        yield SessionLocal
        
        # Cleanup
        Base.metadata.drop_all(bind=engine)
    
    @pytest.fixture
    def client(self, test_db):
        """Create test client with real database"""
        def override_get_db():
            db = test_db()
            try:
                yield db
            finally:
                db.close()
        
        app.dependency_overrides[get_db] = override_get_db
        
        with TestClient(app) as test_client:
            yield test_client
        
        app.dependency_overrides.clear()
    
    def test_full_species_detection_flow(self, client):
        """Test complete species detection flow"""
        # Test data
        detection_data = {
            "user_id": 1,
            "species_name": "Colibrí Coliazul",
            "confidence": 0.95,
            "location": {
                "latitude": 10.4036,
                "longitude": -75.5144,
                "address": "Cartagena, Colombia"
            },
            "detection_time": "2023-10-21T10:30:00Z"
        }
        
        # Make request
        response = client.post("/species/detect", json=detection_data)
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "triggered_achievements" in data
        assert "species_detected" in data
    
    def test_batch_detection_integration(self, client):
        """Test batch detection integration"""
        batch_data = {
            "detections": [
                {
                    "user_id": 1,
                    "species_name": "Pelícano Pardo",
                    "confidence": 0.89,
                    "location": {
                        "latitude": 10.4036,
                        "longitude": -75.5144,
                        "address": "Cartagena Bay"
                    },
                    "detection_time": "2023-10-21T10:30:00Z"
                },
                {
                    "user_id": 1,
                    "species_name": "Gaviota Real",
                    "confidence": 0.92,
                    "location": {
                        "latitude": 10.4036,
                        "longitude": -75.5144,
                        "address": "Cartagena Beach"
                    },
                    "detection_time": "2023-10-21T10:35:00Z"
                }
            ]
        }
        
        response = client.post("/species/detect/batch", json=batch_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["total_processed"] == 2
    
    def test_service_health_check(self, client):
        """Test service health and availability"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Winged Achievements Service" in data["message"]