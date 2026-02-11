"""Tests for IntegrativeCore component."""

import pytest
from evo.integrative_core import IntegrativeCore


class TestIntegrativeCore:
    """Test suite for IntegrativeCore that combines user input and self state."""

    def test_integrative_core_init_creates_empty_contexts(self):
        """Test that IntegrativeCore initializes with empty user and self contexts."""
        core = IntegrativeCore()
        assert core.user_context is not None
        assert core.self_context is not None
        assert isinstance(core.user_context, dict)
        assert isinstance(core.self_context, dict)

    def test_integrative_core_combine_user_input_only(self):
        """Test combining only user input without self state."""
        core = IntegrativeCore()
        user_input = {"type": "user", "message": "Hello"}
        result = core.combine(user_input, None)
        assert result["source"] == "user"
        assert result["data"] == user_input

    def test_integrative_core_combine_self_state_only(self):
        """Test combining only self state without user input."""
        core = IntegrativeCore()
        self_state = {"type": "self", "goal": "explore"}
        result = core.combine(None, self_state)
        assert result["source"] == "self"
        assert result["data"] == self_state

    def test_integrative_core_combine_both_user_and_self(self):
        """Test combining both user input and self state (hybrid mode)."""
        core = IntegrativeCore()
        user_input = {"type": "user", "message": "Help me"}
        self_state = {"type": "self", "goal": "assist"}
        result = core.combine(user_input, self_state)
        assert result["source"] == "hybrid"
        assert "user" in result["data"]
        assert "self" in result["data"]

    def test_integrative_core_combine_with_empty_inputs(self):
        """Test combining empty inputs returns empty context."""
        core = IntegrativeCore()
        result = core.combine(None, None)
        assert result["source"] == "empty"
        assert result["data"] == {}

    def test_integrative_core_update_user_context(self):
        """Test updating user context."""
        core = IntegrativeCore()
        core.update_user_context("conversation", ["Hello", "Hi"])
        assert core.user_context["conversation"] == ["Hello", "Hi"]

    def test_integrative_core_update_self_context(self):
        """Test updating self context."""
        core = IntegrativeCore()
        core.update_self_context("active_goals", ["explore", "learn"])
        assert core.self_context["active_goals"] == ["explore", "learn"]

    def test_integrative_core_get_integrated_context(self):
        """Test getting the integrated context."""
        core = IntegrativeCore()
        core.update_user_context("message", "Hello")
        core.update_self_context("goal", "assist")
        result = core.get_integrated_context()
        assert "user" in result
        assert "self" in result
        assert result["user"]["message"] == "Hello"
        assert result["self"]["goal"] == "assist"


class TestIntegrativeCoreIntegration:
    """Integration tests for IntegrativeCore with other components."""

    def test_integrative_core_with_perception_gateway(self):
        """Test IntegrativeCore working with PerceptionGateway."""
        from evo.perception import PerceptionGateway

        core = IntegrativeCore()
        gateway = PerceptionGateway()
        
        user_input = {"source": "user", "data": "Hello"}
        routed = gateway.filter_and_route(user_input)
        
        result = core.combine(routed, None)
        assert result["source"] in ["user", "empty"]

    def test_integrative_core_with_goal_engine(self):
        """Test IntegrativeCore working with GoalEngine."""
        from evo.goal import GoalEngine

        core = IntegrativeCore()
        goal_engine = GoalEngine()
        
        goal_engine.add_internal_goal("explore", "Learn new things")
        core.update_self_context("goals", goal_engine.list_internal_goals())
        
        result = core.get_integrated_context()
        assert "explore" in result["self"]["goals"]