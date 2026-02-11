"""Interactive demo for the evo autonomous agent system."""

from evo.main import create_evo_system
from evo.config import Config
from evo.llm import LLMClientIFlow, LLMClientOpenRouter, ModelsIFlow, ModelsOpenRouter


def main():
    """Interactive demo for the evo system."""
    print("=== Evo Autonomous Agent System - Interactive Demo ===\n")
    
    # Create system instance
    system = create_evo_system()
    print("✓ System initialized\n")
    
    # Display LLM configuration
    print(f"LLM Provider: {Config.LLM_PROVIDER}")
    print(f"LLM Model: {Config.LLM_MODEL}")
    print(f"LLM API Key: {'✓ Set' if Config.LLM_API_KEY else '✗ Not set'}")
    print()
    
    print("Available components:")
    print("  - PerceptionGateway: Routes and filters inputs")
    print("  - DecisionEngine: Selects operating mode")
    print("  - GoalEngine: Manages internal and external goals")
    print("  - CapabilityRegistry: Tracks available tools/capabilities")
    print("  - ActionLayer: Executes actions with LLM-based planning")
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
    
    # Example 6: LLM-based action planning (if API key is set)
    print("\n--- Example 6: LLM-Based Action Planning ---")
    if Config.LLM_API_KEY:
        print("Using LLM for action planning...")
        
        # Register a test tool
        def test_tool():
            return "Tool executed successfully"
        
        system.action.register_tool("test_tool", test_tool, "A simple test tool")
        
        # Plan an action using LLM
        plan = system.action.plan_action({
            "goal": "Demonstrate the test tool functionality",
            "context": {"user": "demo_user"}
        })
        
        print(f"Plan generated: {plan}")
        print("LLM integration: ✓ Working")
    else:
        print("LLM API key not set.")
        print("To enable LLM features:")
        print("  1. Edit .env/llm_providers.json and add your API key")
        print("  2. Or set environment variable: export LLM_API_KEY=your-key")
        print("  3. Then run: uv run python demo.py")
    
    # Example 7: Direct LLM client usage
    print("\n--- Example 7: Direct LLM Client Usage ---")
    if Config.LLM_API_KEY:
        print("Testing direct LLM client connection...")
        
        try:
            if Config.LLM_PROVIDER == "iflow":
                client = LLMClientIFlow(api_key=Config.LLM_API_KEY)
                model = ModelsIFlow.DEEPSEEK_V3
            elif Config.LLM_PROVIDER == "openrouter":
                client = LLMClientOpenRouter(api_key=Config.LLM_API_KEY)
                model = ModelsOpenRouter.DEEPSEEK_R1_0528
            else:
                print(f"Unsupported provider: {Config.LLM_PROVIDER}")
                client = None
                model = None
            
            if client:
                response = client.respond(
                    model,
                    [{"role": "user", "content": "Say hello in one word."}]
                )
                print(f"LLM Response: {response}")
                print("Direct LLM client: ✓ Working")
        except Exception as e:
            print(f"LLM client error: {e}")
            print("Check your API key and network connection")
    else:
        print("Skip: LLM API key not set")
    
    print("\n=== Demo Complete ===")
    print("\nConfiguration:")
    print(f"  Provider: {Config.LLM_PROVIDER}")
    print(f"  Model: {Config.LLM_MODEL}")
    print(f"  API Key: {'✓ Configured' if Config.LLM_API_KEY else '✗ Not configured'}")
    
    print("\nTo run the full system:")
    print("  uv run python main.py")
    print("\nTo run tests:")
    print("  uv run pytest tests/ -v")
    print("\nTo configure LLM:")
    print("  Edit .env/llm_providers.json or set LLM_API_KEY environment variable")


if __name__ == "__main__":
    main()