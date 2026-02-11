"""Tests for covering edge cases in safety layer."""

import pytest
from evo.safety import SafetyLayer


class TestSafetyLayerEdgeCases:
    """Tests for covering remaining uncovered lines in safety layer."""

    def test_handle_user_override_unknown_command(self):
        """Test unknown command returns unknown action (line 130)."""
        safety = SafetyLayer()
        result = safety.handle_user_override("unknown_command")
        assert result["action"] == "unknown"
        assert result["command"] == "unknown_command"

    def test_handle_user_override_unblock_without_block(self):
        """Test unblock command on non-blocked action (line 109)."""
        safety = SafetyLayer()
        # Unblock an action that was never blocked
        result = safety.handle_user_override("unblock", "never_blocked")
        assert result["action"] == "unblocked"
        assert result["action_id"] == "never_blocked"
