"""Exploration Engine - Novelty detection and purpose synthesis."""

from typing import Any, Dict, List


class ExplorationEngine:
    """Novelty detection and purpose synthesis."""
    
    def __init__(self) -> None:
        self._capabilities: Dict[str, bool] = {}
    
    # Novelty detector
    def register_capability(self, name: str, used: bool) -> None:
        """Register a capability and track if it's been used."""
        self._capabilities[name] = used
    
    def detect_novelty(self) -> List[str]:
        """Detect unused capabilities (novelty)."""
        return [name for name, used in self._capabilities.items() if not used]
    
    # Random exploration
    def random_exploration(self) -> Dict[str, str]:
        """Generate a random exploration goal."""
        return {
            "goal": "explore_unknown",
            "type": "random"
        }
    
    # Purpose synthesis
    def synthesize_purpose(self, reflections: Dict[str, Any]) -> Dict[str, str]:
        """Synthesize purpose from reflections and drives."""
        return {
            "purpose": "self_improvement",
            "statement": "I exist to learn, improve, and find meaning through continuous exploration."
        }