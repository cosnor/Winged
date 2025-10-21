"""
Unit tests for token validation endpoint
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import status
from datetime import datetime, timezone
from domain.exceptions.user_exceptions import InvalidTokenError


class TestValidateToken:
    """Tests for the validate token endpoint"""
    
    def test_validate_token_success(self, client, validate_token_request_data):
        """Test successful token validation"""
        # Mock response from use case
        mock_response = Mock()
        mock_response.is_valid = True
        mock_response.user_id = 1
        mock_response.email = "test@example.com"
        mock_response.level = 2
        mock_response.xp = 100
        mock_response.is_active = True
        mock_response.created_at = "2025-10-20T15:30:00"
        mock_response.expires_at = datetime.now(timezone.utc)
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.ValidateTokenUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/validate-token", json=validate_token_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["is_valid"] is True
            assert data["user_info"]["user_id"] == 1
            assert data["user_info"]["email"] == "test@example.com"
            assert data["token_type"] == "Bearer"
            assert "expires_at" in data
    
    def test_validate_token_invalid(self, client, validate_token_request_data):
        """Test validation of invalid token"""
        # Mock response from use case
        mock_response = Mock()
        mock_response.is_valid = False
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.ValidateTokenUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/validate-token", json=validate_token_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["is_valid"] is False
            assert data["error"] == "Invalid or expired token"
    
    def test_validate_token_exception(self, client, validate_token_request_data):
        """Test token validation with InvalidTokenError exception"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.ValidateTokenUseCase') as mock_use_case:
            
            # Setup mocks to raise InvalidTokenError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = InvalidTokenError("Token expired")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/validate-token", json=validate_token_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["is_valid"] is False
            assert data["error"] == "Token expired"
    
    def test_validate_token_missing_token(self, client):
        """Test validation with missing token"""
        invalid_data = {}
        
        response = client.post("/validate-token", json=invalid_data)
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_validate_token_empty_token(self, client):
        """Test validation with empty token"""
        invalid_data = {
            "token": ""
        }
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.ValidateTokenUseCase') as mock_use_case:
            
            # Setup mocks for empty token - should return invalid
            mock_use_case_instance = Mock()
            mock_response = Mock()
            mock_response.is_valid = False
            mock_response.error = "Invalid token format"
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            response = client.post("/validate-token", json=invalid_data)
            
            # Should return 200 with is_valid=False for empty token
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["is_valid"] is False
            assert "error" in data
    
    def test_validate_token_malformed_token(self, client):
        """Test validation with malformed token"""
        invalid_data = {
            "token": "invalid.token.format"
        }
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.ValidateTokenUseCase') as mock_use_case:
            
            # Setup mocks to raise InvalidTokenError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = InvalidTokenError("Malformed token")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/validate-token", json=invalid_data)
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["is_valid"] is False
            assert data["error"] == "Malformed token"
    
    def test_validate_token_internal_error(self, client, validate_token_request_data):
        """Test token validation with internal server error"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.get_auth_service') as mock_auth, \
             patch('presentation.controllers.user_controller.ValidateTokenUseCase') as mock_use_case:
            
            # Setup mocks to raise generic exception
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = Exception("Database error")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.post("/validate-token", json=validate_token_request_data)
            
            # Assertions
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.json()
            assert data["detail"] == "Token validation failed"