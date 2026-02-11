"""Goal Engine - External and internal goal management with validation."""

from typing import Any, Dict, List
from evo.validation import validate_goal_name
from evo.logging import get_logger

logger = get_logger("evo.goal")


class GoalEngine:
    """External and internal goal management with drive-based generation."""
    
    def __init__(self) -> None:
        self._external_goals: Dict[str, str] = {}
        self._internal_goals: Dict[str, str] = {}
    
    # External goals
    def add_external_goal(self, name: str, description: str) -> None:
        """Add an external goal from user."""
        if not validate_goal_name(name):
            raise ValueError(f"Invalid goal name: {name}")
        self._external_goals[name] = description
        logger.info(f"Added external goal: {name}")
    
    def remove_external_goal(self, name: str) -> None:
        """Remove an external goal."""
        self._external_goals.pop(name, None)
        logger.info(f"Removed external goal: {name}")
    
    def list_external_goals(self) -> List[str]:
        """List all external goal names."""
        return list(self._external_goals.keys())
    
    # Internal goals
    def add_internal_goal(self, name: str, description: str) -> None:
        """Add an internal goal."""
        if not validate_goal_name(name):
            raise ValueError(f"Invalid goal name: {name}")
        self._internal_goals[name] = description
        logger.debug(f"Added internal goal: {name}")
    
    def list_internal_goals(self) -> List[str]:
        """List all internal goal names."""
        return list(self._internal_goals.keys())
    
    # Drive-based goal generation
    def generate_curiosity_goal(self) -> Dict[str, str]:
        """Generate goal from curiosity drive - reduce uncertainty."""
        return {
            "drive": "curiosity",
            "description": "reduce_uncertainty"
        }
    
    def generate_competence_goal(self) -> Dict[str, str]:
        """Generate goal from competence drive - improve capabilities."""
        return {
            "drive": "competence",
            "description": "improve_capability"
        }
    
    def generate_autonomy_goal(self) -> Dict[str, str]:
        """Generate goal from autonomy drive - expand independence."""
        return {
            "drive": "autonomy",
            "description": "independent_action"
        }
    
    def generate_meaning_goal(self) -> Dict[str, str]:
        """Generate goal from meaning drive - discover purpose."""
        return {
            "drive": "meaning",
            "description": "find_purpose"
        }
    
    # Goal evaluation
    def evaluate_goal(self, goal: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate goal with feasibility, learning potential, and drive alignment."""
        return {
            "feasibility": 0.8,
            "learning_potential": 0.7,
            "drive_alignment": 0.9
        }
    
    # Goal prioritization
    def prioritize_goals(self) -> List[Dict[str, str]]:
        """Prioritize goals, external goals always come first."""
        prioritized = []
        for name in self._external_goals:
            prioritized.append({"name": name, "source": "external"})
        for name in self._internal_goals:
            prioritized.append({"name": name, "source": "internal"})
        return prioritized
