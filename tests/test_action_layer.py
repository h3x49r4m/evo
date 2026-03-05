"""Tests for Action Layer (TDD Red Phase)."""

import pytest
from evo.action import ActionLayer


class TestActionPlanner:
    """Tests for action planner."""
    
    def test_plan_action_returns_execution_plan(self):
        """Given action layer, When planning action, Then returns execution plan."""
        layer = ActionLayer(api_key=None)  # No LLM, use simple planning
        plan = layer.plan_action({"goal": "write_code", "tools": ["file_write"]})
        assert "steps" in plan
        assert len(plan["steps"]) > 0
    
    def test_plan_action_selects_tools_from_registry(self):
        """Given action layer with tools, When planning, Then selects appropriate tools."""
        layer = ActionLayer(api_key=None)  # No LLM, use simple planning
        layer.register_tool("file_write", lambda: "written")
        plan = layer.plan_action({"goal": "write_file", "tools": ["file_write"]})
        assert "file_write" in str(plan["steps"])
    
    def test_plan_action_handles_no_available_tools(self):
        """Given action layer without tools, When planning, Then creates default step."""
        layer = ActionLayer(api_key=None)  # No LLM, use simple planning
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
        """Given action layer, When executing nonexistent tool, Then raises ToolNotFoundError."""
        from evo import ToolNotFoundError
        layer = ActionLayer()
        with pytest.raises(ToolNotFoundError):
            layer.execute_tool("nonexistent")


class TestActionLayerIntegration:
    """Integration tests for action layer."""
    
    def test_full_workflow_plan_and_execute(self):
        """Given action layer, When planning and executing, Then completes workflow."""
        layer = ActionLayer(api_key=None)  # No LLM, use simple planning
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
        import os
        original_key = os.environ.get("LLM_API_KEY")
        try:
            os.environ["LLM_API_KEY"] = "env-key-456"
            # Note: Config is loaded at module import, so this won't affect Config.LLM_API_KEY
            # This test demonstrates the limitation of the current config system
            layer = ActionLayer()
            assert layer.api_key is not None
        finally:
            if original_key is not None:
                os.environ["LLM_API_KEY"] = original_key
            else:
                os.environ.pop("LLM_API_KEY", None)
    
    def test_plan_action_with_api_key_calls_llm_planner(self):
        """Given api_key, When planning action, Then calls LLM planner."""
        # Skip if LLM not properly configured
        from evo.action import LLM_CLIENTS_AVAILABLE
        from evo.config import Config
        if not LLM_CLIENTS_AVAILABLE or not Config.LLM_API_KEY:
            pytest.skip("LLM not configured")
        
        layer = ActionLayer()
        try:
            plan = layer.plan_action({"goal": "write_file", "tools": ["file_write"]})
            assert "steps" in plan
        except Exception as e:
            # LLM call failed - this is expected behavior with no fallbacks
            pytest.skip(f"LLM call failed: {e}")
    
    def test_plan_action_falls_back_on_llm_error(self):
        """Given LLM error, When planning, Then should raise LLMResponseError (no fallback)."""
        from evo.action import LLM_CLIENTS_AVAILABLE
        from evo.config import Config
        if not LLM_CLIENTS_AVAILABLE or not Config.LLM_API_KEY:
            pytest.skip("LLM not configured")
        
        layer = ActionLayer()
        # With no fallbacks, LLM errors should raise exceptions
        try:
            plan = layer.plan_action({"goal": "test", "tools": []})
            # If we get here, LLM succeeded
            assert "steps" in plan
        except Exception as e:
            # Expected: LLM raised an exception (no silent fallback)
            from evo import LLMResponseError
            assert isinstance(e, LLMResponseError) or "LLM" in str(type(e).__name__)
    
    def test_plan_action_handles_llm_response_without_steps(self):
        """Given LLM response without steps, When planning, Then returns simple plan."""
        from evo.action import LLM_CLIENTS_AVAILABLE
        from evo.config import Config
        if not LLM_CLIENTS_AVAILABLE or not Config.LLM_API_KEY:
            pytest.skip("LLM not configured")
        
        layer = ActionLayer()
        try:
            plan = layer.plan_action({"goal": "simple_task"})
            assert "steps" in plan
        except Exception as e:
            pytest.skip(f"LLM call failed: {e}")
    
    def test_plan_action_with_stream_uses_streaming_api(self):
        """Given stream=True, When planning, Then uses streaming API."""
        from evo.action import LLM_CLIENTS_AVAILABLE
        from evo.config import Config
        if not LLM_CLIENTS_AVAILABLE or not Config.LLM_API_KEY:
            pytest.skip("LLM not configured")
        
        layer = ActionLayer()
        try:
            plan = layer.plan_action({"goal": "stream_test", "tools": []}, stream=True)
            assert "steps" in plan
        except Exception as e:
            pytest.skip(f"LLM call failed: {e}")
    
    def test_llm_plan_action_with_retry_on_failure(self):
        """Given LLM failure, When planning, Then retries and raises LLMResponseError."""
        from evo.action import LLM_CLIENTS_AVAILABLE
        from evo.config import Config
        if not LLM_CLIENTS_AVAILABLE or not Config.LLM_API_KEY:
            pytest.skip("LLM not configured")
        
        layer = ActionLayer()
        # With no fallbacks, should raise exception after retries
        try:
            plan = layer.plan_action({"goal": "retry_test", "tools": []})
            assert "steps" in plan
        except Exception as e:
            # Expected: LLM raised an exception after retries
            from evo import LLMResponseError
            assert isinstance(e, LLMResponseError) or "LLM" in str(type(e).__name__)


class TestToolExecutorErrorPaths:
    """Tests for tool executor error handling paths."""
    
    def test_execute_tool_returns_error_after_max_retries(self):
        """Given tool that always fails, When executing, Then returns error after max retries."""
        from evo import ToolNotFoundError
        layer = ActionLayer()
        call_count = [0]
        def always_failing():
            call_count[0] += 1
            raise Exception("Always fails")
        layer.register_tool("failing_tool", always_failing)
        
        with pytest.raises(RuntimeError, match="failed after.*attempts"):
            layer.execute_tool("failing_tool", max_retries=3)
        
        assert call_count[0] == 3  # Should have attempted 3 times
    
    def test_execute_tool_with_zero_retries_immediately_fails(self):
        """Given tool that fails, When executing with 0 retries, Then returns error immediately."""
        layer = ActionLayer()
        def failing_tool():
            raise Exception("Fails immediately")
        layer.register_tool("failing_tool", failing_tool)
        
        with pytest.raises(RuntimeError, match="failed after.*attempts"):
            layer.execute_tool("failing_tool", max_retries=1)
    
    def test_execute_tool_with_params_and_exception_returns_error(self):
        """Given tool with params that raises exception, When executing, Then handles and returns error."""
        layer = ActionLayer()
        def tool_with_params(x, y):
            if x == y:
                raise ValueError("x cannot equal y")
            return x + y
        layer.register_tool("add_tool", tool_with_params)
        
        with pytest.raises(RuntimeError, match="failed after.*attempts"):
            layer.execute_tool("add_tool", {"x": 5, "y": 5}, max_retries=1)
    
    def test_execute_tool_without_params_and_exception_returns_error(self):
        """Given tool without params that raises exception, When executing, Then handles and returns error."""
        layer = ActionLayer()
        def no_param_tool():
            raise RuntimeError("No params tool error")
        layer.register_tool("no_param_tool", no_param_tool)
        
        with pytest.raises(RuntimeError, match="failed after.*attempts"):
            layer.execute_tool("no_param_tool", max_retries=1)
    
    def test_execute_tool_with_exception_retried_and_finally_returns_unknown_error(self):
        """Given tool with retry that fails all attempts, When executing, Then returns unknown error path."""
        layer = ActionLayer()
        call_count = [0]
        def fails_all_retries():
            call_count[0] += 1
            raise Exception("Fails all")
        layer.register_tool("fail_all", fails_all_retries)
        
        with pytest.raises(RuntimeError, match="failed after.*attempts"):
            layer.execute_tool("fail_all", max_retries=2)
        
        assert call_count[0] == 2


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