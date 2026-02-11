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