"""Tests for LLM client integration."""

import pytest
from unittest.mock import Mock, patch

from evo.llm import LLMClientIFlow, LLMClientOpenRouter, ModelsIFlow, ModelsOpenRouter
from evo.llm.base import LLMClientBase


class TestLLMClientBase:
    """Test base LLM client functionality."""

    def test_llm_client_base_initialization(self):
        """Test that LLMClientBase can be initialized."""
        client = LLMClientBase(api_key="test-key", base_url="https://test.com/v1")
        assert client is not None
        assert client.client is not None

    @patch('evo.llm.base.llm_client_base.OpenAI')
    def test_llm_client_base_respond(self, mock_openai):
        """Test LLMClientBase respond method."""
        # Mock the OpenAI client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        client = LLMClientBase(api_key="test-key", base_url="https://test.com/v1")
        result = client.respond("test-model", [{"role": "user", "content": "Hello"}])
        
        assert result == "Test response"

    @patch('evo.llm.base.llm_client_base.OpenAI')
    def test_llm_client_base_respond_with_format(self, mock_openai):
        """Test LLMClientBase respond with response format."""
        # Mock the OpenAI client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"key": "value"}'
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        client = LLMClientBase(api_key="test-key", base_url="https://test.com/v1")
        result = client.respond(
            "test-model",
            [{"role": "user", "content": "Hello"}],
            response_format={"type": "json_object"}
        )
        
        assert result == '{"key": "value"}'


class TestLLMClientIFlow:
    """Test iFlow LLM client."""

    def test_iflow_client_initialization(self):
        """Test that LLMClientIFlow can be initialized."""
        client = LLMClientIFlow(api_key="test-key")
        assert client is not None
        assert isinstance(client, LLMClientBase)

    def test_iflow_client_custom_base_url(self):
        """Test LLMClientIFlow with custom base URL."""
        client = LLMClientIFlow(api_key="test-key", base_url="https://custom.com/v1")
        assert client is not None

    def test_models_iflow_enum(self):
        """Test ModelsIFlow enum values."""
        assert ModelsIFlow.IFLOW_ROME == 'iflow-rome-30ba3b'
        assert ModelsIFlow.DEEPSEEK_V3 == 'deepseek-v3'
        assert ModelsIFlow.QWEN3_MAX == 'qwen3-max'
        assert ModelsIFlow.KIMI_K2 == 'kimi-k2'


class TestLLMClientOpenRouter:
    """Test OpenRouter LLM client."""

    def test_openrouter_client_initialization(self):
        """Test that LLMClientOpenRouter can be initialized."""
        client = LLMClientOpenRouter(api_key="test-key")
        assert client is not None
        assert isinstance(client, LLMClientBase)

    def test_openrouter_client_custom_base_url(self):
        """Test LLMClientOpenRouter with custom base URL."""
        client = LLMClientOpenRouter(api_key="test-key", base_url="https://custom.com/v1")
        assert client is not None

    def test_models_openrouter_enum(self):
        """Test ModelsOpenRouter enum values."""
        assert ModelsOpenRouter.DEEPSEEK_R1_0528 == 'deepseek/deepseek-r1-0528:free'
        assert ModelsOpenRouter.QWEN3_CODER == 'qwen/qwen3-coder:free'
        assert ModelsOpenRouter.PONY_ALPHA == 'openrouter/pony-alpha'


class TestActionLayerLLMIntegration:
    """Test ActionLayer integration with LLM clients."""

    @patch('evo.action.LLMClientIFlow')
    def test_action_layer_with_iflow_provider(self, mock_iflow_client):
        """Test ActionLayer with iFlow provider."""
        from evo.action import ActionLayer
        from evo.config import Config
        
        # Mock the LLM client
        mock_llm_instance = Mock()
        mock_llm_instance.respond.return_value = '{"steps": [{"tool": "test", "action": "execute"}]}'
        mock_iflow_client.return_value = mock_llm_instance
        
        # Set environment for iFlow provider
        import os
        os.environ['LLM_PROVIDER'] = 'iflow'
        os.environ['LLM_API_KEY'] = 'test-key'
        
        action = ActionLayer(api_key='test-key', llm_provider='iflow')
        
        # Verify client was created with correct parameters
        mock_iflow_client.assert_called_once()
        call_args = mock_iflow_client.call_args
        assert call_args[1]['api_key'] == 'test-key'
        
        # Clean up
        del os.environ['LLM_PROVIDER']
        del os.environ['LLM_API_KEY']

    @patch('evo.action.LLMClientOpenRouter')
    def test_action_layer_with_openrouter_provider(self, mock_openrouter_client):
        """Test ActionLayer with OpenRouter provider."""
        from evo.action import ActionLayer
        
        # Mock the LLM client
        mock_llm_instance = Mock()
        mock_llm_instance.respond.return_value = '{"steps": [{"tool": "test", "action": "execute"}]}'
        mock_openrouter_client.return_value = mock_llm_instance
        
        action = ActionLayer(api_key='test-key', llm_provider='openrouter')
        
        # Verify client was created with correct parameters
        mock_openrouter_client.assert_called_once()
        call_args = mock_openrouter_client.call_args
        assert call_args[1]['api_key'] == 'test-key'

    def test_action_plan_action_with_llm_client(self):
        """Test plan_action uses LLM client when available."""
        from evo.action import ActionLayer
        
        with patch('evo.action.LLMClientIFlow') as mock_client:
            mock_llm_instance = Mock()
            mock_llm_instance.respond.return_value = '{"steps": [{"tool": "test_tool", "action": "execute"}]}'
            mock_client.return_value = mock_llm_instance
            
            action = ActionLayer(api_key='test-key', llm_provider='iflow')
            action.register_tool('test_tool', lambda: 'result', 'A test tool')
            
            result = action.plan_action({'goal': 'test goal'})
            
            assert 'steps' in result
            assert len(result['steps']) > 0
            mock_llm_instance.respond.assert_called_once()

    def test_action_plan_action_fallback_without_api_key(self):
        """Test plan_action falls back to simple planning without API key."""
        from evo.action import ActionLayer
        
        action = ActionLayer(api_key=None)
        
        result = action.plan_action({'goal': 'test goal'})
        
        assert 'steps' in result
        assert result.get('goal') == 'test goal' or 'goal' in result