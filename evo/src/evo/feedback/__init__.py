"""Feedback Loop - Observation processor and memory manager."""

from typing import Any, Dict, List
from evo.memory import MemorySystem


class FeedbackLoop:
    """Observation processor and memory manager."""
    
    def __init__(self) -> None:
        self._memory = MemorySystem(collection_name="feedback")
        self._observations: List[Dict[str, Any]] = []
    
    # Observation processor
    def process_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Process observation and extract key information."""
        processed = {
            "action": observation.get("action"),
            "result": observation.get("result"),
            "output": observation.get("output"),
            "timestamp": observation.get("timestamp")
        }
        self._observations.append(processed)
        return processed
    
    def detect_patterns(self) -> List[Dict[str, Any]]:
        """Detect patterns from accumulated observations."""
        patterns = []
        action_counts = {}
        for obs in self._observations:
            action = obs.get("action")
            if action:
                action_counts[action] = action_counts.get(action, 0) + 1
        
        for action, count in action_counts.items():
            if count >= 2:
                patterns.append({"action": action, "frequency": count})
        
        return patterns
    
    # Memory manager
    def store_observation(self, observation: Dict[str, Any]) -> None:
        """Store observation in working and episodic memory."""
        # Store in working memory
        self._memory.working.store("last_observation", observation)
        # Store in episodic memory (simplified - just count)
        current_count = self._memory.working.retrieve("episodic_count") or 0
        self._memory.working.store("episodic_count", current_count + 1)
    
    def get_working_memory_size(self) -> int:
        """Get size of working memory."""
        return len(self._memory.working.context)
    
    def get_episodic_memory_count(self) -> int:
        """Get count of episodic memories."""
        return self._memory.working.retrieve("episodic_count") or 0
    
    def update_semantic_memory(self, key: str, value: str) -> None:
        """Update semantic memory with learnings."""
        self._memory.semantic.add_fact(key, value)
    
    def get_semantic_fact(self, key: str) -> Any:
        """Get fact from semantic memory."""
        return self._memory.semantic.retrieve_fact(key)