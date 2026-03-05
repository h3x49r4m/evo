"""Exploration Engine - Novelty detection and purpose synthesis with action execution."""

from typing import Any, Dict, List
from evo.config import Config


class ExplorationEngine:
    """Novelty detection and purpose synthesis with action execution."""
    
    def __init__(self) -> None:
        self._capabilities: Dict[str, bool] = {}
        self._exploration_history: List[Dict[str, Any]] = []
        self._exploration_count = 0
    
    # Novelty detector
    def register_capability(self, name: str, used: bool) -> None:
        """Register a capability and track if it's been used."""
        self._capabilities[name] = used
    
    def detect_novelty(self) -> List[str]:
        """Detect unused capabilities (novelty)."""
        return [name for name, used in self._capabilities.items() if not used]
    
    # Exploration execution
    def explore(self) -> Dict[str, Any]:
        """Execute exploration actions and discover new capabilities.
        
        Returns:
            Dictionary containing actions, goals, plan, purposes, and exploration status.
        """
        self._exploration_count += 1
        
        # Detect unused capabilities
        unused_capabilities = self.detect_novelty()
        
        # Generate exploration goals
        goals = self._generate_exploration_goals(unused_capabilities)
        
        # Create executable plan
        plan = self._create_exploration_plan(unused_capabilities)
        
        # Synthesize purposes
        purposes = self._synthesize_purposes_from_exploration()
        
        # Select actions
        actions = self._select_exploration_actions(unused_capabilities)
        
        # Record exploration
        exploration_record = {
            "exploration_number": self._exploration_count,
            "capabilities_found": len(unused_capabilities),
            "actions_executed": len(actions),
            "timestamp": "now"
        }
        self._exploration_history.append(exploration_record)
        
        return {
            "actions": actions,
            "goals": goals,
            "plan": plan,
            "purposes": purposes,
            "exploration_number": self._exploration_count,
            "record": exploration_record
        }
    
    def _generate_exploration_goals(self, unused_capabilities: List[str]) -> List[Dict[str, str]]:
        """Generate exploration goals based on unused capabilities."""
        goals = []
        
        if unused_capabilities:
            for cap in unused_capabilities:
                goals.append({
                    "goal": f"explore_{cap}",
                    "type": "capability_discovery",
                    "priority": "medium"
                })
        else:
            goals.append({
                "goal": "general_exploration",
                "type": "random",
                "priority": "low"
            })
        
        return goals
    
    def _create_exploration_plan(self, unused_capabilities: List[str]) -> Dict[str, Any]:
        """Create executable exploration plan."""
        plan = {
            "steps": [],
            "estimated_duration": "short",
            "success_criteria": ["discover_new_information"]
        }
        
        if unused_capabilities:
            for cap in unused_capabilities[:Config.EXPLORATION_PLAN_STEP_LIMIT]:
                plan["steps"].append({
                    "action": "try_capability",
                    "target": cap,
                    "purpose": "discover_new_knowledge"
                })
        else:
            plan["steps"].append({
                "action": "random_search",
                "purpose": "find_unknown_areas"
            })
        
        return plan
    
    def _select_exploration_actions(self, unused_capabilities: List[str]) -> List[str]:
        """Select exploration actions based on unused capabilities."""
        actions = []
        
        if unused_capabilities:
            # Prioritize unused capabilities
            actions = [f"try_{cap}" for cap in unused_capabilities[:Config.EXPLORATION_ACTION_LIMIT]]
        else:
            # Fall back to random exploration
            actions = ["random_search", "try_new_approach"]
        
        return actions
    
    def _synthesize_purposes_from_exploration(self) -> List[Dict[str, str]]:
        """Synthesize new purposes from exploration."""
        purposes = [
            {
                "purpose": "continuous_learning",
                "reason": "Exploration reveals new areas to learn"
            },
            {
                "purpose": "capability_expansion",
                "reason": "Discovering new capabilities increases autonomy"
            }
        ]
        
        return purposes
    
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