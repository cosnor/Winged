"""
Unit tests for user login endpoint
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import status
from domain.exceptions.user_exceptions import InvalidCredentialsError


class TestLoginUser:
    """Tests for the login user endpoint"""
    
    def test_login_user_success(self, client, login_request_data):
        """Test successful user login"""
        # Mock response from use case
        mock_response = Mock()
        mock_response.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"
        mock_response.token_type = "Bearer"
        mock_response.expires_in = 3600
        mock_response.user_info = {
            "user_id": 1,
            "email": "test@example.com",
            "level": 2,
            "xp": 100,
            "is_active": True,
            "created_at": "2025-10-20T15:30:00"
        }
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.AuthenticateUserUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/login", json=login_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["message"] == "Login successful"
            assert data["access_token"] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"
            assert data["token_type"] == "Bearer"
            assert data["expires_in"] == 3600
            assert data["user_info"]["user_id"] == 1
            assert data["user_info"]["email"] == "test@example.com"
    
    def test_login_user_invalid_credentials(self, client, login_request_data):
        """Test login with invalid credentials"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.AuthenticateUserUseCase') as mock_use_case:
            
            # Setup mocks to raise InvalidCredentialsError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = InvalidCredentialsError("Invalid email or password")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/login", json=login_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            data = response.json()
            assert "Invalid email or password" in data["detail"]
    
    def test_login_user_missing_email(self, client):
        """Test login with missing email"""
        invalid_data = {
            "password": "password123"
        }
        
        response = client.post("/login", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_user_missing_password(self, client):
        """Test login with missing password"""
        invalid_data = {
            "email": "test@example.com"
        }
        
        response = client.post("/login", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_user_invalid_email_format(self, client):
        """Test login with invalid email format"""
        invalid_data = {
            "email": "invalid_email",
            "password": "password123"
        }
        
        response = client.post("/login", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_user_internal_error(self, client, login_request_data):
        """Test login with internal server error"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.AuthenticateUserUseCase') as mock_use_case:
            
            # Setup mocks to raise generic exception
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = Exception("Database error")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/login", json=login_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.json()
            assert data["detail"] == "Login failed"
    
    def test_login_user_empty_credentials(self, client):
        """Test login with empty credentials"""
        invalid_data = {
            "email": "",
            "password": ""
        }
        
        response = client.post("/login", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_user_whitespace_credentials(self, client):
        """Test login with whitespace-only credentials"""
        invalid_data = {
            "email": "   ",
            "password": "   "
        }
        
        response = client.post("/login", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY