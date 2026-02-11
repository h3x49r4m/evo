"""Tests for input validation."""

import pytest
from evo.validation import (
    validate_skill_level,
    validate_name,
    validate_tool_name,
    validate_goal_name
)


class TestSkillLevelValidation:
    """Tests for skill level validation."""
    
    def test_valid_skill_levels(self):
        """Test valid skill levels pass validation."""
        assert validate_skill_level(0.0) is True
        assert validate_skill_level(0.5) is True
        assert validate_skill_level(1.0) is True
    
    def test_invalid_skill_levels(self):
        """Test invalid skill levels fail validation."""
        assert validate_skill_level(-0.1) is False
        assert validate_skill_level(1.1) is False
        assert validate_skill_level(2.0) is False
    
    def test_invalid_skill_type(self):
        """Test non-numeric skill levels fail validation."""
        assert validate_skill_level("0.5") is False
        assert validate_skill_level(None) is False


class TestNameValidation:
    """Tests for name validation."""
    
    def test_valid_names(self):
        """Test valid names pass validation."""
        assert validate_name("test", "Entity") is True
        assert validate_name("test_name", "Entity") is True
        assert validate_name("Test123", "Entity") is True
    
    def test_invalid_names(self):
        """Test invalid names fail validation."""
        assert validate_name(None, "Entity") is False
        assert validate_name("", "Entity") is False
        assert validate_name("   ", "Entity") is False
        assert validate_name(123, "Entity") is False


class TestToolNameValidation:
    """Tests for tool name validation."""
    
    def test_valid_tool_names(self):
        """Test valid tool names pass validation."""
        assert validate_tool_name("tool") is True
        assert validate_tool_name("my_tool") is True
        assert validate_tool_name("tool123") is True
    
    def test_invalid_tool_names(self):
        """Test invalid tool names fail validation."""
        assert validate_tool_name("tool-name") is False
        assert validate_tool_name("tool.name") is False
        assert validate_tool_name("tool name") is False


class TestGoalNameValidation:
    """Tests for goal name validation."""
    
    def test_valid_goal_names(self):
        """Test valid goal names pass validation."""
        assert validate_goal_name("goal") is True
        assert validate_goal_name("my_goal") is True
    
    def test_invalid_goal_names(self):
        """Test invalid goal names fail validation."""
        assert validate_goal_name("") is False
        assert validate_goal_name(None) is False
        assert validate_goal_name("   ") is False