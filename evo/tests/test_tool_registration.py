"""Tests for consolidated tool registration."""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.action import ActionLayer
from evo.capability import CapabilityRegistry


def test_action_layer_uses_capability_registry():
    """Test that ActionLayer uses CapabilityRegistry for tool registration."""
    registry = CapabilityRegistry()
    action = ActionLayer(capability_registry=registry)
    
    # Register a tool via action layer
    def test_tool():
        return "test result"
    
    action.register_tool("test_tool", test_tool, "A test tool")
    
    # Verify tool is in capability registry
    assert "test_tool" in registry.list_tools()
    tool_data = registry.get_tool("test_tool")
    assert tool_data["callable"] == test_tool
    assert tool_data["description"] == "A test tool"


def test_action_layer_fallback_internal_storage():
    """Test that ActionLayer uses internal storage when no capability_registry."""
    action = ActionLayer(capability_registry=None)
    
    # Register a tool via action layer
    def test_tool():
        return "test result"
    
    action.register_tool("test_tool", test_tool, "A test tool")
    
    # Verify tool is accessible and executable
    assert "test_tool" in action._internal_tools
    result = action.execute_tool("test_tool")
    assert result == "test result"


def test_action_layer_execute_from_registry():
    """Test that execute_tool retrieves tools from capability_registry."""
    registry = CapabilityRegistry()
    action = ActionLayer(capability_registry=registry)
    
    # Register tool via registry
    def test_tool(param1, param2="default"):
        return {"param1": param1, "param2": param2}
    
    registry.register_tool("test_tool", "Test tool description", test_tool)
    
    # Execute via action layer
    result = action.execute_tool("test_tool", params={"param1": "value1", "param2": "value2"})
    assert result["param1"] == "value1"
    assert result["param2"] == "value2"


def test_action_layer_llm_plan_uses_registry_tools():
    """Test that LLM planner uses tools from capability_registry."""
    registry = CapabilityRegistry()
    action = ActionLayer(capability_registry=registry)
    
    # Register some tools
    registry.register_tool("tool1", "First tool", lambda: "result1")
    registry.register_tool("tool2", "Second tool", lambda: "result2")
    
    # The simple planner should use available tools
    goal = {"goal": "Use tool1", "tools": ["tool1"]}
    plan = action._simple_plan_action(goal)
    
    assert "steps" in plan
    assert len(plan["steps"]) == 1
    assert plan["steps"][0]["tool"] == "tool1"


def test_tool_not_found_error():
    """Test that executing non-existent tool returns error."""
    registry = CapabilityRegistry()
    action = ActionLayer(capability_registry=registry)
    
    result = action.execute_tool("nonexistent_tool")
    assert "error" in result
    assert "not found" in result["error"]


def test_shared_registry_across_layers():
    """Test that multiple ActionLayers can share the same CapabilityRegistry."""
    registry = CapabilityRegistry()
    
    action1 = ActionLayer(capability_registry=registry)
    action2 = ActionLayer(capability_registry=registry)
    
    # Register tool via action1
    def test_tool():
        return "shared result"
    
    action1.register_tool("shared_tool", test_tool, "Shared tool")
    
    # Both action layers should see the tool
    assert "shared_tool" in action1.capability_registry.list_tools()
    assert "shared_tool" in action2.capability_registry.list_tools()
    
    # Both should be able to execute it
    result1 = action1.execute_tool("shared_tool")
    result2 = action2.execute_tool("shared_tool")
    assert result1 == "shared result"
    assert result2 == "shared result"


def test_action_layer_without_registry_no_tools():
    """Test that ActionLayer without registry starts with no tools."""
    action = ActionLayer(capability_registry=None)
    
    # Should not have internal tools initially
    assert not hasattr(action, '_internal_tools') or len(action._internal_tools) == 0


def test_execute_tool_retry_logic_with_registry():
    """Test that retry logic works with tools from capability_registry."""
    registry = CapabilityRegistry()
    action = ActionLayer(capability_registry=registry)
    
    call_count = 0
    
    def flaky_tool():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise Exception("First attempt fails")
        return "success after retry"
    
    registry.register_tool("flaky_tool", "A flaky tool", flaky_tool)
    
    result = action.execute_tool("flaky_tool", max_retries=3)
    assert result == "success after retry"
    assert call_count == 2