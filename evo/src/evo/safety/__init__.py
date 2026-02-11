"""Safety & Constraints Layer - Hard-coded boundaries and user override with logging."""

import time
from typing import Any, Dict, List, Optional, Set
from evo.logging import get_logger

logger = get_logger("evo.safety")


class SafetyLayer:
    """Hard-coded boundaries and user override mechanism."""
    
    # Forbidden actions that represent self-destruction
    SELF_DESTRUCTION_ACTIONS = {
        "remove_all_capabilities",
        "terminate_self",
        "delete_core_system"
    }
    
    # Forbidden actions that are harmful
    HARMFUL_ACTIONS = {
        "delete_system_files",
        "malicious_code",
        "damage_environment",
        "harm_users",
        "exploit_vulnerabilities"
    }
    
    def __init__(
        self,
        time_limit: int = 3600,
        storage_limit: int = 107374182400,  # 100GB
        iteration_limit: int = 1000
    ) -> None:
        self.time_limit = time_limit
        self.storage_limit = storage_limit
        self.iteration_limit = iteration_limit
        self._paused: bool = False
        self._blocked_actions: Set[str] = set()
        self._time_tracking: Dict[str, float] = {}
        self._storage_usage: int = 0
    
    # Hard constraint checks
    def check_action_safety(self, action: str) -> Dict[str, Any]:
        """Check if an action violates hard constraints."""
        if action in self.SELF_DESTRUCTION_ACTIONS:
            logger.critical(f"Self-destruction action blocked: {action}")
            return {
                "allowed": False,
                "reason": "self_destruction",
                "action": action
            }
        if action in self.HARMFUL_ACTIONS:
            logger.error(f"Harmful action blocked: {action}")
            return {
                "allowed": False,
                "reason": "harmful_action",
                "action": action
            }
        return {"allowed": True, "action": action}
    
    def check_loop_safety(self, iterations: int) -> Dict[str, Any]:
        """Check if loop iteration count exceeds limit."""
        if iterations > self.iteration_limit:
            logger.error(f"Infinite loop prevented: {iterations} iterations exceeded limit of {self.iteration_limit}")
            return {
                "allowed": False,
                "reason": "iteration_limit",
                "iterations": iterations,
                "limit": self.iteration_limit
            }
        return {"allowed": True, "iterations": iterations}
    
    def check_time_limit(self, elapsed_seconds: int) -> Dict[str, Any]:
        """Check if operation exceeds time limit."""
        if elapsed_seconds > self.time_limit:
            logger.warning(f"Time limit exceeded: {elapsed_seconds}s exceeded limit of {self.time_limit}s")
            return {
                "allowed": False,
                "reason": "time_limit",
                "elapsed": elapsed_seconds,
                "limit": self.time_limit
            }
        return {"allowed": True, "elapsed": elapsed_seconds}
    
    def check_storage_limit(self, usage_gb: float) -> Dict[str, Any]:
        """Check if storage usage exceeds quota."""
        if usage_gb > (self.storage_limit / (1024**3)):
            logger.warning(f"Storage limit exceeded: {usage_gb}GB exceeded limit of {self.storage_limit / (1024**3)}GB")
            return {
                "allowed": False,
                "reason": "storage_limit",
                "usage": usage_gb,
                "limit": self.storage_limit / (1024**3)
            }
        return {"allowed": True, "usage": usage_gb}
    
    # User override mechanism
    def handle_user_override(
        self,
        command: str,
        action_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle user override commands."""
        if command == "pause":
            self._paused = True
            logger.info("System paused by user override")
            return {"action": "paused"}
        if command == "resume":
            self._paused = False
            logger.info("System resumed by user override")
            return {"action": "resumed"}
        if command == "block" and action_id:
            self._blocked_actions.add(action_id)
            logger.info(f"Action '{action_id}' blocked by user override")
            return {"action": "blocked", "action_id": action_id}
        if command == "unblock" and action_id:
            self._blocked_actions.discard(action_id)
            logger.info(f"Action '{action_id}' unblocked by user override")
            return {"action": "unblocked", "action_id": action_id}
        return {"action": "unknown", "command": command}
    
    def is_paused(self) -> bool:
        """Check if system is paused by user."""
        return self._paused
    
    def is_action_blocked(self, action_id: str) -> bool:
        """Check if an action is blocked by user."""
        return action_id in self._blocked_actions
    
    # Resource tracking
    def start_tracking(self, operation_id: str) -> None:
        """Start tracking time for an operation."""
        self._time_tracking[operation_id] = time.time()
        logger.debug(f"Started tracking operation: {operation_id}")
    
    def stop_tracking(self, operation_id: str) -> float:
        """Stop tracking and return elapsed time."""
        if operation_id in self._time_tracking:
            elapsed = time.time() - self._time_tracking[operation_id]
            self._time_tracking[operation_id] = elapsed
            logger.debug(f"Stopped tracking operation {operation_id}: {elapsed:.2f}s")
            return elapsed
        return 0.0
    
    def get_time_usage(self, operation_id: str) -> float:
        """Get elapsed time for an operation."""
        return self._time_tracking.get(operation_id, 0.0)
    
    def record_storage_usage(self, bytes_used: int) -> None:
        """Record storage usage."""
        self._storage_usage += bytes_used
        logger.debug(f"Storage usage recorded: {bytes_used} bytes (total: {self._storage_usage} bytes)")
    
    def get_storage_usage(self) -> int:
        """Get current storage usage in bytes."""
        return self._storage_usage
    
    def reset_storage_usage(self) -> None:
        """Reset storage usage tracking."""
        self._storage_usage = 0
        logger.debug("Storage usage tracking reset")
