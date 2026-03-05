"""Feedback Loop - Observation processor and memory manager with learning integration."""

from typing import Any, Dict, List, Optional
from evo.memory import MemorySystem
from evo.config import Config


class FeedbackLoop:
    """Observation processor and memory manager with learning integration."""
    
    def __init__(self, memory: Optional[MemorySystem] = None) -> None:
        """Initialize the feedback loop.
        
        Args:
            memory: Optional shared MemorySystem instance for dependency injection.
                   If not provided, creates a new instance.
        """
        self._memory = memory or MemorySystem(collection_name="feedback")
        self._observations: List[Dict[str, Any]] = []
        # Action frequency index for O(1) pattern detection
        self._action_frequency: Dict[str, int] = {}
        # Track success/failure counts for each action
        self._action_outcomes: Dict[str, Dict[str, int]] = {}
    
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
        
        # Update action frequency index
        action = processed.get("action")
        if action:
            self._action_frequency[action] = self._action_frequency.get(action, 0) + 1
            
            # Track outcomes for this action
            if action not in self._action_outcomes:
                self._action_outcomes[action] = {"success": 0, "failure": 0}
            
            result = processed.get("result", "").lower()
            if "success" in result:
                self._action_outcomes[action]["success"] += 1
            elif "failure" in result:
                self._action_outcomes[action]["failure"] += 1
        
        return processed
    
    def detect_patterns(self) -> List[Dict[str, Any]]:
        """Detect patterns from accumulated observations.
        
        Optimized to use pre-built action frequency index instead of
        iterating through all observations (O(1) vs O(n)).
        """
        patterns = []
        # Use pre-built frequency index - O(n) where n is unique actions, not total observations
        for action, count in self._action_frequency.items():
            if count >= Config.PATTERN_DETECTION_THRESHOLD:
                patterns.append({"action": action, "frequency": count})
        
        return patterns
    
    # Learning integration
    def get_learnings(self) -> Dict[str, Any]:
        """Get learnings from accumulated observations for improved decision-making.
        
        Returns:
            Dictionary containing observations, patterns, success rates, recommendations,
            and other learning insights.
        """
        # Detect patterns
        patterns = self.detect_patterns()
        
        # Calculate success rates
        success_rates = {}
        for action, outcomes in self._action_outcomes.items():
            total = outcomes["success"] + outcomes["failure"]
            if total > 0:
                success_rates[action] = outcomes["success"] / total
        
        # Identify best and failing actions
        best_actions = [action for action, rate in success_rates.items() if rate >= Config.BEST_ACTION_SUCCESS_THRESHOLD]
        failing_actions = [action for action, rate in success_rates.items() if rate <= Config.FAILING_ACTION_SUCCESS_THRESHOLD]
        
        # Generate recommendations
        recommendations = []
        if best_actions:
            recommendations.append({
                "type": "use_best_actions",
                "actions": best_actions,
                "reason": "These actions have high success rates"
            })
        if failing_actions:
            recommendations.append({
                "type": "avoid_failing_actions",
                "actions": failing_actions,
                "reason": "These actions have low success rates"
            })
        
        # Calculate confidence score based on amount of data
        confidence = min(1.0, len(self._observations) / Config.CONFIDENCE_DIVISOR)
        
        # Extract key facts for semantic memory
        key_facts = []
        if best_actions:
            key_facts.append(f"Best performing actions: {', '.join(best_actions)}")
        if failing_actions:
            key_facts.append(f"Actions to avoid: {', '.join(failing_actions)}")
        
        # Calculate learning score
        learning_score = min(1.0, len(self._observations) / Config.LEARNING_SCORE_DIVISOR)
        
        return {
            "observations": self._observations.copy(),
            "patterns": patterns,
            "success_rates": success_rates,
            "best_actions": best_actions,
            "failing_actions": failing_actions,
            "recommendations": recommendations,
            "confidence": confidence,
            "key_facts": key_facts,
            "learning_score": learning_score
        }
    
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