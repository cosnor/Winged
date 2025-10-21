"""
Unit tests for ManageAchievements use case
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from ....app.application.use_cases.manage_achievements import ManageAchievementsUseCase
from ....app.domain.entities.achievement import Achievement
from ....app.domain.entities.user_achievement import UserAchievement


class TestManageAchievementsUseCase:
    """Test cases for ManageAchievements use case"""
    
    @pytest.fixture
    def mock_repository(self):
        """Mock achievement repository"""
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_repository):
        """Create use case instance with mocked repository"""
        return ManageAchievementsUseCase(mock_repository)
    
    def test_create_default_achievements(self, use_case, mock_repository):
        """Test creation of default achievements"""
        # Mock that no achievements exist yet
        mock_repository.get_all.return_value = []
        mock_repository.create.return_value = Mock(spec=Achievement, id=1)
        
        result = use_case.create_default_achievements()
        
        assert len(result) > 0  # Should create some default achievements
        assert mock_repository.create.call_count > 0
    
    def test_create_default_achievements_already_exist(self, use_case, mock_repository):
        """Test that default achievements are not created if they already exist"""
        # Mock that achievements already exist
        existing_achievement = Mock(spec=Achievement, id=1, name="First Bird")
        mock_repository.get_all.return_value = [existing_achievement]
        
        result = use_case.create_default_achievements()
        
        assert result == []  # Should not create new achievements
        mock_repository.create.assert_not_called()
    
    def test_process_species_detection_new_species(self, use_case, mock_repository):
        """Test processing species detection for new species"""
        user_id = 1
        species_name = "Colibrí Coliazul"
        confidence = 0.95
        location = {"latitude": 10.4036, "longitude": -75.5144}
        detection_time = datetime.utcnow()
        
        # Mock achievements that could be triggered
        first_bird_achievement = Mock(spec=Achievement, id=1, name="First Bird")
        hummingbird_achievement = Mock(spec=Achievement, id=2, name="Hummingbird Spotter")
        
        mock_repository.get_active_achievements.return_value = [
            first_bird_achievement,
            hummingbird_achievement
        ]
        
        # Mock user achievements (empty for new user)
        mock_repository.get_user_achievements.return_value = []
        
        # Mock criteria checking
        first_bird_achievement.is_criteria_met.return_value = True
        hummingbird_achievement.is_criteria_met.return_value = True
        
        result = use_case.process_species_detection(
            user_id, species_name, confidence, location, detection_time
        )
        
        assert len(result) == 2  # Should trigger both achievements
        assert mock_repository.create_user_achievement.call_count == 2
    
    def test_process_species_detection_existing_achievement(self, use_case, mock_repository):
        """Test that already earned achievements are not triggered again"""
        user_id = 1
        species_name = "Pelícano Pardo"
        confidence = 0.89
        location = {"latitude": 10.4036, "longitude": -75.5144}
        detection_time = datetime.utcnow()
        
        # Mock achievement
        first_bird_achievement = Mock(spec=Achievement, id=1, name="First Bird")
        mock_repository.get_active_achievements.return_value = [first_bird_achievement]
        
        # Mock that user already has this achievement
        existing_user_achievement = Mock(spec=UserAchievement, achievement_id=1)
        mock_repository.get_user_achievements.return_value = [existing_user_achievement]
        
        first_bird_achievement.is_criteria_met.return_value = True
        
        result = use_case.process_species_detection(
            user_id, species_name, confidence, location, detection_time
        )
        
        assert len(result) == 0  # Should not trigger already earned achievement
        mock_repository.create_user_achievement.assert_not_called()
    
    def test_process_species_detection_criteria_not_met(self, use_case, mock_repository):
        """Test that achievements are not triggered when criteria is not met"""
        user_id = 1
        species_name = "Unknown Bird"
        confidence = 0.45  # Low confidence
        location = {"latitude": 10.4036, "longitude": -75.5144}
        detection_time = datetime.utcnow()
        
        # Mock achievement with strict criteria
        expert_achievement = Mock(spec=Achievement, id=1, name="Expert Identifier")
        mock_repository.get_active_achievements.return_value = [expert_achievement]
        mock_repository.get_user_achievements.return_value = []
        
        # Mock that criteria is not met
        expert_achievement.is_criteria_met.return_value = False
        
        result = use_case.process_species_detection(
            user_id, species_name, confidence, location, detection_time
        )
        
        assert len(result) == 0
        mock_repository.create_user_achievement.assert_not_called()
    
    def test_get_user_achievements(self, use_case, mock_repository):
        """Test getting user achievements"""
        user_id = 1
        
        # Mock user achievements
        user_achievement1 = Mock(spec=UserAchievement, id=1, achievement_id=1)
        user_achievement2 = Mock(spec=UserAchievement, id=2, achievement_id=2)
        mock_repository.get_user_achievements.return_value = [user_achievement1, user_achievement2]
        
        result = use_case.get_user_achievements(user_id)
        
        assert len(result) == 2
        mock_repository.get_user_achievements.assert_called_once_with(user_id)
    
    def test_get_user_progress(self, use_case, mock_repository):
        """Test getting user progress towards achievements"""
        user_id = 1
        
        # Mock achievement
        achievement = Mock(spec=Achievement, id=1, name="Bird Collector")
        mock_repository.get_active_achievements.return_value = [achievement]
        
        # Mock user stats and collection
        achievement.calculate_progress.return_value = 0.6
        
        result = use_case.get_user_progress(user_id)
        
        assert len(result) > 0
        # Progress should be calculated for active achievements
    
    def test_process_species_detection_invalid_confidence(self, use_case, mock_repository):
        """Test processing species detection with invalid confidence score"""
        user_id = 1
        species_name = "Test Bird"
        confidence = 1.5  # Invalid confidence > 1.0
        location = {"latitude": 10.4036, "longitude": -75.5144}
        detection_time = datetime.utcnow()
        
        # Should handle invalid confidence gracefully
        result = use_case.process_species_detection(
            user_id, species_name, confidence, location, detection_time
        )
        
        # Implementation may vary - might return empty result or raise exception
        assert isinstance(result, list)


class TestManageAchievementsUseCaseIntegration:
    """Integration tests for ManageAchievements use case with real scenarios"""
    
    @pytest.fixture
    def mock_repository(self):
        """Mock repository with more realistic behavior"""
        repository = Mock()
        
        # Default achievements
        repository.get_all.return_value = []
        
        # Active achievements that could be triggered
        first_bird = Mock(spec=Achievement, id=1, name="First Bird", category="discovery")
        hummingbird_spotter = Mock(spec=Achievement, id=2, name="Hummingbird Spotter", category="family")
        seabird_enthusiast = Mock(spec=Achievement, id=3, name="Seabird Enthusiast", category="family")
        
        repository.get_active_achievements.return_value = [
            first_bird, hummingbird_spotter, seabird_enthusiast
        ]
        
        return repository
    
    @pytest.fixture
    def use_case(self, mock_repository):
        """Create use case with realistic mock repository"""
        return ManageAchievementsUseCase(mock_repository)
    
    def test_hummingbird_detection_scenario(self, use_case, mock_repository):
        """Test realistic hummingbird detection scenario"""
        user_id = 1
        species_name = "Colibrí Coliazul"
        confidence = 0.92
        location = {"latitude": 10.4036, "longitude": -75.5144, "address": "Cartagena"}
        detection_time = datetime.utcnow()
        
        # New user - no achievements yet
        mock_repository.get_user_achievements.return_value = []
        
        # Configure achievement criteria
        first_bird = mock_repository.get_active_achievements.return_value[0]
        hummingbird_spotter = mock_repository.get_active_achievements.return_value[1]
        seabird_enthusiast = mock_repository.get_active_achievements.return_value[2]
        
        # First bird and hummingbird achievements should trigger
        first_bird.is_criteria_met.return_value = True
        hummingbird_spotter.is_criteria_met.return_value = True
        seabird_enthusiast.is_criteria_met.return_value = False  # Not a seabird
        
        result = use_case.process_species_detection(
            user_id, species_name, confidence, location, detection_time
        )
        
        assert len(result) == 2  # First Bird + Hummingbird Spotter
        assert mock_repository.create_user_achievement.call_count == 2
    
    def test_batch_species_detection_scenario(self, use_case, mock_repository):
        """Test processing multiple species detections in sequence"""
        user_id = 1
        detections = [
            ("Colibrí Coliazul", 0.95),
            ("Pelícano Pardo", 0.89),
            ("Gaviota Real", 0.92)
        ]
        
        location = {"latitude": 10.4036, "longitude": -75.5144}
        detection_time = datetime.utcnow()
        
        # Start with no achievements
        mock_repository.get_user_achievements.return_value = []
        
        total_triggered = []
        
        for species_name, confidence in detections:
            result = use_case.process_species_detection(
                user_id, species_name, confidence, location, detection_time
            )
            total_triggered.extend(result)
            
            # Update mock to include newly earned achievements
            # (In real scenario, repository would persist these)
        
        # Should have triggered multiple achievements across different species
        assert len(total_triggered) > 0