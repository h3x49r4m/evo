"""Action Layer - Action planner and tool executor with LLM integration and config."""

import json
import time
from typing import Any, Callable, Dict, List, Optional
from evo.config import Config

try:
    from evo.llm import LLMClientIFlow, LLMClientOpenRouter, ModelsIFlow, ModelsOpenRouter
    LLM_CLIENTS_AVAILABLE = True
except ImportError:
    LLM_CLIENTS_AVAILABLE = False


class ActionLayer:
    """Action planner and tool executor with LLM-based action planning."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        memory: Optional[Any] = None,
        capability_registry: Optional[Any] = None,
        llm_provider: Optional[str] = None,
        llm_base_url: Optional[str] = None
    ) -> None:
        """Initialize the action layer.
        
        Args:
            api_key: Optional API key for LLM-based planning.
            memory: Optional shared MemorySystem instance for dependency injection.
            capability_registry: Optional CapabilityRegistry for tool registration.
                                 If not provided, creates a new instance.
            llm_provider: Optional LLM provider (iflow, openrouter, openai).
            llm_base_url: Optional custom base URL for LLM API.
        """
        self.api_key = api_key or Config.LLM_API_KEY
        self.memory = memory
        self.capability_registry = capability_registry
        self.llm_provider = llm_provider or Config.LLM_PROVIDER
        self.llm_base_url = llm_base_url or Config.LLM_BASE_URL
        
        # Initialize LLM client based on provider
        self.llm_client = None
        if self.api_key and LLM_CLIENTS_AVAILABLE:
            if self.llm_provider == "iflow":
                base_url = self.llm_base_url or "https://apis.iflow.cn/v1"
                self.llm_client = LLMClientIFlow(api_key=self.api_key, base_url=base_url)
            elif self.llm_provider == "openrouter":
                base_url = self.llm_base_url or "https://openrouter.ai/api/v1"
                self.llm_client = LLMClientOpenRouter(api_key=self.api_key, base_url=base_url)
    
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
    def plan_action(self, goal: Dict[str, Any], stream: bool = False) -> Dict[str, Any]:
        """Create an execution plan for a goal.
        
        Uses OpenAI API for LLM-based planning if API key is provided,
        otherwise falls back to simple planning.
        
        Args:
            goal: Dictionary containing goal description and optional context.
            stream: Whether to use streaming response from OpenAI API.
            
        Returns:
            Dictionary with execution steps and goal.
        """
        # Try LLM-based planning if LLM client is available
        if self.llm_client:
            try:
                llm_plan = self._llm_plan_action(goal, stream=stream)
                if llm_plan and "steps" in llm_plan:
                    return llm_plan
            except Exception:
                # Fall back to simple planning on error
                pass
        
        # Simple fallback planning
        return self._simple_plan_action(goal)
    
    def _llm_plan_action(self, goal: Dict[str, Any], stream: bool = False) -> Dict[str, Any]:
        """Use OpenAI API to create an execution plan.
        
        Args:
            goal: Dictionary containing goal description and optional context.
            stream: Whether to use streaming response from OpenAI API.
            
        Returns:
            Dictionary with execution steps.
        """
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

        # Call LLM API with retry and exponential backoff
        max_retries = Config.LLM_MAX_RETRIES
        base_delay = Config.LLM_RETRY_DELAY
        
        for attempt in range(max_retries):
            try:
                # Get model based on provider
                model = Config.LLM_MODEL
                if self.llm_provider == "iflow":
                    model = model or "deepseek-v3"
                elif self.llm_provider == "openrouter":
                    model = model or "deepseek/deepseek-r1-0528:free"
                
                messages = [
                    {"role": "system", "content": "You are an action planning assistant."},
                    {"role": "user", "content": prompt}
                ]
                
                if stream and self.llm_client:
                    # Streaming response
                    content = self.llm_client.respond_streaming(model, messages, debug=False)
                elif self.llm_client:
                    # Non-streaming response
                    content = self.llm_client.respond(model, messages)
                else:
                    raise RuntimeError("LLM client not available")
                
                # Parse response
                return json.loads(content)
                
            except Exception as e:
                if attempt == max_retries - 1:
                    # Re-raise on last attempt
                    raise
                # Exponential backoff: base_delay * 2^attempt
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
    
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
