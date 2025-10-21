"""
Test configuration and fixtures for the users service
"""
import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from fastapi import FastAPI

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.auth.jwt_handler import JWTAuthService
from presentation.controllers.user_controller import router


@pytest.fixture
def app():
    """Create FastAPI app for testing"""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture
def mock_user_repository():
    """Mock user repository"""
    return Mock(spec=UserRepository)


@pytest.fixture
def mock_auth_service():
    """Mock auth service"""
    return Mock(spec=JWTAuthService)


@pytest.fixture
def sample_user():
    """Sample user entity for testing"""
    return User(
        id=1,
        email="test@example.com",
        password_hash="hashed_password",
        xp=100,
        level=2,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def sample_user_dict():
    """Sample user data as dictionary"""
    return {
        "user_id": 1,
        "email": "test@example.com",
        "level": 2,
        "xp": 100,
        "is_active": True
    }


@pytest.fixture
def http_exception():
    """HTTPException class for testing"""
    from fastapi import HTTPException
    return HTTPException


@pytest.fixture
def valid_jwt_token():
    """Valid JWT token for testing"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIn0.test_token"


@pytest.fixture
def register_request_data():
    """Sample registration request data"""
    return {
        "email": "newuser@example.com",
        "password": "password123"
    }


@pytest.fixture
def login_request_data():
    """Sample login request data"""
    return {
        "email": "test@example.com",
        "password": "password123"
    }


@pytest.fixture
def validate_token_request_data():
    """Sample validate token request data"""
    return {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"
    }