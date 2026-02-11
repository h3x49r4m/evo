"""Integration tests for Responsive Mode Flow."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import EvoSystem, create_evo_system


class TestResponsiveModeFlow:
    """Integration tests for responsive mode workflow when user is present."""

    def test_responsive_mode_user_input_flow(self):
        """Test complete responsive mode flow with user input."""
        system = create_evo_system()
        
        # Simulate user input
        user_input = {
            "source": "user",
            "data": "Hello, can you help me?"
        }
        
        # Process through the system
        result = system.process_input(user_input)
        
        # Verify responsive mode is selected
        assert result["mode"] == "responsive"
        assert result["decision"]["handler"] == "user_handler"
        
        # Verify integrative core combined user context
        assert result["integrated"]["source"] == "user"
        assert "data" in result["integrated"]

    def test_responsive_mode_perception_to_decision(self):
        """Test flow from perception gateway to decision engine."""
        system = create_evo_system()
        
        # User input enters through perception
        user_input = {"source": "user", "data": "test input"}
        routed = system.perception.filter_and_route(user_input)
        
        # Verify perception routing
        assert routed is not None
        assert routed["context"] == "user"
        
        # Verify decision engine selects responsive mode
        context = routed
        mode = system.decision.select_mode({"user_input": True})
        assert mode == "responsive"

    def test_responsive_mode_goal_override(self):
        """Test that external goals override internal goals in responsive mode."""
        system = create_evo_system()
        
        # Add internal goal
        system.goal.add_internal_goal("explore", "Explore capabilities")
        
        # Add external goal (should override)
        system.goal.add_external_goal("assist_user", "Help the user")
        
        # Prioritize goals
        prioritized = system.goal.prioritize_goals()
        
        # External goal should come first
        assert prioritized[0]["source"] == "external"
        assert prioritized[0]["name"] == "assist_user"

    def test_responsive_mode_user_handler_execution(self):
        """Test user handler execution in responsive mode."""
        system = create_evo_system()
        
        handler = system.handler["user_handler"]
        
        # Parse user intent
        intent = handler.parse_intent("What can you do?")
        
        # Execute request
        response = handler.execute_request(intent)
        
        # Verify handler processed the request
        assert "response" in response
        assert "Processed" in response["response"]

    def test_responsive_mode_with_capability_usage(self):
        """Test responsive mode using capability registry."""
        system = create_evo_system()
        
        # Register a capability
        def search_tool(query: str) -> str:
            return f"Results for: {query}"
        
        system.capability.register_tool("search", "Search capability", search_tool)
        
        # User requests to use the capability
        user_input = {"source": "user", "data": "search for something"}
        result = system.process_input(user_input)
        
        # Verify capability is available
        tool = system.capability.get_tool("search")
        assert tool is not None
        assert tool["description"] == "Search capability"

    def test_responsive_mode_safety_checks(self):
        """Test that safety checks are applied in responsive mode."""
        system = create_evo_system()
        
        # Attempt harmful action (should be blocked)
        harmful_action = {"action": "delete_system_files"}
        safety_result = system.safety.check_action_safety(harmful_action["action"])
        
        # Verify safety blocks harmful actions
        assert safety_result["allowed"] is False
        assert safety_result["reason"] == "harmful_action"

    def test_responsive_mode_feedback_loop(self):
        """Test feedback loop integration in responsive mode."""
        system = create_evo_system()
        
        # Simulate action and observation
        observation = {
            "action": "user_request",
            "result": "success",
            "output": "Response sent to user"
        }
        
        # Process observation
        processed = system.feedback.process_observation(observation)
        
        # Store in memory
        system.feedback.store_observation(processed)
        
        # Verify memory storage
        assert system.feedback.get_working_memory_size() > 0

    def test_responsive_mode_with_memory_context(self):
        """Test responsive mode maintains conversation context in memory."""
        system = create_evo_system()
        
        # Store conversation history
        system.memory.working.store("conversation", ["Hello", "Hi there"])
        
        # Process new user input
        user_input = {"source": "user", "data": "How are you?"}
        result = system.process_input(user_input)
        
        # Verify memory context is preserved
        conversation = system.memory.working.retrieve("conversation")
        assert len(conversation) == 2