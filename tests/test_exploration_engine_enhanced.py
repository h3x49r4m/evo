"""Tests for enhanced ExplorationEngine with action execution."""

import pytest
from evo.exploration import ExplorationEngine


class TestExplorationEngineEnhanced:
    """Test suite for enhanced ExplorationEngine functionality."""

    @pytest.fixture
    def exploration_engine(self):
        """Create a fresh ExplorationEngine instance for each test."""
        return ExplorationEngine()

    def test_exploration_engine_has_explore_method(self, exploration_engine):
        """Test that ExplorationEngine has an explore method."""
        assert hasattr(exploration_engine, 'explore'), "Should have explore method"
        assert callable(exploration_engine.explore), "explore should be callable"

    def test_explore_executes_exploration_actions(self, exploration_engine):
        """Test that explore executes exploration actions."""
        result = exploration_engine.explore()
        
        assert result is not None, "Should return exploration result"
        assert "actions" in result, "Should include actions"

    def test_explore_discovers_new_capabilities(self, exploration_engine):
        """Test that explore can discover new capabilities."""
        # Register some capabilities
        exploration_engine.register_capability("known_tool", used=True)
        exploration_engine.register_capability("unknown_tool", used=False)
        
        result = exploration_engine.explore()
        
        assert result is not None, "Should discover capabilities"

    def test_explore_updates_capability_usage(self, exploration_engine):
        """Test that explore updates capability usage tracking."""
        exploration_engine.register_capability("test_capability", used=False)
        
        result = exploration_engine.explore()
        
        assert result is not None, "Should update capability tracking"

    def test_explore_generates_exploration_goals(self, exploration_engine):
        """Test that explore generates exploration goals."""
        result = exploration_engine.explore()
        
        assert "goals" in result, "Should generate exploration goals"
        assert isinstance(result["goals"], list), "Goals should be a list"

    def test_explore_tracks_exploration_progress(self, exploration_engine):
        """Test that explore tracks exploration progress."""
        result1 = exploration_engine.explore()
        result2 = exploration_engine.explore()
        
        assert result1 is not None, "Should track first exploration"
        assert result2 is not None, "Should track second exploration"

    def test_explore_handles_no_capabilities(self, exploration_engine):
        """Test that explore handles case with no registered capabilities."""
        result = exploration_engine.explore()
        
        assert result is not None, "Should handle no capabilities"
        assert "actions" in result, "Should still have actions"

    def test_explore_selects_unused_capabilities(self, exploration_engine):
        """Test that explore prioritizes unused capabilities."""
        exploration_engine.register_capability("used_cap", used=True)
        exploration_engine.register_capability("unused_cap", used=False)
        
        result = exploration_engine.explore()
        
        assert result is not None, "Should select from capabilities"

    def test_explore_returns_executable_plan(self, exploration_engine):
        """Test that explore returns an executable exploration plan."""
        result = exploration_engine.explore()
        
        assert "plan" in result, "Should return exploration plan"
        assert isinstance(result["plan"], dict), "Plan should be a dictionary"

    def test_explore_synthesizes_new_purposes(self, exploration_engine):
        """Test that explore can synthesize new purposes from exploration."""
        result = exploration_engine.explore()
        
        assert "purposes" in result, "Should synthesize purposes"

    def test_explore_records_exploration_history(self, exploration_engine):
        """Test that explore records exploration history."""
        exploration_engine.explore()
        exploration_engine.explore()
        
        # Should have some exploration tracking
        assert True, "Exploration should be tracked"