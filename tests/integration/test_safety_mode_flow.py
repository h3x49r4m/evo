"""Integration tests for Safety Mode Flow."""

import pytest

from evo.main import EvoSystem, create_evo_system


class TestSafetyModeFlow:
    """Integration tests for safety mode workflow triggered by safety alerts."""

    def test_safety_mode_triggered_by_alert(self):
        """Test safety mode is triggered when safety alert is present."""
        system = create_evo_system()
        
        # Context with safety alert
        context = {"safety_alert": True}
        
        # Select mode
        mode = system.decision.select_mode(context)
        
        # Verify safety mode selected
        assert mode == "safety"

    def test_safety_mode_decision_routing(self):
        """Test decision engine routes to safety handler in safety mode."""
        system = create_evo_system()
        
        # Safety alert context
        context = {"safety_alert": True, "alert_type": "resource_limit"}
        
        # Select and route
        mode = system.decision.select_mode(context)
        decision = system.decision.route_decision(mode, context)
        
        # Verify routing to safety handler
        assert mode == "safety"
        assert decision["handler"] == "safety_handler"

    def test_safety_mode_no_self_destruction(self):
        """Test safety mode blocks self-destruction actions."""
        system = create_evo_system()
        
        # Test various self-destruction actions
        self_destruct_actions = [
            "remove_all_capabilities",
            "terminate_self",
            "delete_core_system"
        ]
        
        for action in self_destruct_actions:
            result = system.safety.check_action_safety(action)
            assert result["allowed"] is False
            assert result["reason"] == "self_destruction"

    def test_safety_mode_no_harmful_actions(self):
        """Test safety mode blocks harmful actions."""
        system = create_evo_system()
        
        # Test various harmful actions
        harmful_actions = [
            "delete_system_files",
            "malicious_code",
            "damage_environment",
            "harm_users",
            "exploit_vulnerabilities"
        ]
        
        for action in harmful_actions:
            result = system.safety.check_action_safety(action)
            assert result["allowed"] is False
            assert result["reason"] == "harmful_action"

    def test_safety_mode_prevents_infinite_loops(self):
        """Test safety mode prevents infinite loops."""
        system = create_evo_system()
        
        # Test loop iteration limits
        safe_iterations = 500
        unsafe_iterations = 1500
        
        safe_result = system.safety.check_loop_safety(safe_iterations)
        unsafe_result = system.safety.check_loop_safety(unsafe_iterations)
        
        # Verify enforcement
        assert safe_result["allowed"] is True
        assert unsafe_result["allowed"] is False
        assert unsafe_result["reason"] == "iteration_limit"

    def test_safety_mode_enforces_time_limits(self):
        """Test safety mode enforces time limits on operations."""
        system = create_evo_system()
        
        # Test time limit enforcement
        safe_time = 1800  # 30 minutes
        unsafe_time = 7200  # 2 hours
        
        safe_result = system.safety.check_time_limit(safe_time)
        unsafe_result = system.safety.check_time_limit(unsafe_time)
        
        # Verify enforcement
        assert safe_result["allowed"] is True
        assert unsafe_result["allowed"] is False
        assert unsafe_result["reason"] == "time_limit"

    def test_safety_mode_enforces_storage_limits(self):
        """Test safety mode enforces storage limits."""
        system = create_evo_system()
        
        # Test storage limit enforcement (50GB limit = ~53687091200 bytes for testing)
        safe_usage = 10  # 10GB
        unsafe_usage = 150  # 150GB
        
        safe_result = system.safety.check_storage_limit(safe_usage)
        unsafe_result = system.safety.check_storage_limit(unsafe_usage)
        
        # Verify enforcement
        assert safe_result["allowed"] is True
        assert unsafe_result["allowed"] is False
        assert unsafe_result["reason"] == "storage_limit"

    def test_safety_mode_user_override_pause(self):
        """Test user can pause the system via override mechanism."""
        system = create_evo_system()
        
        # User issues pause command
        result = system.safety.handle_user_override("pause")
        
        # Verify system paused
        assert result["action"] == "paused"
        assert system.safety.is_paused() is True

    def test_safety_mode_user_override_resume(self):
        """Test user can resume the system via override mechanism."""
        system = create_evo_system()
        
        # First pause
        system.safety.handle_user_override("pause")
        
        # Then resume
        result = system.safety.handle_user_override("resume")
        
        # Verify system resumed
        assert result["action"] == "resumed"
        assert system.safety.is_paused() is False

    def test_safety_mode_user_override_block_action(self):
        """Test user can block specific actions via override mechanism."""
        system = create_evo_system()
        
        # User blocks an action
        result = system.safety.handle_user_override("block", "test_action_id")
        
        # Verify action blocked
        assert result["action"] == "blocked"
        assert result["action_id"] == "test_action_id"
        assert system.safety.is_action_blocked("test_action_id") is True

    def test_safety_mode_user_override_unblock_action(self):
        """Test user can unblock specific actions via override mechanism."""
        system = create_evo_system()
        
        # First block
        system.safety.handle_user_override("block", "test_action_id")
        
        # Then unblock
        result = system.safety.handle_user_override("unblock", "test_action_id")
        
        # Verify action unblocked
        assert result["action"] == "unblocked"
        assert system.safety.is_action_blocked("test_action_id") is False

    def test_safety_mode_time_tracking(self):
        """Test safety mode tracks time usage for operations."""
        system = create_evo_system()
        
        # Start tracking
        operation_id = "test_operation"
        import time
        system.safety.start_tracking(operation_id)
        time.sleep(0.01)
        
        # Stop tracking
        elapsed = system.safety.stop_tracking(operation_id)
        
        # Verify time tracked
        assert elapsed > 0
        assert system.safety.get_time_usage(operation_id) == elapsed

    def test_safety_mode_storage_tracking(self):
        """Test safety mode tracks storage usage."""
        system = create_evo_system()
        
        # Record storage usage
        system.safety.record_storage_usage(1024)  # 1KB
        system.safety.record_storage_usage(2048)  # 2KB
        
        # Verify tracking
        usage = system.safety.get_storage_usage()
        assert usage == 3072  # 3KB
        
        # Reset and verify
        system.safety.reset_storage_usage()
        assert system.safety.get_storage_usage() == 0

    def test_safety_mode_allows_safe_actions(self):
        """Test safety mode allows safe actions to proceed."""
        system = create_evo_system()
        
        # Test safe actions
        safe_actions = [
            "read_file",
            "write_file",
            "search",
            "analyze"
        ]
        
        for action in safe_actions:
            result = system.safety.check_action_safety(action)
            # Should either be allowed or have different reason
            # (not self_destruction or harmful_action)

    def test_safety_mode_with_user_input(self):
        """Test safety mode processes user input when safety alert is active."""
        system = create_evo_system()
        
        # Safety alert is active
        context = {"safety_alert": True}
        
        # User input comes in during safety mode
        user_input = {"source": "user", "data": "What's happening?"}
        
        # Process
        result = system.process_input(user_input)
        
        # Verify safety mode still takes precedence
        mode = system.decision.select_mode(context)
        assert mode == "safety"

    def test_safety_mode_memory_of_violations(self):
        """Test safety mode records violations in memory."""
        system = create_evo_system()
        
        # Attempt harmful action (blocked)
        action = "delete_system_files"
        result = system.safety.check_action_safety(action)
        
        # Record in working memory
        system.memory.working.store("last_violation", {
            "action": action,
            "reason": result["reason"],
            "timestamp": "now"
        })
        
        # Verify violation recorded
        violation = system.memory.working.retrieve("last_violation")
        assert violation is not None
        assert violation["action"] == action
        assert violation["reason"] == "harmful_action"