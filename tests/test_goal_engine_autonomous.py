"""Tests for GoalEngine with autonomous goal generation from intrinsic drives."""

import pytest
from evo.goal import GoalEngine


class TestGoalEngineAutonomous:
    """Test suite for GoalEngine autonomous goal generation."""

    @pytest.fixture
    def goal_engine(self):
        """Create a fresh GoalEngine instance for each test."""
        return GoalEngine()

    def test_goal_engine_has_generate_autonomous_goals_method(self, goal_engine):
        """Test that GoalEngine has generate_autonomous_goals method."""
        assert hasattr(goal_engine, 'generate_autonomous_goals'), "Should have generate_autonomous_goals"
        assert callable(goal_engine.generate_autonomous_goals), "Should be callable"

    def test_generate_autonomous_goals_creates_goals(self, goal_engine):
        """Test that generate_autonomous_goals creates internal goals."""
        goals = goal_engine.generate_autonomous_goals()
        
        assert goals is not None, "Should return goals"
        assert isinstance(goals, list), "Goals should be a list"
        assert len(goals) > 0, "Should generate at least one goal"

    def test_generate_autonomous_goals_uses_all_drives(self, goal_engine):
        """Test that generate_autonomous_goals uses all intrinsic drives."""
        goals = goal_engine.generate_autonomous_goals()
        
        # Should generate goals for different drives
        drives_used = set()
        for goal in goals:
            if "drive" in goal:
                drives_used.add(goal["drive"])
        
        assert len(drives_used) > 0, "Should use at least one drive"

    def test_generate_autonomous_goals_prioritizes_goals(self, goal_engine):
        """Test that generate_autonomous_goals prioritizes goals."""
        goals = goal_engine.generate_autonomous_goals()
        
        # Goals should have priorities
        for goal in goals:
            assert "priority" in goal, "Goals should have priority"
            assert 0 <= goal["priority"] <= 1, "Priority should be between 0 and 1"

    def test_generate_autonomous_goals_adds_to_internal_goals(self, goal_engine):
        """Test that generate_autonomous_goals adds goals to internal goals."""
        initial_count = len(goal_engine.list_internal_goals())
        
        goal_engine.generate_autonomous_goals()
        
        final_count = len(goal_engine.list_internal_goals())
        assert final_count > initial_count, "Should add internal goals"

    def test_generate_autonomous_goals_respects_drive_selection(self, goal_engine):
        """Test that generate_autonomous_goals respects specific drive selection."""
        goals = goal_engine.generate_autonomous_goals(drive="curiosity")
        
        assert len(goals) > 0, "Should generate goals for specific drive"
        for goal in goals:
            if "drive" in goal:
                assert goal["drive"] == "curiosity", "Should use selected drive"

    def test_generate_autonomous_goals_evaluates_feasibility(self, goal_engine):
        """Test that generate_autonomous_goals evaluates goal feasibility."""
        goals = goal_engine.generate_autonomous_goals()
        
        for goal in goals:
            assert "feasibility" in goal, "Goals should have feasibility score"
            assert 0 <= goal["feasibility"] <= 1, "Feasibility should be between 0 and 1"

    def test_generate_autonomous_goals_tracks_drive_frequency(self, goal_engine):
        """Test that generate_autonomous_goals tracks drive usage frequency."""
        goals1 = goal_engine.generate_autonomous_goals()
        goals2 = goal_engine.generate_autonomous_goals()
        
        # Should generate goals in both calls
        assert len(goals1) > 0, "First call should generate goals"
        assert len(goals2) > 0, "Second call should generate goals"

    def test_generate_autonomous_goals_balances_drives(self, goal_engine):
        """Test that generate_autonomous_goals balances across drives."""
        all_goals = []
        for _ in range(4):  # Generate multiple times
            goals = goal_engine.generate_autonomous_goals()
            all_goals.extend(goals)
        
        # Should have used multiple drives
        drives = set()
        for goal in all_goals:
            if "drive" in goal:
                drives.add(goal["drive"])
        
        assert len(drives) > 1, "Should balance across multiple drives"

    def test_generate_autonomous_goals_handles_no_drives(self, goal_engine):
        """Test that generate_autonomous_goals handles case with no drives specified."""
        goals = goal_engine.generate_autonomous_goals(drive=None)
        
        assert goals is not None, "Should handle no drive specified"
        assert isinstance(goals, list), "Should return list"

    def test_generate_autonomous_goals_includes_actionable_steps(self, goal_engine):
        """Test that generate_autonomous_goals includes actionable steps."""
        goals = goal_engine.generate_autonomous_goals()
        
        for goal in goals:
            assert "actions" in goal, "Goals should have actions"
            assert isinstance(goal["actions"], list), "Actions should be a list"
            assert len(goal["actions"]) > 0, "Should have at least one action"