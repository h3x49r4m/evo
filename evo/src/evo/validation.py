"""Input validation utilities for the evo autonomous agent system.

This module provides validation functions for common input types throughout
the system. These functions help ensure data integrity and catch invalid
inputs early in the processing pipeline.

Validation Categories:
    - Skill/Capability Levels: Validates that skill levels are within valid bounds (0.0-1.0)
    - Names: Validates that entity names are non-empty and valid identifiers
    - Tool Names: Validates that tool names follow Python identifier rules

Usage Pattern:
    Import validation functions and use them before accepting user input
    or storing data. Raise ValueError with descriptive messages for invalid inputs.

Example:
    >>> from evo.validation import validate_skill_level, validate_name
    >>>
    >>> # Validate a skill level
    >>> level = 0.75
    >>> if not validate_skill_level(level):
    ...     raise ValueError(f"Invalid skill level: {level}")
    >>>
    >>> # Validate a name
    >>> name = "search_web"
    >>> if not validate_name(name, "Skill"):
    ...     raise ValueError(f"Invalid skill name: {name}")

Common Patterns:
    1. Validate during registration (e.g., register_tool, register_skill)
    2. Validate before storing in memory
    3. Validate after parsing user input
    4. Validate configuration values

Error Handling:
    All validation functions return boolean values. It's up to the caller
    to raise appropriate exceptions with meaningful error messages.
"""

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
