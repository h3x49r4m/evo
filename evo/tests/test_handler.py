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


class TestUserHandlerIntegration:
    """Integration tests for user handler workflow."""
    
    def test_full_user_handler_workflow(self):
        """Given user handler, When processing through full workflow, Then correctly processes user request."""
        handler = UserHandler()
        
        # Step 1: Parse user intent
        user_input = "Write a function to sort an array"
        intent = handler.parse_intent(user_input)
        assert intent["action"] == user_input
        assert intent["intent"] == "user_request"
        
        # Step 2: Execute the parsed request
        response = handler.execute_request(intent)
        assert "response" in response
        assert "Processed:" in response["response"]
        assert user_input in response["response"]
    
    def test_user_handler_handles_empty_input(self):
        """Given user handler, When processing empty input, Then handles gracefully."""
        handler = UserHandler()
        
        intent = handler.parse_intent("")
        assert "action" in intent
        assert intent["action"] == ""
        
        response = handler.execute_request(intent)
        assert "response" in response
    
    def test_user_handler_handles_special_characters(self):
        """Given user handler, When processing special characters, Then preserves them."""
        handler = UserHandler()
        
        special_input = "Test with @#$%^&*()_+-=[]{}|;':\",./<>?"
        intent = handler.parse_intent(special_input)
        assert intent["action"] == special_input
        
        response = handler.execute_request(intent)
        assert special_input in response["response"]


class TestSelfHandlerIntegration:
    """Integration tests for self handler workflow."""
    
    def test_full_self_handler_workflow(self):
        """Given self handler, When processing through full workflow, Then correctly generates and explores."""
        handler = SelfHandler()
        
        # Step 1: Generate internal goal from drives
        goal = handler.generate_internal_goal()
        assert "goal" in goal
        assert "drive" in goal
        
        # Step 2: Explore purposes based on goal
        purposes = handler.explore_purposes()
        assert len(purposes) >= 1
        for purpose in purposes:
            assert "purpose" in purpose
            assert "reason" in purpose
    
    def test_self_handler_purposes_contain_meaningful_content(self):
        """Given self handler, When exploring purposes, Then returns meaningful purposes."""
        handler = SelfHandler()
        
        purposes = handler.explore_purposes()
        assert len(purposes) >= 1
        
        # Verify each purpose has meaningful content
        for purpose in purposes:
            assert len(purpose["purpose"]) > 0
            assert len(purpose["reason"]) > 0
            assert purpose["purpose"] != purpose["reason"]


class TestHandlerIntegration:
    """Integration tests for both handlers working together."""
    
    def test_handlers_have_compatible_interfaces(self):
        """Given both handlers, When comparing interfaces, Then they follow consistent patterns."""
        user_handler = UserHandler()
        self_handler = SelfHandler()
        
        # Both handlers should have __init__ method
        assert hasattr(user_handler, '__init__')
        assert hasattr(self_handler, '__init__')
        
        # Both should have processing methods
        assert hasattr(user_handler, 'parse_intent')
        assert hasattr(user_handler, 'execute_request')
        assert hasattr(self_handler, 'generate_internal_goal')
        assert hasattr(self_handler, 'explore_purposes')
    
    def test_handlers_return_consistent_dict_formats(self):
        """Given both handlers, When returning results, Then use consistent dict formats."""
        user_handler = UserHandler()
        self_handler = SelfHandler()
        
        # User handler returns dict with string keys
        user_result = user_handler.execute_request({"action": "test"})
        assert isinstance(user_result, dict)
        assert all(isinstance(k, str) for k in user_result.keys())
        
        # Self handler returns dict with string keys
        self_goal = self_handler.generate_internal_goal()
        assert isinstance(self_goal, dict)
        assert all(isinstance(k, str) for k in self_goal.keys())
        
        self_purposes = self_handler.explore_purposes()
        assert isinstance(self_purposes, list)
        assert all(isinstance(p, dict) for p in self_purposes)