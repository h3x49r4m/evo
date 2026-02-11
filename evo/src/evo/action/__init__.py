"""Action Layer - Action planner and tool executor with LLM integration and config."""

import json
import time
from typing import Any, Callable, Dict, List, Optional
from evo.config import Config

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ActionLayer:
    """Action planner and tool executor with LLM-based action planning."""
    
    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize the action layer.
        
        Args:
            api_key: Optional OpenAI API key for LLM-based planning.
        """
        self._tools: Dict[str, Callable] = {}
        self.api_key = api_key or Config.OPENAI_API_KEY
        
        if self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
    
    # Tool registration
    def register_tool(self, name: str, callable_func: Callable) -> None:
        """Register a tool for execution."""
        self._tools[name] = callable_func
    
    # Action planner
    def plan_action(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Create an execution plan for a goal.
        
        Uses OpenAI API for LLM-based planning if API key is provided,
        otherwise falls back to simple planning.
        
        Args:
            goal: Dictionary containing goal description and optional context.
            
        Returns:
            Dictionary with execution steps and goal.
        """
        # Try LLM-based planning if API key available
        if self.api_key and OPENAI_AVAILABLE:
            try:
                llm_plan = self._llm_plan_action(goal)
                if llm_plan and "steps" in llm_plan:
                    return llm_plan
            except Exception:
                # Fall back to simple planning on error
                pass
        
        # Simple fallback planning
        return self._simple_plan_action(goal)
    
    def _llm_plan_action(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Use OpenAI API to create an execution plan."""
        goal_text = goal.get("goal", "")
        context = goal.get("context", {})
        available_tools = list(self._tools.keys())
        
        # Build prompt for LLM
        prompt = f"""You are an AI assistant that plans actions to achieve goals.

Goal: {goal_text}

Available tools: {', '.join(available_tools) if available_tools else 'none'}

Context: {json.dumps(context, indent=2)}

Create a JSON response with this format:
{{"steps": [{{"tool": "tool_name", "action": "execute"}}]}}

Only use tools from the available list. Be specific and concise."""

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an action planning assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=Config.OPENAI_TEMPERATURE
        )
        
        # Parse response
        content = response.choices[0].message.content
        return json.loads(content)
    
    def _simple_plan_action(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Simple fallback action planner without LLM."""
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
    def execute_tool(self, tool_name: str, params: Dict[str, Any] = None, max_retries: Optional[int] = None) -> Any:
        """Execute a tool with optional retry logic.
        
        Args:
            tool_name: Name of the tool to execute.
            params: Optional parameters to pass to the tool.
            max_retries: Maximum number of retry attempts.
            
        Returns:
            Result from tool execution or error dictionary.
        """
        if tool_name not in self._tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        params = params or {}
        max_retries = max_retries or Config.ACTION_MAX_RETRIES
        
        for attempt in range(max_retries):
            try:
                tool = self._tools[tool_name]
                if params:
                    return tool(**params)
                return tool()
            except Exception as e:
                if attempt == max_retries - 1:
                    return {"error": f"Tool '{tool_name}' failed after {max_retries} attempts"}
                time.sleep(Config.ACTION_RETRY_DELAY)  # Use config value
        
        return {"error": "Unknown error"}
