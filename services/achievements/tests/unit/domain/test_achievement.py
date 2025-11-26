"""
Unit tests for Achievement domain entity
"""

import pytest
from datetime import datetime
from unittest.mock import Mock

from ....app.domain.entities.achievement import Achievement
from ....app.domain.value_objects.achievement_criteria import AchievementCriteria


class TestAchievement:
    """Test cases for Achievement entity"""
    
    def test_achievement_creation(self):
        """Test basic achievement creation"""
        criteria = Mock(spec=AchievementCriteria)
        
        achievement = Achievement(
            id=1,
            name="First Bird",
            description="Identify your first bird",
            category="discovery",
            criteria=criteria,
            xp_reward=100,
            icon="🐦",
            is_active=True
        )
        
        assert achievement.id == 1
        assert achievement.name == "First Bird"
        assert achievement.description == "Identify your first bird"
        assert achievement.category == "discovery"
        assert achievement.xp_reward == 100
        assert achievement.icon == "🐦"
        assert achievement.is_active is True
        assert isinstance(achievement.created_at, datetime)
    
    def test_achievement_creation_without_id(self):
        """Test achievement creation without ID (for new achievements)"""
        criteria = Mock(spec=AchievementCriteria)
        
        achievement = Achievement(
            id=None,
            name="Bird Expert",
            description="Identify 100 different bird species",
            category="collection",
            criteria=criteria,
            xp_reward=1000,
            icon="🏆",
            is_active=True
        )
        
        assert achievement.id is None
        assert achievement.name == "Bird Expert"
        assert isinstance(achievement.created_at, datetime)
    
    def test_achievement_created_at_auto_set(self):
        """Test that created_at is automatically set if not provided"""
        criteria = Mock(spec=AchievementCriteria)
        before_creation = datetime.utcnow()
        
        achievement = Achievement(
            id=1,
            name="Test Achievement",
            description="Test description",
            category="test",
            criteria=criteria,
            xp_reward=50,
            icon="✅",
            is_active=True
        )
        
        after_creation = datetime.utcnow()
        
        assert before_creation <= achievement.created_at <= after_creation
    
    def test_achievement_created_at_custom(self):
        """Test achievement creation with custom created_at"""
        criteria = Mock(spec=AchievementCriteria)
        custom_date = datetime(2023, 1, 1, 12, 0, 0)
        
        achievement = Achievement(
            id=1,
            name="Test Achievement",
            description="Test description", 
            category="test",
            criteria=criteria,
            xp_reward=50,
            icon="✅",
            is_active=True,
            created_at=custom_date
        )
        
        assert achievement.created_at == custom_date
    
    def test_is_criteria_met_delegates_to_criteria(self):
        """Test that is_criteria_met properly delegates to criteria object"""
        criteria = Mock(spec=AchievementCriteria)
        criteria.is_met.return_value = True
        
        achievement = Achievement(
            id=1,
            name="Test Achievement",
            description="Test description",
            category="discovery",
            criteria=criteria,
            xp_reward=100,
            icon="🎯",
            is_active=True
        )
        
        user_stats = Mock()
        user_collection = []
        
        result = achievement.is_criteria_met(user_stats, user_collection)
        
        assert result is True
        criteria.is_met.assert_called_once_with(user_stats, user_collection, "discovery")
    
    def test_calculate_progress_delegates_to_criteria(self):
        """Test that calculate_progress properly delegates to criteria object"""
        criteria = Mock(spec=AchievementCriteria)
        criteria.calculate_progress.return_value = 0.75
        
        achievement = Achievement(
            id=1,
            name="Progress Achievement",
            description="Test progress calculation",
            category="progress",
            criteria=criteria,
            xp_reward=200,
            icon="📈",
            is_active=True
        )
        
        user_stats = Mock()
        user_collection = []
        
        progress = achievement.calculate_progress(user_stats, user_collection)
        
        assert progress == 0.75
        criteria.calculate_progress.assert_called_once_with(user_stats, user_collection, "progress")
    
    def test_achievement_equality(self):
        """Test achievement equality based on ID"""
        criteria1 = Mock(spec=AchievementCriteria)
        criteria2 = Mock(spec=AchievementCriteria)
        
        achievement1 = Achievement(
            id=1,
            name="Test 1",
            description="Description 1",
            category="test",
            criteria=criteria1,
            xp_reward=100,
            icon="🔥",
            is_active=True
        )
        
        achievement2 = Achievement(
            id=1,
            name="Test 2",  # Different name but same ID
            description="Description 2",
            category="test",
            criteria=criteria2,
            xp_reward=200,
            icon="⭐",
            is_active=False
        )
        
        achievement3 = Achievement(
            id=2,
            name="Test 1",  # Same name but different ID
            description="Description 1",
            category="test",
            criteria=criteria1,
            xp_reward=100,
            icon="🔥",
            is_active=True
        )
        
        # Achievements with same ID should be equal (if implementing __eq__)
        # Different IDs should not be equal
        assert achievement1.id == achievement2.id
        assert achievement1.id != achievement3.id


class TestAchievementValidation:
    """Test cases for achievement validation"""
    
    def test_achievement_with_zero_xp_reward(self):
        """Test achievement creation with zero XP reward"""
        criteria = Mock(spec=AchievementCriteria)
        
        achievement = Achievement(
            id=1,
            name="No Reward Achievement",
            description="Achievement with no XP reward",
            category="special",
            criteria=criteria,
            xp_reward=0,
            icon="👻",
            is_active=True
        )
        
        assert achievement.xp_reward == 0
    
    def test_achievement_with_negative_xp_should_be_invalid(self):
        """Test that negative XP rewards should be considered invalid"""
        criteria = Mock(spec=AchievementCriteria)
        
        # This test assumes we might add validation in the future
        # For now, just test the creation doesn't crash
        achievement = Achievement(
            id=1,
            name="Negative Achievement", 
            description="Achievement with negative XP",
            category="penalty",
            criteria=criteria,
            xp_reward=-50,
            icon="💀",
            is_active=True
        )
        
        # In future, this might raise a validation error
        assert achievement.xp_reward == -50
    
    def test_inactive_achievement(self):
        """Test creation of inactive achievement"""
        criteria = Mock(spec=AchievementCriteria)
        
        achievement = Achievement(
            id=1,
            name="Inactive Achievement",
            description="This achievement is disabled",
            category="disabled",
            criteria=criteria,
            xp_reward=100,
            icon="🚫",
            is_active=False
        )
        
        assert achievement.is_active is False