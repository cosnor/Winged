"""
Unit tests for user registration endpoint
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import status
from domain.exceptions.user_exceptions import EmailAlreadyExistsError
from domain.use_cases.register_user import RegisterUserResponse


class TestRegisterUser:
    """Tests for the register user endpoint"""
    
    def test_register_user_success(self, client, register_request_data):
        """Test successful user registration"""
        # Mock response from use case
        mock_response = Mock()
        mock_response.user_id = 1
        mock_response.name = "New User"
        mock_response.email = "newuser@example.com"
        mock_response.level = 1
        mock_response.xp = 0
        mock_response.is_active = True
        mock_response.created_at = "2025-10-20T15:30:00"
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.RegisterUserUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/register", json=register_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["success"] is True
            assert data["message"] == "User registered successfully"
            assert data["data"]["user_id"] == 1
            assert data["data"]["name"] == "New User"
            assert data["data"]["email"] == "newuser@example.com"
            assert data["data"]["level"] == 1
            assert data["data"]["xp"] == 0
            assert data["data"]["is_active"] is True
    
    def test_register_user_email_already_exists(self, client, register_request_data):
        """Test registration with existing email"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.RegisterUserUseCase') as mock_use_case:
            
            # Setup mocks to raise EmailAlreadyExistsError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = EmailAlreadyExistsError("Email already exists")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/register", json=register_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_409_CONFLICT
            data = response.json()
            assert "Email already exists" in data["detail"]
    
    def test_register_user_invalid_email_format(self, client):
        """Test registration with invalid email format"""
        invalid_data = {
            "email": "invalid_email",
            "password": "password123"
        }
        
        response = client.post("/register", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_user_missing_password(self, client):
        """Test registration with missing password"""
        invalid_data = {
            "email": "test@example.com"
        }
        
        response = client.post("/register", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_user_empty_password(self, client):
        """Test registration with empty password"""
        invalid_data = {
            "email": "test@example.com",
            "password": ""
        }
        
        response = client.post("/register", json=invalid_data)
        
        # Should return validation error  
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_user_internal_error(self, client, register_request_data):
        """Test registration with internal server error"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.RegisterUserUseCase') as mock_use_case:
            
            # Setup mocks to raise generic exception
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = Exception("Database error")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/register", json=register_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.json()
            assert data["detail"] == "Registration failed"
    
    def test_register_user_request_validation(self, client):
        """Test registration request validation"""
        # Test with missing email
        response = client.post("/register", json={"password": "test123"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test with missing password
        response = client.post("/register", json={"email": "test@example.com"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test with empty body
        response = client.post("/register", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY