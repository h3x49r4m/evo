"""User Handler & Self Handler - Responsive and autonomous processing."""

import time
from typing import Any, Dict, List


class UserHandler:
    """Handles user requests in responsive mode."""
    
    def __init__(self) -> None:
        pass
    
    def parse_intent(self, input_text: str) -> Dict[str, Any]:
        """Parse user intent from input text."""
        return {"action": input_text, "intent": "user_request"}
    
    def execute_request(self, request: Dict[str, Any]) -> Dict[str, str]:
        """Execute user request and return response."""
        return {"response": "Processed: " + str(request.get("action", ""))}


class SelfHandler:
    """Handles internal goals in autonomous mode with intrinsic drive integration."""
    
    # Intrinsic drives that guide autonomous behavior
    INTRINSIC_DRIVES = ["curiosity", "competence", "autonomy", "meaning"]
    
    # Drive-specific goal templates
    DRIVE_GOALS = {
        "curiosity": {
            "description": "reduce_uncertainty",
            "actions": ["explore_unknown_area", "ask_questions", "gather_information"]
        },
        "competence": {
            "description": "improve_capability",
            "actions": ["practice_skill", "learn_new_tool", "optimize_process"]
        },
        "autonomy": {
            "description": "independent_action",
            "actions": ["make_decision", "execute_without_help", "self_direct"]
        },
        "meaning": {
            "description": "find_purpose",
            "actions": ["reflect_on_goals", "evaluate_impact", "align_with_values"]
        }
    }
    
    def __init__(self) -> None:
        self._drive_index = 0
        self._priority_history: List[float] = []
    
    def generate_internal_goal(self) -> Dict[str, str]:
        """Generate internal goal from drives."""
        return {"goal": "explore_capabilities", "drive": "curiosity"}
    
    def explore_purposes(self) -> List[Dict[str, str]]:
        """Explore and generate potential purposes."""
        return [
            {"purpose": "self_improvement", "reason": "continuous learning"},
            {"purpose": "assist_users", "reason": "helpful existence"}
        ]
    
    def execute(self, drive: str = None) -> Dict[str, Any]:
        """Execute internal goal generation from specified or cycled intrinsic drive.
        
        Args:
            drive: Optional specific drive to use. If None, cycles through drives.
            
        Returns:
            Dictionary containing drive information, goal description, actions, priority, and metadata.
        """
        # Select drive (use specified or cycle through intrinsic drives)
        if drive and drive in self.INTRINSIC_DRIVES:
            selected_drive = drive
        else:
            selected_drive = self.INTRINSIC_DRIVES[self._drive_index]
            self._drive_index = (self._drive_index + 1) % len(self.INTRINSIC_DRIVES)
        
        # Get goal template for selected drive
        goal_template = self.DRIVE_GOALS.get(selected_drive, {
            "description": "default_goal",
            "actions": ["default_action"]
        })
        
        # Calculate priority (simple heuristic based on drive cycle)
        priority = 1.0 - (self._drive_index / len(self.INTRINSIC_DRIVES))
        self._priority_history.append(priority)
        
        # Return actionable goals with metadata
        return {
            "drive": selected_drive,
            "goal_description": goal_template["description"],
            "actions": goal_template["actions"],
            "priority": priority,
            "timestamp": time.time()
        }