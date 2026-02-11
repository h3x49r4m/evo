"""Interactive demo for the evo autonomous agent system."""

from evo.main import create_evo_system


def main():
    """Interactive demo for the evo system."""
    print("=== Evo Autonomous Agent System - Interactive Demo ===\n")
    
    # Create system instance
    system = create_evo_system()
    print("✓ System initialized\n")
    
    print("Available components:")
    print("  - PerceptionGateway: Routes and filters inputs")
    print("  - DecisionEngine: Selects operating mode")
    print("  - GoalEngine: Manages internal and external goals")
    print("  - CapabilityRegistry: Tracks available tools/capabilities")
    print("  - ActionLayer: Executes actions with safety checks")
    print("  - MemorySystem: Three-tier memory (working, short-term, long-term)")
    print("  - MetacognitionLayer: Self-awareness and reflection")
    print("  - ExplorationEngine: Novelty detection and purpose synthesis")
    print("  - SafetyLayer: Enforces safety constraints")
    print("  - FeedbackLoop: Learning from outcomes")
    print("  - IntegrativeCore: Combines user and self contexts\n")
    
    print("Operating modes:")
    print("  - responsive: Processes user input")
    print("  - autonomous: Acts based on internal goals")
    print("  - hybrid: Combines user input and internal goals")
    print("  - safety: Emergency mode with maximum safety\n")
    
    print("Example usage:")
    print("  system.process_input({\"text\": \"Hello, evo!\"})")
    print("  system.process_input(None)  # Autonomous mode\n")
    
    # Example 1: User input
    print("\n--- Example 1: User Input ---")
    result = system.process_input({"text": "Hello, evo!"})
    print(f"Mode: {result['mode']}")
    print(f"Decision: {result['decision']}")
    
    # Example 2: Autonomous mode
    print("\n--- Example 2: Autonomous Mode ---")
    result = system.process_input(None)
    print(f"Mode: {result['mode']}")
    print(f"Decision: {result['decision']}")
    
    # Example 3: Goal management
    print("\n--- Example 3: Goal Management ---")
    system.goal.add_external_goal("demo_goal", "Test goal for demo")
    goals = system.goal.list_external_goals()
    print(f"External goals: {goals}")
    
    # Example 4: Memory
    print("\n--- Example 4: Memory System ---")
    system.memory.working.store("demo_key", "demo_value")
    retrieved = system.memory.working.retrieve("demo_key")
    print(f"Stored and retrieved: {retrieved}")
    
    # Example 5: Safety check
    print("\n--- Example 5: Safety Check ---")
    harmful_action = {"action": "delete_system_files"}
    safety_result = system.safety.check_action_safety(harmful_action["action"])
    print(f"Harmful action blocked: {not safety_result['allowed']}")
    print(f"Reason: {safety_result['reason']}")
    
    print("\n=== Demo Complete ===")
    print("\nTo run the full system:")
    print("  uv run python main.py")
    print("\nTo run tests:")
    print("  uv run pytest tests/ -v")


if __name__ == "__main__":
    main()