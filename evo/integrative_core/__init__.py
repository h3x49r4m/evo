"""Integrative Core - Combines user input and self state for unified processing."""

from typing import Any, Dict, Optional
from evo.types import ContextData


class IntegrativeCore:
    """Combines user input and self state for unified processing."""

    def __init__(self) -> None:
        """Initialize IntegrativeCore with empty contexts."""
        self.user_context: Dict[str, Any] = {}
        self.self_context: Dict[str, Any] = {}

    def combine(
        self,
        user_input: Optional[Dict[str, Any]],
        self_state: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Combine user input and self state into unified context."""
        if user_input and self_state:
            return {
                "source": "hybrid",
                "data": {
                    "user": user_input,
                    "self": self_state
                }
            }
        if user_input:
            return {
                "source": "user",
                "data": user_input
            }
        if self_state:
            return {
                "source": "self",
                "data": self_state
            }
        return {
            "source": "empty",
            "data": {}
        }

    def update_user_context(self, key: str, value: str) -> None:
        """Update user context with key-value pair."""
        self.user_context[key] = value

    def update_self_context(self, key: str, value: ContextData) -> None:
        """Update self context with key-value pair."""
        self.self_context[key] = value

    def get_integrated_context(self) -> Dict[str, Any]:
        """Get the integrated context combining user and self."""
        return {
            "user": self.user_context,
            "self": self.self_context
        }