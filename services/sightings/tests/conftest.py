"""
Test configuration and fixtures for sightings service tests
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch

from ..app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the sightings service."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_sighting_data():
    """Sample sighting creation data for testing."""
    return {
        "user_id": 1,
        "species_name": "Turdus ignobilis", 
        "common_name": "Black-billed Thrush",
        "confidence_score": 0.92,
        "location_lat": 10.4806,
        "location_lon": -75.5138,
        "timestamp": "2023-10-21T10:30:00Z",
        "audio_url": "https://example.com/audio.mp3",
        "image_url": "https://example.com/image.jpg"
    }


@pytest.fixture
def sample_sighting_minimal():
    """Minimal required sighting data for testing."""
    return {
        "user_id": 1,
        "species_name": "Colibrí Coliazul",
        "confidence_score": 0.85,
        "location_lat": 10.4036,
        "location_lon": -75.5144
    }


@pytest.fixture
def mock_achievements_response():
    """Mock response from achievements service."""
    return [
        {
            "id": 1,
            "name": "First Sighting",
            "description": "Record your first bird sighting",
            "xp_reward": 100
        },
        {
            "id": 2,
            "name": "Thrush Spotter",
            "description": "Identify a thrush species",
            "xp_reward": 50
        }
    ]


@pytest.fixture
def mock_httpx_client():
    """Mock httpx client for external service calls."""
    return AsyncMock()


# Mock external dependencies
@pytest.fixture
def mock_achievements_service_success(mock_httpx_client, mock_achievements_response):
    """Mock successful achievements service response."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_achievements_response
    mock_httpx_client.post.return_value = mock_response
    return mock_httpx_client


@pytest.fixture
def mock_achievements_service_failure(mock_httpx_client):
    """Mock failed achievements service response."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_httpx_client.post.return_value = mock_response
    return mock_httpx_client


@pytest.fixture
def mock_achievements_service_timeout(mock_httpx_client):
    """Mock achievements service timeout."""
    mock_httpx_client.post.side_effect = Exception("Connection timeout")
    return mock_httpx_client