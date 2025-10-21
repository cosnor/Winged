"""
Unit tests for update user XP endpoint
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import status
from domain.exceptions.user_exceptions import UserNotFoundError


class TestUpdateUserXP:
    """Tests for the update user XP endpoint"""
    
    def test_update_user_xp_success(self, client, sample_user_dict):
        """Test successful XP update"""
        # Mock updated user response
        updated_user = {
            "user_id": 1,
            "email": "test@example.com",
            "level": 3,  # Level increased due to XP gain
            "xp": 250,   # XP increased
            "is_active": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T01:00:00"
        }
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.UpdateUserXpUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_response = Mock()
            mock_response.user_id = updated_user["user_id"]
            mock_response.email = updated_user["email"]
            mock_response.level = updated_user["level"]
            mock_response.xp = updated_user["xp"]
            mock_response.is_active = updated_user["is_active"]
            mock_response.created_at = updated_user["created_at"]
            mock_response.updated_at = updated_user["updated_at"]
            
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request with query parameter
            response = client.patch("/users/1/xp?xp_to_add=150")
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["message"] == "User XP updated (+150)"
            assert data["data"]["user_id"] == 1
            assert data["data"]["level"] == 3
            assert data["data"]["xp"] == 250
            
            # Verify use case was called with correct parameters
            mock_use_case_instance.execute.assert_called_once_with(
                mock_use_case_instance.execute.call_args[0][0]  # domain request object
            )
    
    def test_update_user_xp_user_not_found(self, client):
        """Test XP update when user doesn't exist"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.UpdateUserXpUseCase') as mock_use_case:
            
            # Setup mocks to raise UserNotFoundError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = UserNotFoundError("User with ID 999 not found")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request with query parameter
            response = client.patch("/users/999/xp?xp_to_add=100")
            
            # Assertions
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "User with ID 999 not found" in data["detail"]
    
    def test_update_user_xp_invalid_user_id(self, client):
        """Test XP update with invalid user ID format"""
        # Make request with invalid ID
        response = client.patch("/users/invalid/xp?xp_to_add=100")
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_user_xp_negative_user_id(self, client):
        """Test XP update with negative user ID"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.UpdateUserXpUseCase') as mock_use_case:
            
            # Setup mocks to raise UserNotFoundError
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = UserNotFoundError("User with ID -1 not found")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.patch("/users/-1/xp?xp_to_add=100")
            
            # Assertions
            assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_user_xp_missing_xp_to_add_parameter(self, client):
        """Test XP update without xp_to_add query parameter"""
        # Make request without query parameter
        response = client.patch("/users/1/xp")
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "Field required" in str(data["detail"])
    
    def test_update_user_xp_invalid_xp_to_add_type(self, client):
        """Test XP update with invalid xp_to_add type"""
        # Make request with string instead of int
        response = client.patch("/users/1/xp?xp_to_add=invalid")
        
        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_user_xp_negative_xp_gain(self, client, sample_user_dict):
        """Test XP update with negative XP gain"""
        # Mock user response
        updated_user = {
            "user_id": 1,
            "email": "test@example.com",
            "level": 1,
            "xp": 50,  # XP decreased
            "is_active": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T01:00:00"
        }
        
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.UpdateUserXpUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_response = Mock()
            mock_response.user_id = updated_user["user_id"]
            mock_response.email = updated_user["email"]
            mock_response.level = updated_user["level"]
            mock_response.xp = updated_user["xp"]
            mock_response.is_active = updated_user["is_active"]
            mock_response.created_at = updated_user["created_at"]
            mock_response.updated_at = updated_user["updated_at"]
            
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request with negative XP value
            response = client.patch("/users/1/xp?xp_to_add=-50")
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["data"]["xp"] == 50
            assert data["message"] == "User XP updated (+-50)"
    
    def test_update_user_xp_zero_xp_gain(self, client, sample_user_dict):
        """Test XP update with zero XP gain"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.UpdateUserXpUseCase') as mock_use_case:
            
            # Setup mocks
            mock_use_case_instance = Mock()
            mock_response = Mock()
            mock_response.user_id = 1
            mock_response.email = "test@example.com"
            mock_response.level = 2
            mock_response.xp = 100  # XP unchanged
            mock_response.is_active = True
            mock_response.created_at = "2023-01-01T00:00:00"
            mock_response.updated_at = "2023-01-01T01:00:00"
            
            mock_use_case_instance.execute.return_value = mock_response
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request with zero XP value
            response = client.patch("/users/1/xp?xp_to_add=0")
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["data"]["xp"] == 100
            assert data["message"] == "User XP updated (+0)"
    
    def test_update_user_xp_internal_error(self, client):
        """Test XP update with internal server error"""
        with patch('presentation.controllers.user_controller.get_user_repository') as mock_repo, \
             patch('presentation.controllers.user_controller.UpdateUserXpUseCase') as mock_use_case:
            
            # Setup mocks to raise generic exception
            mock_use_case_instance = Mock()
            mock_use_case_instance.execute.side_effect = Exception("Database error")
            mock_use_case.return_value = mock_use_case_instance
            
            # Make request
            response = client.patch("/users/1/xp?xp_to_add=100")
            
            # Assertions
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.json()
            assert data["detail"] == "Failed to update user XP"