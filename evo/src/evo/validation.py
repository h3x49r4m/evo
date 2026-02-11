"""Input validation utilities for the evo system."""

from evo.config import Config
from evo.logging import get_logger

logger = get_logger("evo.validation")


def validate_skill_level(level: float) -> bool:
    """Validate skill level is within bounds."""
    if not isinstance(level, (int, float)):
        logger.error(f"Skill level must be a number, got {type(level)}")
        return False
    if not Config.CAPABILITY_MIN_LEVEL <= level <= Config.CAPABILITY_MAX_LEVEL:
        logger.error(f"Skill level {level} must be between {Config.CAPABILITY_MIN_LEVEL} and {Config.CAPABILITY_MAX_LEVEL}")
        return False
    return True


def validate_name(name: str, entity_type: str) -> bool:
    """Validate a name is not empty or None."""
    if name is None:
        logger.error(f"{entity_type} name cannot be None")
        return False
    if not isinstance(name, str):
        logger.error(f"{entity_type} name must be a string, got {type(name)}")
        return False
    if not name.strip():
        logger.error(f"{entity_type} name cannot be empty")
        return False
    return True


def validate_tool_name(name: str) -> bool:
    """Validate tool name is a valid identifier."""
    if not validate_name(name, "Tool"):
        return False
    # Check for valid identifier characters
    if not name.replace("_", "").isalnum():
        logger.error(f"Tool name '{name}' contains invalid characters")
        return False
    return True


def validate_goal_name(name: str) -> bool:
    """Validate goal name is valid."""
    return validate_name(name, "Goal")
