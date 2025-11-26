"""
Test configuration and fixtures for achievements service tests
"""

import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import Mock

# Import application components
from ..app.main import app, get_db, get_current_user
from ..app.infrastructure.database.config import Base
from ..app.infrastructure.database.repositories import SQLAlchemyAchievementRepository
from ..app.application.use_cases.manage_achievements import ManageAchievementsUseCase


# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test_achievements.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session for each test function."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def override_get_db(db_session):
    """Override the get_db dependency to use test database."""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    return _override_get_db


@pytest.fixture
def mock_current_user():
    """Mock current user for authentication testing."""
    return {
        "user_id": 1,
        "username": "test_user",
        "email": "test@example.com"
    }


@pytest.fixture
def override_get_current_user(mock_current_user):
    """Override the get_current_user dependency."""
    def _override_get_current_user():
        return mock_current_user
    return _override_get_current_user


@pytest.fixture
def client(override_get_db, override_get_current_user):
    """Create a test client with overridden dependencies."""
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up overrides
    app.dependency_overrides.clear()


@pytest.fixture
def achievement_repository(db_session):
    """Create an achievement repository instance for testing."""
    return SQLAlchemyAchievementRepository(db_session)


@pytest.fixture
def manage_achievements_use_case(achievement_repository):
    """Create a manage achievements use case for testing."""
    return ManageAchievementsUseCase(achievement_repository)


@pytest.fixture
def sample_species_detection():
    """Sample species detection data for testing."""
    return {
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


@pytest.fixture
def sample_batch_detection():
    """Sample batch species detection data for testing."""
    return {
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


# Mock external services
@pytest.fixture
def mock_ml_worker_client():
    """Mock ML Worker service client."""
    mock = Mock()
    mock.process_detection.return_value = {"success": True, "species_confirmed": True}
    return mock


@pytest.fixture
def mock_sightings_client():
    """Mock Sightings service client."""
    mock = Mock()
    mock.create_sighting.return_value = {"sighting_id": 123, "success": True}
    return mock