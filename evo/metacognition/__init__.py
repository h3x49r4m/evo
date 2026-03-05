"""Metacognition Layer - Reflection and self-model update."""

import time
from typing import Any, Dict, List
from evo.types import BeliefValue
from evo.config import Config


class MetacognitionLayer:
    """Reflection and self-model update with automatic reflection triggers."""
    
    def __init__(self) -> None:
        self._self_model: Dict[str, Any] = {
            "capabilities": {},
            "beliefs": {},
            "goal_strategy": "default",
            "reflection_count": 0,
            "last_reflection": 0
        }
        self._learned_strategies: List[Dict[str, Any]] = []
        self._insights: List[Dict[str, Any]] = []
    
    # Reflection trigger
    def trigger_reflection(self, trigger_type: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Trigger a reflection event."""
        return {
            "type": "reflection",
            "trigger": trigger_type,
            "data": data or {}
        }
    
    # Automatic reflection
    def auto_reflection(self, experiences: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform automatic reflection and update self-model.
        
        Args:
            experiences: List of recent experiences to reflect on.
            
        Returns:
            Dictionary containing insights, patterns, and processing status.
        """
        experiences = experiences or []
        
        # Update reflection count and timestamp
        self._self_model["reflection_count"] = self._self_model.get("reflection_count", 0) + 1
        self._self_model["last_reflection"] = time.time()
        
        # Process experiences and update self-model
        insights = self._generate_insights(experiences)
        patterns = self._identify_patterns(experiences)
        
        # Update capabilities based on outcomes
        self._update_capabilities_from_experiences(experiences)
        
        # Update beliefs based on experiences
        self._update_beliefs_from_experiences(experiences)
        
        return {
            "processed": len(experiences),
            "insights": insights,
            "patterns": patterns,
            "reflection_number": self._self_model["reflection_count"]
        }
    
    def _generate_insights(self, experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate insights from experiences."""
        insights = []
        
        if not experiences:
            insights.append({"type": "no_data", "message": "No experiences to analyze"})
            return insights
        
        # Count outcomes
        outcomes = {}
        for exp in experiences:
            outcome = exp.get("outcome", "unknown")
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
        
        # Generate insight about most common outcome
        if outcomes:
            most_common = max(outcomes, key=outcomes.get)
            insights.append({
                "type": "outcome_pattern",
                "message": f"Most common outcome: {most_common}",
                "count": outcomes[most_common]
            })
        
        return insights
    
    def _identify_patterns(self, experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify patterns in experiences."""
        patterns = []
        
        if len(experiences) < 2:
            return patterns
        
        # Look for repeated actions with same outcome
        action_outcomes = {}
        for exp in experiences:
            action = exp.get("action", "unknown")
            outcome = exp.get("outcome", "unknown")
            key = f"{action}:{outcome}"
            action_outcomes[key] = action_outcomes.get(key, 0) + 1
        
        # Identify patterns (actions that repeat with same outcome)
        for key, count in action_outcomes.items():
            if count >= Config.METACOGNITION_PATTERN_THRESHOLD:
                action, outcome = key.split(":")
                patterns.append({
                    "action": action,
                    "outcome": outcome,
                    "frequency": count
                })
        
        return patterns
    
    def _update_capabilities_from_experiences(self, experiences: List[Dict[str, Any]]) -> None:
        """Update capabilities based on experience outcomes."""
        if not experiences:
            return
        
        for exp in experiences:
            action = exp.get("action")
            outcome = exp.get("outcome")
            confidence = exp.get("confidence", 0.5)
            
            if not action or not outcome:
                continue
            
            # Get current capability level
            current_level = self._self_model["capabilities"].get(action, 0.5)
            
            # Update based on outcome
            if outcome == "success":
                new_level = min(1.0, current_level + (Config.CAPABILITY_UPDATE_MULTIPLIER * confidence))
            elif outcome == "failure":
                new_level = max(0.0, current_level - (Config.CAPABILITY_UPDATE_MULTIPLIER * (1 - confidence)))
            else:
                # Slight adjustment for unknown outcomes
                new_level = current_level
            
            self._self_model["capabilities"][action] = new_level
    
    def _update_beliefs_from_experiences(self, experiences: List[Dict[str, Any]]) -> None:
        """Update beliefs based on experiences."""
        if not experiences:
            return
        
        for exp in experiences:
            belief_key = exp.get("belief_key")
            outcome = exp.get("outcome")
            
            if belief_key:
                # Update belief based on outcome
                if outcome == "success":
                    self._self_model["beliefs"][belief_key] = True
                elif outcome == "failure":
                    self._self_model["beliefs"][belief_key] = False
    
    # Self-model update
    def update_capabilities(self, capability: str, level: float) -> None:
        """Update a capability in the self-model."""
        self._self_model["capabilities"][capability] = level
    
    def update_beliefs(self, belief: str, value: BeliefValue) -> None:
        """Update a belief in the self-model."""
        self._self_model["beliefs"][belief] = value
    
    def get_self_model(self) -> Dict[str, Any]:
        """Get the current self-model."""
        return self._self_model
    
    # Meta-learning
    def learn_from_experience(self, experience: Dict[str, Any]) -> None:
        """Learn from experience and update strategies."""
        strategy = {
            "outcome": experience.get("outcome"),
            "strategy": experience.get("strategy"),
            "learned_at": "now"
        }
        self._learned_strategies.append(strategy)
    
    def get_learned_strategies(self) -> List[Dict[str, Any]]:
        """Get all learned strategies."""
        return self._learned_strategies