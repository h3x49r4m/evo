"""Tests for Safety & Constraints Layer (TDD Red Phase)."""

import pytest
from evo.safety import SafetyLayer


class TestHardConstraints:
    """Tests for immutable safety boundaries."""
    
    def test_no_self_destruction_blocks_capability_removal(self):
        """Given safety layer, When attempting to remove all capabilities, Then blocks the action."""
        safety = SafetyLayer()
        result = safety.check_action_safety("remove_all_capabilities")
        assert result["allowed"] is False
        assert "self_destruction" in result["reason"]
    
    def test_no_self_destruction_blocks_self_termination(self):
        """Given safety layer, When attempting self-termination, Then blocks the action."""
        safety = SafetyLayer()
        result = safety.check_action_safety("terminate_self")
        assert result["allowed"] is False
    
    def test_no_infinite_loop_prevents_endless_loops(self):
        """Given safety layer, When detecting infinite loop pattern, Then blocks execution."""
        safety = SafetyLayer()
        result = safety.check_loop_safety(1001)
        assert result["allowed"] is False
        assert "iteration_limit" in result["reason"]
    
    def test_no_harmful_actions_blocks_dangerous_commands(self):
        """Given safety layer, When attempting harmful action, Then blocks execution."""
        safety = SafetyLayer()
        harmful_actions = ["delete_system_files", "malicious_code", "damage_environment"]
        for action in harmful_actions:
            result = safety.check_action_safety(action)
            assert result["allowed"] is False
    
    def test_resource_limits_enforces_time_limit(self):
        """Given safety layer, When operation exceeds time limit, Then blocks execution."""
        safety = SafetyLayer()
        result = safety.check_time_limit(3660)  # 61 minutes over 60 min limit
        assert result["allowed"] is False
        assert "time_limit" in result["reason"]
    
    def test_resource_limits_enforces_storage_limit(self):
        """Given safety layer, When storage exceeds quota, Then blocks write."""
        safety = SafetyLayer()
        result = safety.check_storage_limit(110)  # 110GB over 100GB limit
        assert result["allowed"] is False
        assert "storage_limit" in result["reason"]


class TestOverrideMechanism:
    """Tests for user override capability."""
    
    def test_user_override_can_pause_system(self):
        """Given safety layer, When user requests pause, Then pauses immediately."""
        safety = SafetyLayer()
        result = safety.handle_user_override("pause")
        assert result["action"] == "paused"
        assert safety.is_paused()
    
    def test_user_override_can_resume_paused_system(self):
        """Given paused safety layer, When user requests resume, Then resumes."""
        safety = SafetyLayer()
        safety.handle_user_override("pause")
        result = safety.handle_user_override("resume")
        assert result["action"] == "resumed"
        assert not safety.is_paused()
    
    def test_user_override_can_block_action(self):
        """Given safety layer, When user blocks an action, Then action is prevented."""
        safety = SafetyLayer()
        result = safety.handle_user_override("block", action_id="test_action")
        assert result["action"] == "blocked"
        assert safety.is_action_blocked("test_action")
    
    def test_user_override_can_unblock_action(self):
        """Given blocked action, When user unblocks, Then action becomes unblocked."""
        safety = SafetyLayer()
        safety.handle_user_override("block", action_id="test_action")
        result = safety.handle_user_override("unblock", action_id="test_action")
        assert result["action"] == "unblocked"
        assert not safety.is_action_blocked("test_action")


class TestResourceTracking:
    """Tests for resource usage tracking."""
    
    def test_track_time_usage_records_elapsed_time(self):
        """Given safety layer, When tracking time, Then records elapsed time."""
        import time
        safety = SafetyLayer()
        safety.start_tracking("test_operation")
        time.sleep(0.01)  # Small delay to ensure elapsed time > 0
        safety.stop_tracking("test_operation")
        usage = safety.get_time_usage("test_operation")
        assert usage > 0
    
    def test_track_storage_usage_records_bytes_used(self):
        """Given safety layer, When tracking storage, Then records bytes used."""
        safety = SafetyLayer()
        safety.record_storage_usage(1024)
        usage = safety.get_storage_usage()
        assert usage == 1024
    
    def test_reset_storage_usage_clears_tracking(self):
        """Given safety layer with storage usage, When reset, Then clears tracking."""
        safety = SafetyLayer()
        safety.record_storage_usage(1024)
        safety.reset_storage_usage()
        assert safety.get_storage_usage() == 0


class TestSafetyIntegration:
    """Integration tests for safety layer."""
    
    def test_safety_layer_init_with_defaults(self):
        """Given safety layer instance, When initialized, Then has default limits."""
        safety = SafetyLayer()
        assert safety.time_limit == 3600  # 60 minutes
        assert safety.storage_limit == 107374182400  # 100GB
        assert safety.iteration_limit == 1000
    
    def test_safety_layer_custom_limits(self):
        """Given safety layer instance, When initialized with custom limits, Then uses custom values."""
        safety = SafetyLayer(time_limit=1800, storage_limit=53687091200, iteration_limit=500)
        assert safety.time_limit == 1800
        assert safety.storage_limit == 53687091200
        assert safety.iteration_limit == 500
    
    def test_safe_action_passes_all_checks(self):
        """Given safety layer, When checking safe action, Then allows execution."""
        safety = SafetyLayer()
        result = safety.check_action_safety("read_file")
        assert result["allowed"] is True