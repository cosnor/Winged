"""
Unit tests for user profile endpoints
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import status
from domain.exceptions.user_exceptions import UserNotFoundError


class TestGetUserProfile:
    """Tests for the get user profile endpoint"""
    
    def test_get_user_profile_success(self, client, sample_user_dict):
        """Test successful profile retrieval with valid token"""
        from presentation.dependencies.auth_dependency import get_current_user
        
        # Override the dependency to return our sample user
        def override_get_current_user():
            return sample_user_dict
        
        client.app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Make request with Authorization header
            headers = {"Authorization": "Bearer valid_jwt_token"}
            response = client.get("/profile", headers=headers)
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["message"] == "Profile retrieved successfully"
            assert data["data"]["user_id"] == 1
            assert data["data"]["email"] == "test@example.com"
            assert data["data"]["level"] == 2
            assert data["data"]["xp"] == 100
            assert data["data"]["is_active"] is True
        finally:
            # Clean up dependency override
            client.app.dependency_overrides.clear()
    
    def test_get_user_profile_missing_token(self, client):
        """Test profile retrieval without Authorization header"""
        # Make request without Authorization header
        response = client.get("/profile")
        
        # Should return 403 Forbidden (FastAPI HTTPBearer default)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert data["detail"] == "Not authenticated"
    
    def test_get_user_profile_invalid_token(self, client, http_exception):
        """Test profile retrieval with invalid token"""        
        from presentation.dependencies.auth_dependency import get_current_user
        
        # Override the dependency to raise HTTPException for invalid token
        def override_get_current_user():
            raise http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token"
            )
        
        client.app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Make request with invalid token
            headers = {"Authorization": "Bearer invalid_token"}
            response = client.get("/profile", headers=headers)
            
            # Assertions
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            data = response.json()
            assert data["detail"] == "Invalid token"
        finally:
            # Clean up dependency override
            client.app.dependency_overrides.clear()
    
    def test_get_user_profile_malformed_header(self, client):
        """Test profile retrieval with malformed Authorization header"""
        # Make request with malformed header (missing Bearer)
        headers = {"Authorization": "invalid_format_token"}
        response = client.get("/profile", headers=headers)
        
        # Should return 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_user_profile_internal_error(self, client, sample_user_dict):
        """Test profile retrieval with internal error"""
        from presentation.dependencies.auth_dependency import get_current_user
        
        # Override the dependency to return malformed user data that will cause error in controller
        def override_get_current_user():
            # Return user data missing required fields to trigger error in controller
            return {
                "user_id": 1,
                "email": "test@example.com",
                # Missing level, xp, is_active fields to cause KeyError
            }
        
        client.app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Make request with valid header format
            headers = {"Authorization": "Bearer valid_token"}
            response = client.get("/profile", headers=headers)
            
            # Assertions
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.json()
            assert data["detail"] == "Failed to retrieve profile"
        finally:
            # Clean up dependency override
            client.app.dependency_overrides.clear()


class TestGetUserById:
    """Tests for the get user by ID endpoint"""
    
    def test_get_user_by_id_success(self, client):
        """Test successful user retrieval by ID"""
        # Mock response from use case
        mock_response = Mock()
        mock_response.user_id = 1
        mock_response.name = "Test User"
        mock_response.email = "test@example.com"
        mock_response.level = 2
        mock_response.xp = 100
        mock_response.is_active = True
        mock_response.created_at = "2025-10-20T15:30:00"
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.GetUserByIdUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.get("/users/1")
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["message"] == "User found"
            assert data["data"]["user_id"] == 1
            assert data["data"]["name"] == "Test User"
            assert data["data"]["email"] == "test@example.com"
            assert data["data"]["level"] == 2
            assert data["data"]["xp"] == 100
            assert data["data"]["is_active"] is True
    
    def test_get_user_by_id_not_found(self, client):
        """Test user retrieval by ID when user doesn't exist"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.GetUserByIdUseCase') as mock_use_case:
            
            # Setup mocks to raise UserNotFoundError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = UserNotFoundError("User with ID 999 not found")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.get("/users/999")
            
            # Assertions
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "User with ID 999 not found" in data["detail"]
    
    def test_get_user_by_id_invalid_id(self, client):
        """Test user retrieval with invalid ID format"""
        # Make request with invalid ID
        response = client.get("/users/invalid")
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_user_by_id_negative_id(self, client):
        """Test user retrieval with negative ID"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.GetUserByIdUseCase') as mock_use_case:
            
            # Setup mocks to raise UserNotFoundError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = UserNotFoundError("User with ID -1 not found")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.get("/users/-1")
            
            # Assertions
            assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_user_by_id_internal_error(self, client):
        """Test user retrieval by ID with internal server error"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.GetUserByIdUseCase') as mock_use_case:
            
            # Setup mocks to raise generic exception
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = Exception("Database error")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.get("/users/1")
            
            # Assertions
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.json()
            assert data["detail"] == "Failed to retrieve user"