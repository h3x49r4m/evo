"""Main entry point for the evo autonomous agent system."""

from typing import Any, Dict, Optional
from evo.perception import PerceptionGateway
from evo.decision import DecisionEngine
from evo.goal import GoalEngine
from evo.capability import CapabilityRegistry
from evo.action import ActionLayer
from evo.memory import MemorySystem
from evo.metacognition import MetacognitionLayer
from evo.exploration import ExplorationEngine
from evo.safety import SafetyLayer
from evo.feedback import FeedbackLoop
from evo.handler import UserHandler, SelfHandler
from evo.integrative_core import IntegrativeCore


class EvoSystem:
    """Main system integrating all architecture components."""

    def __init__(self, memory: Optional[MemorySystem] = None) -> None:
        """Initialize the evo system with all components.
        
        Args:
            memory: Optional shared MemorySystem instance for dependency injection.
                   If not provided, creates a new instance.
        """
        # Shared memory system (dependency injection)
        self.memory = memory or MemorySystem()
        
        # Core components
        self.perception = PerceptionGateway()
        self.decision = DecisionEngine()
        self.goal = GoalEngine()
        self.capability = CapabilityRegistry()
        self.action = ActionLayer(memory=self.memory, capability_registry=self.capability)
        self.metacognition = MetacognitionLayer()
        self.exploration = ExplorationEngine()
        self.safety = SafetyLayer()
        self.feedback = FeedbackLoop(memory=self.memory)
        self.integrative_core = IntegrativeCore()

        # Handlers
        self.handler = {
            "user_handler": UserHandler(),
            "self_handler": SelfHandler()
        }

    def process_input(self, user_input: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process user input through the system."""
        # Route input through perception
        if user_input:
            routed = self.perception.filter_and_route(user_input)
        else:
            routed = None

        # Combine with self state in integrative core
        self_state = self.integrative_core.self_context
        integrated = self.integrative_core.combine(routed, self_state)

        # Build context for mode selection
        context: Dict[str, Any] = {}
        
        # Check for user input
        if user_input is not None:
            context["user_input"] = True
        
        # Check for internal goals in self context
        if self_state and "active_goals" in self_state and self_state["active_goals"]:
            context["internal_goals"] = True
        
        # Add integrated data
        if integrated:
            context.update(integrated.get("data", {}))

        # Select mode
        mode = self.decision.select_mode(context)
        decision = self.decision.route_decision(mode, integrated["data"] or {})

        return {
            "mode": mode,
            "decision": decision,
            "integrated": integrated
        }


def create_evo_system() -> EvoSystem:
    """Create and return a new evo system instance."""
    return EvoSystem()


def main() -> None:
    """Main entry point for the evo system."""
    print("Starting evo autonomous agent system...")
    
    system = create_evo_system()
    print("evo system initialized successfully!")
    
    print(f"Components loaded: {', '.join([
        'Perception', 'Decision', 'Goal', 'Capability',
        'Action', 'Memory', 'Metacognition', 'Exploration',
        'Safety', 'Feedback', 'Integrative Core'
    ])}")
    
    print("System ready for input processing.")


if __name__ == "__main__":
    main()