"""Perception Gateway - Filters, prioritizes, and routes inputs."""

from typing import Any, Dict, List, Optional
from evo.config import Config


class PerceptionGateway:
    """Filters, prioritizes, and routes inputs to appropriate contexts.
    
    Priority levels are configurable via environment variables:
    - PERCEPTION_PRIORITY_SAFETY: Default 0 (highest priority)
    - PERCEPTION_PRIORITY_USER: Default 1
    - PERCEPTION_PRIORITY_INTERNET: Default 2
    - PERCEPTION_PRIORITY_ENVIRONMENT: Default 3
    - PERCEPTION_PRIORITY_SYSTEM: Default 4 (lowest priority)
    """
    
    # Priority levels for different sources (configurable)
    PRIORITY_MAP = {
        "safety": Config.PERCEPTION_PRIORITY_SAFETY,
        "user": Config.PERCEPTION_PRIORITY_USER,
        "internet": Config.PERCEPTION_PRIORITY_INTERNET,
        "environment": Config.PERCEPTION_PRIORITY_ENVIRONMENT,
        "system": Config.PERCEPTION_PRIORITY_SYSTEM,
    }
    
    def __init__(self) -> None:
        self._input_queue: List[Dict[str, Any]] = []
    
    # Input filtering and routing
    def filter_and_route(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Filter input and route to appropriate context."""
        if not input_data:
            return None
        
        source = input_data.get("source", "system")
        
        context_map = {
            "safety": "safety",
            "user": "user",
            "environment": "sensor",
            "internet": "network",
        }
        
        context = context_map.get(source, "system")
        
        return {
            "context": context,
            "data": input_data
        }
    
    # Input queue management
    def add_input(self, input_data: Dict[str, Any]) -> None:
        """Add an input to the queue."""
        self._input_queue.append(input_data)
    
    def queue_size(self) -> int:
        """Get the current size of the input queue."""
        return len(self._input_queue)
    
    def get_next_input(self) -> Optional[Dict[str, Any]]:
        """Get the next input from the queue and remove it."""
        if not self._input_queue:
            return None
        return self._input_queue.pop(0)
    
    # Input prioritization
    def get_prioritized_inputs(self) -> List[Dict[str, Any]]:
        """Get all inputs sorted by priority."""
        def get_priority(input_data: Dict[str, Any]) -> int:
            source = input_data.get("source", "system")
            if "priority" in input_data:
                return input_data["priority"]
            return self.PRIORITY_MAP.get(source, 999)
        
        return sorted(self._input_queue, key=get_priority)