"""Tests for Decision Engine (TDD Red Phase)."""

import pytest
from evo.decision import DecisionEngine


class TestModeSelection:
    """Tests for mode selector (responsive/autonomous/hybrid)."""
    
    def test_select_mode_with_user_input_returns_responsive(self):
        """Given decision engine, When user input present, Then selects responsive mode."""
        engine = DecisionEngine()
        context = {"user_input": "Hello"}
        mode = engine.select_mode(context)
        assert mode == "responsive"
    
    def test_select_mode_without_user_input_returns_autonomous(self):
        """Given decision engine, When no user input, Then selects autonomous mode."""
        engine = DecisionEngine()
        context = {}
        mode = engine.select_mode(context)
        assert mode == "autonomous"
    
    def test_select_mode_with_both_returns_hybrid(self):
        """Given decision engine, When both user and internal input present, Then selects hybrid mode."""
        engine = DecisionEngine()
        context = {"user_input": "Hello", "internal_goals": ["explore"]}
        mode = engine.select_mode(context)
        assert mode == "hybrid"
    
    def test_select_mode_with_safety_alert_returns_safety(self):
        """Given decision engine, When safety alert present, Then prioritizes safety mode."""
        engine = DecisionEngine()
        context = {"safety_alert": True}
        mode = engine.select_mode(context)
        assert mode == "safety"


class TestDecisionRouting:
    """Tests for routing decisions to handlers."""
    
    def test_route_responsive_mode_to_user_handler(self):
        """Given decision engine, When responsive mode selected, Then routes to user handler."""
        engine = DecisionEngine()
        result = engine.route_decision("responsive", {"user_input": "test"})
        assert result["handler"] == "user_handler"
    
    def test_route_autonomous_mode_to_self_handler(self):
        """Given decision engine, When autonomous mode selected, Then routes to self handler."""
        engine = DecisionEngine()
        result = engine.route_decision("autonomous", {"internal_goals": ["explore"]})
        assert result["handler"] == "self_handler"
    
    def test_route_hybrid_mode_to_both_handlers(self):
        """Given decision engine, When hybrid mode selected, Then routes to both handlers."""
        engine = DecisionEngine()
        result = engine.route_decision("hybrid", {"user_input": "test", "internal_goals": ["explore"]})
        assert result["handler"] == "hybrid_handler"
    
    def test_route_safety_mode_to_safety_handler(self):
        """Given decision engine, When safety mode selected, Then routes to safety handler."""
        engine = DecisionEngine()
        result = engine.route_decision("safety", {"safety_alert": True})
        assert result["handler"] == "safety_handler"


class TestDecisionExecution:
    """Tests for executing decisions."""
    
    def test_execute_decision_returns_result(self):
        """Given decision engine, When executing decision, Then returns result."""
        engine = DecisionEngine()
        decision = {"mode": "responsive", "data": {"user_input": "test"}}
        result = engine.execute_decision(decision)
        assert "result" in result
        assert result["mode"] == "responsive"
    
    def test_execute_decision_with_no_data_returns_error(self):
        """Given decision engine, When executing decision with no data, Then returns error."""
        engine = DecisionEngine()
        decision = {"mode": "responsive"}
        result = engine.execute_decision(decision)
        assert "error" in result


class TestDecisionIntegration:
    """Integration tests for decision engine."""
    
    def test_full_workflow_select_route_and_execute(self):
        """Given decision engine, When processing through full workflow, Then correctly processes."""
        engine = DecisionEngine()
        # Select mode
        context = {"user_input": "Help me"}
        mode = engine.select_mode(context)
        # Route decision
        routed = engine.route_decision(mode, context)
        # Execute
        result = engine.execute_decision({"mode": mode, "data": context})
        # Verify
        assert mode == "responsive"
        assert routed["handler"] == "user_handler"
        assert result["mode"] == "responsive"