"""Decision Engine - Mode selector and decision routing with logging."""

from typing import Any, Dict
from evo.logging import get_logger

logger = get_logger("evo.decision")


class DecisionEngine:
    """Mode selector and decision routing."""
    
    def __init__(self) -> None:
        pass
    
    # Mode selection
    def select_mode(self, context: Dict[str, Any]) -> str:
        """Select operational mode based on context."""
        if context.get("safety_alert"):
            mode = "safety"
            logger.warning(f"Safety mode selected: {context.get('alert_type', 'unknown')}")
        elif context.get("user_input") and context.get("internal_goals"):
            mode = "hybrid"
            logger.info("Hybrid mode selected: both user input and internal goals present")
        elif context.get("user_input"):
            mode = "responsive"
            logger.info("Responsive mode selected: user input present")
        else:
            mode = "autonomous"
            logger.info("Autonomous mode selected: no user input")
        
        return mode
    
    # Decision routing
    def route_decision(self, mode: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Route decision to appropriate handler."""
        handler_map = {
            "responsive": "user_handler",
            "autonomous": "self_handler",
            "hybrid": "hybrid_handler",
            "safety": "safety_handler"
        }
        
        handler = handler_map.get(mode, "unknown_handler")
        logger.debug(f"Routing to {handler} in {mode} mode")
        
        return {
            "handler": handler,
            "mode": mode,
            "data": data
        }
    
    # Decision execution
    def execute_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a decision and return result."""
        if not decision.get("data"):
            logger.error("Decision execution failed: no data provided")
            return {"error": "No data provided", "mode": decision.get("mode")}
        
        logger.debug(f"Executing decision in {decision.get('mode')} mode")
        return {
            "result": "executed",
            "mode": decision.get("mode"),
            "data": decision.get("data")
        }
