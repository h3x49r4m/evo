"""Tests for enhanced SelfHandler with intrinsic drive integration."""

import pytest
from unittest.mock import Mock, patch
from evo.handler import SelfHandler


class TestSelfHandlerEnhanced:
    """Test suite for enhanced SelfHandler functionality."""

    @pytest.fixture
    def handler(self):
        """Create a fresh SelfHandler instance for each test."""
        return SelfHandler()

    def test_self_handler_has_execute_method(self, handler):
        """Test that SelfHandler has an execute method."""
        assert hasattr(handler, 'execute'), "SelfHandler should have an execute method"
        assert callable(handler.execute), "execute should be a callable method"

    def test_execute_generates_goals_from_curiosity_drive(self, handler):
        """Test that execute generates goals from curiosity drive."""
        goals = handler.execute(drive="curiosity")
        assert goals is not None, "execute should return goals"
        assert "drive" in goals, "goals should contain drive information"
        assert goals["drive"] == "curiosity", "drive should be curiosity"

    def test_execute_generates_goals_from_competence_drive(self, handler):
        """Test that execute generates goals from competence drive."""
        goals = handler.execute(drive="competence")
        assert goals is not None, "execute should return goals"
        assert goals["drive"] == "competence", "drive should be competence"

    def test_execute_generates_goals_from_autonomy_drive(self, handler):
        """Test that execute generates goals from autonomy drive."""
        goals = handler.execute(drive="autonomy")
        assert goals is not None, "execute should return goals"
        assert goals["drive"] == "autonomy", "drive should be autonomy"

    def test_execute_generates_goals_from_meaning_drive(self, handler):
        """Test that execute generates goals from meaning drive."""
        goals = handler.execute(drive="meaning")
        assert goals is not None, "execute should return goals"
        assert goals["drive"] == "meaning", "drive should be meaning"

    def test_execute_cycles_through_all_drives(self, handler):
        """Test that execute cycles through all intrinsic drives."""
        drives = ["curiosity", "competence", "autonomy", "meaning"]
        executed_drives = []
        
        for _ in range(4):
            goals = handler.execute()
            if "drive" in goals:
                executed_drives.append(goals["drive"])
        
        # Should have executed all drives
        assert len(executed_drives) == 4, f"Expected 4 drives, got {len(executed_drives)}"
        for drive in drives:
            assert drive in executed_drives, f"Drive {drive} should have been executed"

    def test_execute_returns_actionable_goals(self, handler):
        """Test that execute returns actionable goals."""
        goals = handler.execute(drive="curiosity")
        assert "actions" in goals, "goals should contain actions"
        assert isinstance(goals["actions"], list), "actions should be a list"
        assert len(goals["actions"]) > 0, "should have at least one action"

    def test_execute_tracks_drive_priority(self, handler):
        """Test that execute tracks drive priority for goal selection."""
        # Execute multiple times and track priorities
        priority_history = []
        
        for _ in range(10):
            goals = handler.execute()
            if "priority" in goals:
                priority_history.append(goals["priority"])
        
        # Should have priority information
        assert len(priority_history) > 0, "Should have tracked priorities"

    def test_execute_updates_self_context(self, handler):
        """Test that execute updates self context with executed goals."""
        initial_context = {"last_goal": None}
        
        goals = handler.execute(drive="curiosity")
        
        # Should return goals that can be used to update context
        assert "goal_description" in goals, "goals should have description"
        assert goals["goal_description"] is not None, "description should not be None"

    def test_execute_handles_no_drive_specified(self, handler):
        """Test that execute handles cases where no drive is specified."""
        goals = handler.execute()
        assert goals is not None, "execute should handle no drive specified"
        assert "drive" in goals, "should select a default drive"

    def test_execute_handles_invalid_drive(self, handler):
        """Test that execute handles invalid drive names gracefully."""
        goals = handler.execute(drive="invalid_drive")
        # Should not crash, should return valid goals with a default drive
        assert goals is not None, "execute should handle invalid drive"
        assert "drive" in goals, "should have drive information"

    def test_execute_returns_goal_metadata(self, handler):
        """Test that execute returns metadata about generated goals."""
        goals = handler.execute(drive="curiosity")
        assert "timestamp" in goals, "goals should have timestamp"
        assert "drive" in goals, "goals should have drive"
        assert "actions" in goals, "goals should have actions"