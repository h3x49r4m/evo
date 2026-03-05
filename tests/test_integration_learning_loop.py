"""Integration tests for the complete learning loop."""

import pytest
from evo.main import EvoSystem


class TestLearningLoopIntegration:
    """Integration tests for the complete learning loop."""

    @pytest.fixture
    def system(self):
        """Create a fresh EvoSystem instance for each test."""
        return EvoSystem()

    def test_system_integrates_all_components(self, system):
        """Test that all components are properly integrated."""
        # Verify all components exist
        assert system.memory is not None
        assert system.perception is not None
        assert system.decision is not None
        assert system.goal is not None
        assert system.capability is not None
        assert system.action is not None
        assert system.metacognition is not None
        assert system.exploration is not None
        assert system.safety is not None
        assert system.feedback is not None
        assert system.integrative_core is not None

    def test_autonomous_mode_generates_internal_goals(self, system):
        """Test that autonomous mode generates internal goals from drives."""
        # Generate autonomous goals
        goals = system.goal.generate_autonomous_goals()
        
        assert len(goals) > 0, "Should generate autonomous goals"
        assert any("drive" in goal for goal in goals), "Goals should have drive information"

    def test_self_handler_generates_goals_from_drives(self, system):
        """Test that SelfHandler generates goals from intrinsic drives."""
        # Execute self handler
        goals = system.handler["self_handler"].execute()
        
        assert goals is not None, "Should generate goals"
        assert "drive" in goals, "Should specify drive"

    def test_metacognition_updates_from_experiences(self, system):
        """Test that metacognition updates self-model from experiences."""
        # Create some experiences
        experiences = [
            {"action": "test", "outcome": "success", "confidence": 0.8}
        ]
        
        # Trigger reflection
        result = system.metacognition.auto_reflection(experiences)
        
        assert result is not None, "Should return reflection result"
        assert "insights" in result, "Should generate insights"

    def test_feedback_loop_generates_learnings(self, system):
        """Test that feedback loop generates learnings from observations."""
        # Process observations
        for i in range(3):
            system.feedback.process_observation({
                "action": "test_action",
                "result": "success"
            })
        
        # Get learnings
        learnings = system.feedback.get_learnings()
        
        assert learnings is not None, "Should generate learnings"
        assert "patterns" in learnings, "Should detect patterns"
        assert "success_rates" in learnings, "Should track success rates"

    def test_exploration_engine_discovers_capabilities(self, system):
        """Test that exploration engine can discover capabilities."""
        # Register some capabilities
        system.exploration.register_capability("known_tool", used=True)
        system.exploration.register_capability("unknown_tool", used=False)
        
        # Explore
        result = system.exploration.explore()
        
        assert result is not None, "Should explore"
        assert "actions" in result, "Should generate actions"

    def test_continuous_loop_integrates_all_components(self, system):
        """Test that continuous loop integrates all components."""
        iteration_count = 0
        
        def mock_process_input(user_input):
            nonlocal iteration_count
            iteration_count += 1
            
            # Simulate autonomous behavior
            if iteration_count == 1:
                # Generate autonomous goals
                goals = system.goal.generate_autonomous_goals()
                system.feedback.process_observation({
                    "action": goals[0]["actions"][0],
                    "result": "success"
                })
            elif iteration_count == 2:
                # Trigger reflection
                experiences = [{"action": "test", "outcome": "success"}]
                system.metacognition.auto_reflection(experiences)
            
            return {"mode": "autonomous", "decision": {"handler": "self_handler"}}
        
        # Patch process_input to simulate behavior
        system.process_input = mock_process_input
        
        # Run for 2 iterations
        system.run(duration=None, iterations=2)
        
        # Verify components were used
        assert iteration_count == 2, "Should complete 2 iterations"

    def test_learning_loop_generates_insights(self, system):
        """Test that the learning loop generates insights from experiences."""
        # Process multiple observations
        for i in range(5):
            system.feedback.process_observation({
                "action": "learning_action",
                "result": "success" if i % 2 == 0 else "failure"
            })
        
        # Get learnings
        learnings = system.feedback.get_learnings()
        
        # Should have patterns and recommendations
        assert len(learnings["patterns"]) > 0 or len(learnings["recommendations"]) > 0, \
            "Should generate patterns or recommendations"

    def test_goal_engine_balances_intrinsic_drives(self, system):
        """Test that goal engine balances across intrinsic drives."""
        # Generate multiple autonomous goals
        all_drives = set()
        for _ in range(10):
            goals = system.goal.generate_autonomous_goals()
            for goal in goals:
                if "drive" in goal:
                    all_drives.add(goal["drive"])
        
        # Should use multiple drives
        assert len(all_drives) >= 2, "Should balance across multiple drives"

    def test_system_memory_tracks_experiences(self, system):
        """Test that system memory tracks experiences across components."""
        # Store in working memory
        system.memory.working.store("test_key", "test_value")
        
        # Retrieve from working memory
        retrieved = system.memory.working.retrieve("test_key")
        
        assert retrieved == "test_value", "Should store and retrieve from memory"

    def test_decision_engine_routes_based_on_context(self, system):
        """Test that decision engine routes based on integrated context."""
        # Test responsive mode
        context = {"user_input": True}
        mode = system.decision.select_mode(context)
        assert mode == "responsive", "Should select responsive mode with user input"
        
        # Test autonomous mode
        context = {"user_input": False, "internal_goals": True}
        mode = system.decision.select_mode(context)
        assert mode == "autonomous", "Should select autonomous mode without user input"