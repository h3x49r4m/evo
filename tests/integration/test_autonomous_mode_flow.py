"""Integration tests for Autonomous Mode Flow."""

import pytest

from evo.main import EvoSystem, create_evo_system


class TestAutonomousModeFlow:
    """Integration tests for autonomous mode workflow when no user input is present."""

    def test_autonomous_mode_no_user_input_flow(self):
        """Test complete autonomous mode flow with no user input."""
        system = create_evo_system()
        
        # No user input (autonomous mode)
        result = system.process_input(None)
        
        # Verify autonomous mode is selected
        assert result["mode"] == "autonomous"
        assert result["decision"]["handler"] == "self_handler"

    def test_autonomous_mode_internal_goal_generation(self):
        """Test internal goal generation from drives."""
        system = create_evo_system()
        
        # Generate goals from all drives
        curiosity_goal = system.goal.generate_curiosity_goal()
        competence_goal = system.goal.generate_competence_goal()
        autonomy_goal = system.goal.generate_autonomy_goal()
        meaning_goal = system.goal.generate_meaning_goal()
        
        # Verify all drives generate goals
        assert curiosity_goal["drive"] == "curiosity"
        assert competence_goal["drive"] == "competence"
        assert autonomy_goal["drive"] == "autonomy"
        assert meaning_goal["drive"] == "meaning"

    def test_autonomous_mode_self_handler_execution(self):
        """Test self handler execution in autonomous mode."""
        system = create_evo_system()
        
        handler = system.handler["self_handler"]
        
        # Generate internal goal
        goal = handler.generate_internal_goal()
        
        # Explore purposes
        purposes = handler.explore_purposes()
        
        # Verify handler generated goals and purposes
        assert "goal" in goal
        assert "drive" in goal
        assert len(purposes) > 0

    def test_autonomous_mode_goal_evaluation(self):
        """Test goal evaluation in autonomous mode."""
        system = create_evo_system()
        
        # Evaluate a goal
        goal = {"name": "explore", "description": "Explore new areas"}
        evaluation = system.goal.evaluate_goal(goal)
        
        # Verify evaluation metrics
        assert "feasibility" in evaluation
        assert "learning_potential" in evaluation
        assert "drive_alignment" in evaluation
        assert 0.0 <= evaluation["feasibility"] <= 1.0

    def test_autonomous_mode_exploration_engine(self):
        """Test exploration engine in autonomous mode."""
        system = create_evo_system()
        
        # Register capabilities
        system.exploration.register_capability("tool_a", used=False)
        system.exploration.register_capability("tool_b", used=True)
        
        # Detect novelty (unused capabilities)
        novelty = system.exploration.detect_novelty()
        
        # Verify unused capability detected
        assert "tool_a" in novelty
        assert "tool_b" not in novelty

    def test_autonomous_mode_random_exploration(self):
        """Test random exploration in autonomous mode."""
        system = create_evo_system()
        
        # Generate random exploration goal
        exploration = system.exploration.random_exploration()
        
        # Verify exploration goal generated
        assert "goal" in exploration
        assert "type" in exploration
        assert exploration["type"] == "random"

    def test_autonomous_mode_purpose_synthesis(self):
        """Test purpose synthesis in autonomous mode."""
        system = create_evo_system()
        
        # Synthesize purpose from reflections
        reflections = {"learned": "I can help users", "drive": "autonomy"}
        purpose = system.exploration.synthesize_purpose(reflections)
        
        # Verify purpose synthesized
        assert "purpose" in purpose
        assert "statement" in purpose

    def test_autonomous_mode_metacognition_loop(self):
        """Test metacognition loop in autonomous mode."""
        system = create_evo_system()
        
        # Trigger reflection
        reflection = system.metacognition.trigger_reflection("periodic", {"data": "test"})
        
        # Update self-model
        system.metacognition.update_capabilities("planning", 0.8)
        system.metacognition.update_beliefs("self_awareness", "high")
        
        # Learn from experience
        system.metacognition.learn_from_experience({"outcome": "success", "strategy": "plan_first"})
        
        # Verify metacognition processed
        assert reflection["type"] == "reflection"
        assert system.metacognition.get_self_model()["capabilities"]["planning"] == 0.8
        assert len(system.metacognition.get_learned_strategies()) > 0

    def test_autonomous_mode_memory_integration(self):
        """Test memory integration in autonomous mode."""
        system = create_evo_system()
        
        # Store internal state in working memory
        system.memory.working.store("current_goal", "explore_capabilities")
        system.memory.working.store("active_drive", "curiosity")
        
        # Store experience in episodic memory
        import asyncio
        experience = {"action": "explore", "result": "discovered_new_capability"}
        
        async def test_episodic():
            exp_id = await system.memory.episodic.store_experience(experience)
            similar = await system.memory.episodic.retrieve_similar("explore", k=5)
            return exp_id, similar
        
        exp_id, similar = asyncio.run(test_episodic())
        
        # Verify memory storage
        assert exp_id is not None
        assert system.memory.working.retrieve("current_goal") == "explore_capabilities"
        assert len(similar) > 0

    def test_autonomous_mode_with_capability_discovery(self):
        """Test autonomous mode discovering new capabilities."""
        system = create_evo_system()
        
        # System explores and discovers new tool
        def new_capability():
            return "I can do something new!"
        
        system.capability.register_tool("new_tool", "A newly discovered tool", new_capability)
        
        # Register in exploration engine as used
        system.exploration.register_capability("new_tool", used=True)
        
        # Verify capability discovery
        assert "new_tool" in system.capability.list_tools()
        assert system.capability.get_capability_count() > 0