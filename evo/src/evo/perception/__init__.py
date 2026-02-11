"""Perception Gateway - Filters, prioritizes, and routes inputs."""

from typing import Any, Dict, List, Optional


class PerceptionGateway:
    """Filters, prioritizes, and routes inputs to appropriate contexts."""
    
    # Priority levels for different sources
    PRIORITY_MAP = {
        "safety": 0,
        "user": 1,
        "internet": 2,
        "environment": 3,
        "system": 4,
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