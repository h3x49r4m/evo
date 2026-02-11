"""Action Layer - Action planner and tool executor."""

import time
from typing import Any, Callable, Dict, List


class ActionLayer:
    """Action planner and tool executor."""
    
    def __init__(self) -> None:
        self._tools: Dict[str, Callable] = {}
    
    # Tool registration
    def register_tool(self, name: str, callable_func: Callable) -> None:
        """Register a tool for execution."""
        self._tools[name] = callable_func
    
    # Action planner
    def plan_action(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Create an execution plan for a goal."""
        steps = []
        tools = goal.get("tools", [])
        
        if tools:
            for tool in tools:
                steps.append({"tool": tool, "action": "execute"})
        
        if not steps:
            # Create a default step if no tools specified
            steps.append({"tool": goal.get("goal", "unknown"), "action": "execute"})
        
        return {"steps": steps, "goal": goal}
    
    # Tool executor
    def execute_tool(self, tool_name: str, params: Dict[str, Any] = None, max_retries: int = 1) -> Any:
        """Execute a tool with optional retry logic."""
        if tool_name not in self._tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        params = params or {}
        
        for attempt in range(max_retries):
            try:
                tool = self._tools[tool_name]
                if params:
                    return tool(**params)
                return tool()
            except Exception:
                if attempt == max_retries - 1:
                    return {"error": f"Tool '{tool_name}' failed after {max_retries} attempts"}
                time.sleep(0.1)  # Small delay between retries
        
        return {"error": "Unknown error"}