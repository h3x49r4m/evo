"""Logging configuration for the evo system."""

import logging
import sys
from typing import Optional
from evo.config import Config

# Create logger
logger = logging.getLogger("evo")
logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

# Create formatter
formatter = logging.Formatter(
    fmt=Config.LOG_FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific component.
    
    Args:
        name: Name of the component (e.g., "evo.perception")
        
    Returns:
        Logger instance for the component.
    """
    return logging.getLogger(name)
