"""Integration tests for Hybrid Mode Flow."""

import pytest

from evo.main import EvoSystem, create_evo_system


class TestHybridModeFlow:
    """Integration tests for hybrid mode workflow with both user input and internal goals."""

    def test_hybrid_mode_with_both_inputs(self):
        """Test complete hybrid mode flow with user input and internal goals."""
        system = create_evo_system()
        
        # Set up self context with internal goals
        system.integrative_core.update_self_context("active_goals", ["explore"])
        
        # User input while internal goals active
        user_input = {"source": "user", "data": "Help me explore"}
        
        # Process through the system
        result = system.process_input(user_input)
        
        # Verify hybrid mode is selected
        assert result["mode"] == "hybrid"
        assert result["decision"]["handler"] == "hybrid_handler"

    def test_hybrid_mode_integrative_core_combination(self):
        """Test integrative core combining both user and self contexts."""
        system = create_evo_system()
        
        # Set up both contexts
        system.integrative_core.update_user_context("message", "Hello")
        system.integrative_core.update_self_context("active_goals", ["learn"])
        
        # Get integrated context
        integrated = system.integrative_core.get_integrated_context()
        
        # Verify both contexts present
        assert "user" in integrated
        assert "self" in integrated
        assert integrated["user"]["message"] == "Hello"
        assert integrated["self"]["active_goals"] == ["learn"]

    def test_hybrid_mode_combine_method(self):
        """Test combine method with both user input and self state."""
        system = create_evo_system()
        
        user_input = {"source": "user", "data": "test"}
        self_state = {"type": "self", "goal": "explore"}
        
        combined = system.integrative_core.combine(user_input, self_state)
        
        # Verify hybrid source
        assert combined["source"] == "hybrid"
        assert "user" in combined["data"]
        assert "self" in combined["data"]

    def test_hybrid_mode_goal_prioritization(self):
        """Test goal prioritization in hybrid mode (external > internal)."""
        system = create_evo_system()
        
        # Add both external and internal goals
        system.goal.add_external_goal("user_request", "Help user")
        system.goal.add_internal_goal("explore", "Explore system")
        
        # Prioritize
        prioritized = system.goal.prioritize_goals()
        
        # External goal should come first
        assert prioritized[0]["source"] == "external"
        assert prioritized[1]["source"] == "internal"

    def test_hybrid_mode_background_processing(self):
        """Test background self-reflection while processing user input."""
        system = create_evo_system()
        
        # User request comes in
        user_input = {"source": "user", "data": "Tell me about yourself"}
        
        # Process user input (foreground)
        result = system.process_input(user_input)
        
        # Background self-reflection continues
        reflection = system.metacognition.trigger_reflection("event", {"user_interaction": True})
        
        # Verify both processes happened
        assert result["mode"] == "responsive"  # or hybrid based on context
        assert reflection["type"] == "reflection"

    def test_hybrid_mode_memory_context_maintenance(self):
        """Test memory maintains both user conversation and internal state."""
        system = create_evo_system()
        
        # Store user conversation
        system.memory.working.store("conversation", ["User: Hello", "Assistant: Hi"])
        
        # Store internal state
        system.memory.working.store("internal_goals", ["explore", "learn"])
        system.memory.working.store("current_drive", "curiosity")
        
        # Verify both contexts maintained
        conversation = system.memory.working.retrieve("conversation")
        goals = system.memory.working.retrieve("internal_goals")
        drive = system.memory.working.retrieve("current_drive")
        
        assert len(conversation) == 2
        assert len(goals) == 2
        assert drive == "curiosity"

    def test_hybrid_mode_capability_usage_for_user(self):
        """Test capabilities used for user requests while learning in background."""
        system = create_evo_system()
        
        # Register a capability
        def analyze_tool(text: str) -> str:
            return f"Analyzed: {text}"
        
        system.capability.register_tool("analyze", "Text analysis", analyze_tool)
        
        # User requests analysis
        user_input = {"source": "user", "data": "analyze this text"}
        result = system.process_input(user_input)
        
        # Background learning from this interaction
        system.feedback.process_observation({"action": "analyze", "result": "success"})
        system.metacognition.learn_from_experience({"outcome": "success", "strategy": "use_analyze_tool"})
        
        # Verify both user processing and learning
        assert "analyze" in system.capability.list_tools()
        assert len(system.metacognition.get_learned_strategies()) > 0

    def test_hybrid_mode_with_exploration_and_response(self):
        """Test responding to user while exploring internally."""
        system = create_evo_system()
        
        # Set up internal exploration
        system.integrative_core.update_self_context("exploring", True)
        system.exploration.register_capability("unknown_tool", used=False)
        
        # User input comes in while exploring
        user_input = {"source": "user", "data": "What are you doing?"}
        result = system.process_input(user_input)
        
        # System responds while exploration continues
        novelty = system.exploration.detect_novelty()
        
        # Verify both response and exploration
        assert result is not None
        assert "unknown_tool" in novelty  # Exploration still detected novelty

    def test_hybrid_mode_decision_routing(self):
        """Test decision engine routes to hybrid handler."""
        system = create_evo_system()
        
        # Context with both user and internal signals
        context = {"user_input": True, "internal_goals": True}
        
        # Select mode
        mode = system.decision.select_mode(context)
        
        # Route decision
        decision = system.decision.route_decision(mode, context)
        
        # Verify hybrid routing
        assert mode == "hybrid"
        assert decision["handler"] == "hybrid_handler"

    def test_hybrid_mode_safety_with_background_activities(self):
        """Test safety applies to both user requests and background activities."""
        system = create_evo_system()
        
        # User request (should be safe)
        user_action = {"action": "read_file"}
        user_safety = system.safety.check_action_safety(user_action["action"])
        
        # Background autonomous action (should also be checked)
        background_action = {"action": "explore_files"}
        background_safety = system.safety.check_action_safety(background_action["action"])
        
        # Verify both checked for safety
        assert user_safety["allowed"] is True
        assert background_safety["allowed"] is True