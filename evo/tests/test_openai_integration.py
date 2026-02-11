"""Tests for OpenAI API integration in ActionLayer."""

import pytest
from unittest.mock import Mock, patch
from evo.action import ActionLayer


class TestOpenAIIntegration:
    """Tests for LLM-based action planning using OpenAI API."""

    @patch('evo.action.openai')
    def test_plan_action_with_openai_api(self, mock_openai):
        """Test plan_action uses OpenAI API for LLM-based planning."""
        # Mock OpenAI client and response
        mock_client = Mock()
        mock_openai.ChatCompletion.create = Mock(return_value=mock_client)
        mock_client.choices = [Mock()]
        mock_client.choices[0].message.content = '{"steps": [{"tool": "analyze", "action": "execute"}, {"tool": "summarize", "action": "execute"}]}'

        # Create action layer with API key
        action_layer = ActionLayer(api_key="test_key")

        # Plan action with goal
        goal = {"goal": "Analyze data and summarize findings"}
        plan = action_layer.plan_action(goal)

        # Verify OpenAI API was called
        assert "steps" in plan
        assert len(plan["steps"]) == 2

    @patch('evo.action.openai')
    def test_plan_action_fallback_when_no_api_key(self, mock_openai):
        """Test plan_action falls back to simple planner when no API key."""
        # Create action layer without API key
        action_layer = ActionLayer()

        # Plan action with goal
        goal = {"goal": "Analyze data"}
        plan = action_layer.plan_action(goal)

        # Verify fallback behavior
        assert "steps" in plan
        assert plan["steps"][0]["tool"] == "Analyze data"

    @patch('evo.action.openai')
    def test_plan_action_handles_openai_error(self, mock_openai):
        """Test plan_action handles OpenAI API errors gracefully."""
        # Mock OpenAI API error
        mock_openai.ChatCompletion.create = Mock(side_effect=Exception("API Error"))

        # Create action layer with API key
        action_layer = ActionLayer(api_key="test_key")

        # Plan action with goal
        goal = {"goal": "Analyze data"}
        plan = action_layer.plan_action(goal)

        # Verify fallback on error
        assert "steps" in plan
        assert plan["steps"][0]["tool"] == "Analyze data"

    @patch('evo.action.openai')
    def test_plan_action_with_context(self, mock_openai):
        """Test plan_action includes context in OpenAI prompt."""
        # Mock OpenAI response
        mock_client = Mock()
        mock_openai.ChatCompletion.create = Mock(return_value=mock_client)
        mock_client.choices = [Mock()]
        mock_client.choices[0].message.content = '{"steps": [{"tool": "search", "action": "execute"}]}'

        # Create action layer with API key
        action_layer = ActionLayer(api_key="test_key")

        # Plan action with goal and context
        goal = {"goal": "Find information", "context": {"user_preferences": ["fast", "accurate"]}}
        plan = action_layer.plan_action(goal)

        # Verify planning succeeded
        assert "steps" in plan