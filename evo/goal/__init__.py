"""Goal Engine - External and internal goal management with validation."""

from typing import Any, Dict, List
from evo.validation import validate_goal_name
from evo.logging import get_logger
from evo.config import Config

logger = get_logger("evo.goal")


class GoalEngine:
    """External and internal goal management with drive-based generation."""
    
    # Intrinsic drives for autonomous goal generation
    INTRINSIC_DRIVES = ["curiosity", "competence", "autonomy", "meaning"]
    
    # Drive-specific goal templates
    DRIVE_GOAL_TEMPLATES = {
        "curiosity": {
            "description": "reduce_uncertainty",
            "actions": ["explore_unknown", "ask_questions", "gather_information"]
        },
        "competence": {
            "description": "improve_capability",
            "actions": ["practice_skill", "learn_new_tool", "optimize_process"]
        },
        "autonomy": {
            "description": "independent_action",
            "actions": ["make_decision", "self_direct", "execute_independently"]
        },
        "meaning": {
            "description": "find_purpose",
            "actions": ["reflect_on_values", "evaluate_impact", "align_with_mission"]
        }
    }
    
    def __init__(self) -> None:
        self._external_goals: Dict[str, str] = {}
        self._internal_goals: Dict[str, str] = {}
        self._drive_index = 0
        self._drive_frequency: Dict[str, int] = {drive: 0 for drive in self.INTRINSIC_DRIVES}
    
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
    
    # Autonomous goal generation
    def generate_autonomous_goals(self, drive: str = None) -> List[Dict[str, Any]]:
        """Generate autonomous goals from intrinsic drives.
        
        Args:
            drive: Optional specific drive to use. If None, cycles through drives.
            
        Returns:
            List of goals with drive, priority, feasibility, and actions.
        """
        goals = []
        
        # Select drive(s)
        if drive and drive in self.INTRINSIC_DRIVES:
            drives = [drive]
        else:
            # Cycle through drives
            drives = [self.INTRINSIC_DRIVES[self._drive_index]]
            self._drive_index = (self._drive_index + 1) % len(self.INTRINSIC_DRIVES)
        
        # Generate goals for each drive
        for selected_drive in drives:
            # Track drive usage
            self._drive_frequency[selected_drive] += 1
            
            # Get goal template
            template = self.DRIVE_GOAL_TEMPLATES.get(selected_drive, {
                "description": "default_goal",
                "actions": ["default_action"]
            })
            
            # Create goal with evaluation
            goal = {
                "drive": selected_drive,
                "description": template["description"],
                "actions": template["actions"],
                "priority": self._calculate_priority(selected_drive),
                "feasibility": self._calculate_feasibility(selected_drive),
                "learning_potential": 0.7  # Default learning potential
            }
            
            goals.append(goal)
            
            # Add to internal goals
            goal_name = f"{selected_drive}_goal_{self._drive_frequency[selected_drive]}"
            self.add_internal_goal(goal_name, template["description"])
        
        return goals
    
    def _calculate_priority(self, drive: str) -> float:
        """Calculate priority for a drive based on frequency."""
        # Lower frequency = higher priority (balance drives)
        frequency = self._drive_frequency.get(drive, 0)
        priority = 1.0 - min(1.0, frequency / Config.DRIVE_PRIORITY_DIVISOR)
        return priority
    
    def _calculate_feasibility(self, drive: str) -> float:
        """Calculate feasibility for a drive-based goal."""
        # Base feasibility on drive type
        base_feasibility = {
            "curiosity": 0.9,
            "competence": 0.8,
            "autonomy": 0.7,
            "meaning": 0.6
        }
        return base_feasibility.get(drive, 0.8)
    
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
