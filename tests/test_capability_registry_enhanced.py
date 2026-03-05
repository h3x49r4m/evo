"""Tests for enhanced CapabilityRegistry with skill level tracking."""

import pytest
from evo.capability import CapabilityRegistry


class TestCapabilityRegistryEnhanced:
    """Test suite for enhanced CapabilityRegistry functionality."""

    @pytest.fixture
    def registry(self):
        """Create a fresh CapabilityRegistry instance for each test."""
        return CapabilityRegistry()

    def test_registry_has_skill_level_tracking(self, registry):
        """Test that registry tracks skill levels."""
        assert hasattr(registry, 'update_skill_level'), "Should have update_skill_level method"
        assert callable(registry.update_skill_level), "Should be callable"

    def test_update_skill_level_updates_capability(self, registry):
        """Test that update_skill_level updates capability skill level."""
        # Register a capability
        registry.register_tool("test_tool", "A test tool", lambda: "result")
        
        # Update skill level
        registry.update_skill_level("test_tool", 0.8)
        
        # Verify skill level was updated
        tool = registry.get_tool("test_tool")
        assert tool is not None, "Should retrieve tool"
        # Tool should have skill level information

    def test_get_skill_level_returns_level(self, registry):
        """Test that get_skill_level returns current skill level."""
        # Register and update skill level
        registry.register_tool("python", "Python programming", lambda: "code")
        registry.update_skill_level("python", 0.9)
        
        # Get skill level
        level = registry.get_skill_level("python")
        
        assert level is not None, "Should return skill level"
        assert level == 0.9, "Should return correct skill level"

    def test_get_skill_level_handles_unknown_capability(self, registry):
        """Test that get_skill_level handles unknown capabilities."""
        level = registry.get_skill_level("unknown_capability")
        
        assert level is not None, "Should handle unknown capability"
        # Should return default level

    def test_get_top_skills_returns_ranked_list(self, registry):
        """Test that get_top_skills returns skills ranked by level."""
        # Register multiple skills
        registry.register_tool("skill1", "Skill 1", lambda: "1")
        registry.register_tool("skill2", "Skill 2", lambda: "2")
        registry.register_tool("skill3", "Skill 3", lambda: "3")
        
        # Set different skill levels
        registry.update_skill_level("skill1", 0.5)
        registry.update_skill_level("skill2", 0.9)
        registry.update_skill_level("skill3", 0.7)
        
        # Get top skills
        top_skills = registry.get_top_skills(limit=2)
        
        assert len(top_skills) == 2, "Should return top 2 skills"
        # Top skill should be skill2 with 0.9
        assert top_skills[0]["name"] == "skill2", "Should rank highest skill first"

    def test_update_skill_level_increments_on_success(self, registry):
        """Test that skill level increments on success."""
        registry.register_tool("test", "Test", lambda: "result")
        registry.update_skill_level("test", 0.5)
        
        # Update with success
        registry.update_skill_level("test", 0.5, success=True)
        
        # Level should have increased
        new_level = registry.get_skill_level("test")
        assert new_level > 0.5, "Skill level should increase on success"

    def test_update_skill_level_decrements_on_failure(self, registry):
        """Test that skill level decrements on failure."""
        registry.register_tool("test", "Test", lambda: "result")
        registry.update_skill_level("test", 0.8)
        
        # Update with failure
        registry.update_skill_level("test", 0.8, success=False)
        
        # Level should have decreased
        new_level = registry.get_skill_level("test")
        assert new_level < 0.8, "Skill level should decrease on failure"

    def test_get_average_skill_level(self, registry):
        """Test that get_average_skill_level returns average of all skills."""
        registry.register_tool("skill1", "Skill 1", lambda: "1")
        registry.register_tool("skill2", "Skill 2", lambda: "2")
        
        registry.update_skill_level("skill1", 0.6)
        registry.update_skill_level("skill2", 0.8)
        
        avg = registry.get_average_skill_level()
        
        assert avg is not None, "Should return average"
        assert avg == 0.7, "Should calculate correct average (0.6 + 0.8) / 2"

    def test_get_learning_progress(self, registry):
        """Test that get_learning_progress tracks skill improvement."""
        registry.register_tool("skill", "Skill", lambda: "result")
        
        # Set initial level
        registry.update_skill_level("skill", 0.5)
        progress1 = registry.get_learning_progress()
        
        # Improve skill
        registry.update_skill_level("skill", 0.7)
        progress2 = registry.get_learning_progress()
        
        # Progress should have increased
        assert progress2 >= progress1, "Learning progress should increase"

    def test_get_capability_mastery(self, registry):
        """Test that get_capability_mastery identifies mastered skills."""
        registry.register_tool("mastered", "Mastered skill", lambda: "result")
        registry.register_tool("learning", "Learning skill", lambda: "result")
        
        registry.update_skill_level("mastered", 0.95)
        registry.update_skill_level("learning", 0.4)
        
        mastery = registry.get_capability_mastery()
        
        assert "mastered" in mastery, "Should identify mastered skill"
        assert "learning" not in mastery, "Should not include learning skill"

    def test_skill_level_clamps_between_0_and_1(self, registry):
        """Test that skill level stays within 0-1 range."""
        registry.register_tool("test", "Test", lambda: "result")
        
        # Try to set above 1
        registry.update_skill_level("test", 1.5)
        level1 = registry.get_skill_level("test")
        assert level1 <= 1.0, "Should clamp to maximum 1.0"
        
        # Try to set below 0
        registry.update_skill_level("test", -0.5)
        level2 = registry.get_skill_level("test")
        assert level2 >= 0.0, "Should clamp to minimum 0.0"