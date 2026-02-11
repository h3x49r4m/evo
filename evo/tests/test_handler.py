"""Tests for User Handler & Self Handler (TDD Red Phase)."""

import pytest
from evo.handler import UserHandler, SelfHandler


class TestUserHandler:
    """Tests for user handler."""
    
    def test_parse_intent_returns_action(self):
        """Given user handler, When parsing intent, Then returns action."""
        handler = UserHandler()
        intent = handler.parse_intent("Write Python code")
        assert "action" in intent
    
    def test_execute_request_returns_response(self):
        """Given user handler, When executing request, Then returns response."""
        handler = UserHandler()
        response = handler.execute_request({"action": "test"})
        assert "response" in response


class TestSelfHandler:
    """Tests for self handler."""
    
    def test_generate_internal_goal_returns_goal(self):
        """Given self handler, When generating goal, Then returns goal."""
        handler = SelfHandler()
        goal = handler.generate_internal_goal()
        assert "goal" in goal
    
    def test_explore_purposes_returns_purposes(self):
        """Given self handler, When exploring purposes, Then returns purposes."""
        handler = SelfHandler()
        purposes = handler.explore_purposes()
        assert len(purposes) >= 1