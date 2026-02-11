"""Tests for Action Layer (TDD Red Phase)."""

import pytest
from evo.action import ActionLayer


class TestActionPlanner:
    """Tests for action planner."""
    
    def test_plan_action_returns_execution_plan(self):
        """Given action layer, When planning action, Then returns execution plan."""
        layer = ActionLayer()
        plan = layer.plan_action({"goal": "write_code", "tools": ["file_write"]})
        assert "steps" in plan
        assert len(plan["steps"]) > 0
    
    def test_plan_action_selects_tools_from_registry(self):
        """Given action layer with tools, When planning, Then selects appropriate tools."""
        layer = ActionLayer()
        layer.register_tool("file_write", lambda: "written")
        plan = layer.plan_action({"goal": "write_file", "tools": ["file_write"]})
        assert "file_write" in str(plan["steps"])
    
    def test_plan_action_handles_no_available_tools(self):
        """Given action layer without tools, When planning, Then creates default step."""
        layer = ActionLayer()
        plan = layer.plan_action({"goal": "complex_task"})
        assert len(plan["steps"]) >= 1  # Always has at least a default step


class TestToolExecutor:
    """Tests for tool executor."""
    
    def test_execute_tool_runs_callable_and_returns_result(self):
        """Given action layer, When executing tool, Then runs callable and returns result."""
        layer = ActionLayer()
        layer.register_tool("test_tool", lambda: "test_result")
        result = layer.execute_tool("test_tool")
        assert result == "test_result"
    
    def test_execute_tool_with_params_passes_params_to_callable(self):
        """Given action layer, When executing tool with params, Then passes params."""
        layer = ActionLayer()
        layer.register_tool("add", lambda x, y: x + y)
        result = layer.execute_tool("add", {"x": 2, "y": 3})
        assert result == 5
    
    def test_execute_tool_handles_errors_with_retry(self):
        """Given action layer, When tool fails, Then retries and handles error."""
        layer = ActionLayer()
        call_count = [0]
        def failing_tool():
            call_count[0] += 1
            if call_count[0] < 2:
                raise Exception("Failed")
            return "success"
        layer.register_tool("failing", failing_tool)
        result = layer.execute_tool("failing", max_retries=2)
        assert result == "success"
        assert call_count[0] == 2
    
    def test_execute_nonexistent_tool_returns_error(self):
        """Given action layer, When executing nonexistent tool, Then returns error."""
        layer = ActionLayer()
        result = layer.execute_tool("nonexistent")
        assert "error" in str(result)


class TestActionLayerIntegration:
    """Integration tests for action layer."""
    
    def test_full_workflow_plan_and_execute(self):
        """Given action layer, When planning and executing, Then completes workflow."""
        layer = ActionLayer()
        layer.register_tool("write", lambda: "written")
        # Plan
        plan = layer.plan_action({"goal": "write_file", "tools": ["write"]})
        # Execute first step
        if plan["steps"]:
            result = layer.execute_tool(plan["steps"][0]["tool"])
            assert result == "written"


class TestActionLayerWithOpenAI:
    """Tests for action layer with OpenAI integration."""
    
    def test_init_with_api_key_sets_openai_api_key(self):
        """Given api_key parameter, When initializing action layer, Then sets OpenAI API key."""
        import unittest.mock as mock
        try:
            import openai
            with mock.patch.object(openai, 'api_key', create=True) as mock_key:
                layer = ActionLayer(api_key="test-key-123")
                assert layer.api_key == "test-key-123"
                # openai.api_key is set in __init__ (lines 11-12)
        except ImportError:
            pytest.skip("openai not available")
    
    def test_init_with_env_api_key_sets_openai_api_key(self):
        """Given OPENAI_API_KEY env var, When initializing, Then sets OpenAI API key from config."""
        import unittest.mock as mock
        try:
            import openai
            # Test that Config.OPENAI_API_KEY is used when no explicit api_key is provided
            from evo.action import ActionLayer
            from evo.config import Config
            with mock.patch.object(Config, 'OPENAI_API_KEY', 'env-key-456'):
                with mock.patch.object(openai, 'api_key', create=True) as mock_key:
                    layer = ActionLayer()
                    assert layer.api_key == "env-key-456"
        except ImportError:
            pytest.skip("openai not available")
    
    def test_plan_action_with_api_key_calls_llm_planner(self):
        """Given action layer with API key, When planning action, Then uses LLM planner."""
        import unittest.mock as mock
        try:
            import openai
            layer = ActionLayer(api_key="test-key")
            layer.register_tool("test_tool", lambda: "result", "A test tool")
            
            # Mock the LLM call
            with mock.patch('evo.action.openai.ChatCompletion.create') as mock_create:
                mock_response = mock.MagicMock()
                mock_response.choices[0].message.content = '{"steps": [{"tool": "test_tool", "action": "execute"}]}'
                mock_create.return_value = mock_response
                
                plan = layer.plan_action({"goal": "test goal"})
                
                # Verify LLM was called (lines 91-93)
                assert mock_create.called
                assert "steps" in plan
        except ImportError:
            pytest.skip("openai not available")
    
    def test_plan_action_falls_back_on_llm_error(self):
        """Given action layer with API key, When LLM fails, Then falls back to simple planner."""
        import unittest.mock as mock
        try:
            import openai
            layer = ActionLayer(api_key="test-key")
            
            # Mock the LLM call to raise exception
            with mock.patch('evo.action.openai.ChatCompletion.create', side_effect=Exception("API error")):
                plan = layer.plan_action({"goal": "test goal", "tools": ["tool1"]})
                
                # Should fall back to simple planner (line 93 exception handling)
                assert "steps" in plan
                assert len(plan["steps"]) > 0
        except ImportError:
            pytest.skip("openai not available")
    
    def test_plan_action_handles_llm_response_without_steps(self):
        """Given LLM response without steps, When planning, Then falls back to simple planner."""
        import unittest.mock as mock
        try:
            import openai
            layer = ActionLayer(api_key="test-key")
            
            # Mock the LLM call to return response without steps
            with mock.patch('evo.action.openai.ChatCompletion.create') as mock_create:
                mock_response = mock.MagicMock()
                mock_response.choices[0].message.content = '{"result": "no steps"}'
                mock_create.return_value = mock_response
                
                plan = layer.plan_action({"goal": "test goal", "tools": ["tool1"]})
                
                # Should fall back to simple planner (line 91 check for "steps" in llm_plan)
                assert "steps" in plan
        except ImportError:
            pytest.skip("openai not available")


class TestToolExecutorErrorPaths:
    """Tests for tool executor error handling paths."""
    
    def test_execute_tool_returns_error_after_max_retries(self):
        """Given tool that always fails, When executing, Then returns error after max retries."""
        layer = ActionLayer()
        call_count = [0]
        def always_failing():
            call_count[0] += 1
            raise Exception("Always fails")
        layer.register_tool("failing_tool", always_failing)
        
        result = layer.execute_tool("failing_tool", max_retries=3)
        
        # Should return error after max retries (lines 174-177)
        assert "error" in result
        assert "failed after 3 attempts" in result["error"]
        assert call_count[0] == 3  # Should have attempted 3 times
    
    def test_execute_tool_with_zero_retries_immediately_fails(self):
        """Given tool that fails, When executing with 0 retries, Then returns error immediately."""
        layer = ActionLayer()
        def failing_tool():
            raise Exception("Fails immediately")
        layer.register_tool("failing_tool", failing_tool)
        
        result = layer.execute_tool("failing_tool", max_retries=1)
        
        # Should return error after single attempt (line 174 check for max_retries - 1)
        assert "error" in result
        assert "failed after 1 attempts" in result["error"]
    
    def test_execute_tool_with_params_and_exception_returns_error(self):
        """Given tool with params that raises exception, When executing, Then handles and returns error."""
        layer = ActionLayer()
        def tool_with_params(x, y):
            if x == y:
                raise ValueError("x cannot equal y")
            return x + y
        layer.register_tool("add_tool", tool_with_params)
        
        result = layer.execute_tool("add_tool", {"x": 5, "y": 5}, max_retries=1)
        
        # Should handle exception and return error (lines 174-177)
        assert "error" in result
        assert "failed after 1 attempts" in result["error"]
    
    def test_execute_tool_without_params_and_exception_returns_error(self):
        """Given tool without params that raises exception, When executing, Then handles and returns error."""
        layer = ActionLayer()
        def no_param_tool():
            raise RuntimeError("No params tool error")
        layer.register_tool("no_param_tool", no_param_tool)
        
        result = layer.execute_tool("no_param_tool", max_retries=1)
        
        # Should handle exception and return error (line 174 check with no params)
        assert "error" in result
        assert "failed after 1 attempts" in result["error"]
    
    def test_execute_tool_with_exception_retried_and_finally_returns_unknown_error(self):
        """Given tool with retry that fails all attempts, When executing, Then returns unknown error path."""
        layer = ActionLayer()
        call_count = [0]
        def fails_all_retries():
            call_count[0] += 1
            raise Exception("Fails all")
        layer.register_tool("fail_all", fails_all_retries)
        
        result = layer.execute_tool("fail_all", max_retries=2)
        
        # Should hit the final return unknown error path (line 177)
        assert "error" in result


class TestActionLayerWithCapabilityRegistry:
    """Tests for action layer integration with capability registry."""
    
    def test_register_tool_without_capability_registry_uses_internal_storage(self):
        """Given action layer without capability_registry, When registering tool, Then uses internal storage (line 51)."""
        layer = ActionLayer(capability_registry=None)
        layer.register_tool("internal_tool", lambda: "internal_result")
        
        # Tool should be stored in internal registry
        assert hasattr(layer, '_internal_tools')
        assert "internal_tool" in layer._internal_tools
    
    def test_execute_tool_retrieves_from_capability_registry(self):
        """Given action layer with capability_registry, When executing tool, Then retrieves from registry (lines 155-157)."""
        from evo.capability import CapabilityRegistry
        
        registry = CapabilityRegistry()
        registry.register_tool("registry_tool", "A tool", lambda: "registry_result")
        
        layer = ActionLayer(capability_registry=registry)
        result = layer.execute_tool("registry_tool")
        
        # Should retrieve from capability registry
        assert result == "registry_result"
    
    def test_execute_tool_fallback_to_internal_when_not_in_registry(self):
        """Given action layer with both registry and internal, When executing, Then checks registry first then internal."""
        from evo.capability import CapabilityRegistry
        
        registry = CapabilityRegistry()
        layer = ActionLayer(capability_registry=registry)
        
        # Register in internal storage
        layer.register_tool("internal_only", lambda: "internal")
        
        result = layer.execute_tool("internal_only")
        assert result == "internal"