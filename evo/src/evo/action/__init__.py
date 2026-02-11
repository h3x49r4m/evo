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
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        memory: Optional[Any] = None,
        capability_registry: Optional[Any] = None
    ) -> None:
        """Initialize the action layer.
        
        Args:
            api_key: Optional OpenAI API key for LLM-based planning.
            memory: Optional shared MemorySystem instance for dependency injection.
            capability_registry: Optional CapabilityRegistry for tool registration.
                                 If not provided, creates a new instance.
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.memory = memory
        self.capability_registry = capability_registry
        
        if self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
    
    # Tool registration (delegates to capability_registry if available)
    def register_tool(self, name: str, callable_func: Callable, description: str = "") -> None:
        """Register a tool for execution.
        
        Delegates to capability_registry if available, otherwise uses internal storage.
        
        Args:
            name: Name of the tool.
            callable_func: Function to execute for the tool.
            description: Optional description of the tool.
        """
        if self.capability_registry:
            self.capability_registry.register_tool(name, description, callable_func)
        else:
            # Fallback: create internal registry if none provided
            if not hasattr(self, '_internal_tools'):
                self._internal_tools: Dict[str, Callable] = {}
            self._internal_tools[name] = callable_func
    
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
        
        # Get available tools from capability_registry or internal storage
        if self.capability_registry:
            available_tools = self.capability_registry.list_tools()
        elif hasattr(self, '_internal_tools'):
            available_tools = list(self._internal_tools.keys())
        else:
            available_tools = []
        
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
        # Get tool from capability_registry or internal storage
        tool = None
        if self.capability_registry:
            tool_data = self.capability_registry.get_tool(tool_name)
            if tool_data and tool_data.get("callable"):
                tool = tool_data["callable"]
        elif hasattr(self, '_internal_tools') and tool_name in self._internal_tools:
            tool = self._internal_tools[tool_name]
        
        if tool is None:
            return {"error": f"Tool '{tool_name}' not found"}
        
        params = params or {}
        max_retries = max_retries or Config.ACTION_MAX_RETRIES
        
        for attempt in range(max_retries):
            try:
                if params:
                    return tool(**params)
                return tool()
            except Exception as e:
                if attempt == max_retries - 1:
                    return {"error": f"Tool '{tool_name}' failed after {max_retries} attempts"}
                time.sleep(Config.ACTION_RETRY_DELAY)  # Use config value
        
        return {"error": "Unknown error"}
