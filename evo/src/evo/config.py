"""Configuration management for the evo autonomous agent system.

This module provides centralized configuration management with support for
environment variables. All magic numbers and configuration values are
consolidated here to enable easy customization across different deployment
environments.

Configuration Categories:
    - Action Layer: Retry delays, max retries, LLM settings
    - Capability Registry: Default skill levels, validation bounds
    - Safety Layer: Time, storage, and iteration limits
    - Perception Gateway: Priority levels for different input sources

Environment Variables:
    Set environment variables to override default configuration values:
    
    Action Configuration:
        - ACTION_RETRY_DELAY: Delay between retry attempts (default: 0.1)
        - ACTION_MAX_RETRIES: Maximum retry attempts (default: 3)
    
    Capability Configuration:
        - CAPABILITY_DEFAULT_LEVEL: Default skill level (default: 0.5)
    
    Safety Configuration:
        - SAFETY_TIME_LIMIT: Maximum execution time in seconds (default: 3600)
        - SAFETY_STORAGE_LIMIT: Maximum storage in bytes (default: 107374182400)
        - SAFETY_ITERATION_LIMIT: Maximum iterations (default: 1000)
    
    LLM Configuration:
        - OPENAI_API_KEY: OpenAI API key (default: None)
        - OPENAI_MODEL: Model name (default: gpt-3.5-turbo)
        - OPENAI_TEMPERATURE: Sampling temperature (default: 0.7)
    
    Perception Configuration:
        - PERCEPTION_PRIORITY_SAFETY: Safety input priority (default: 0)
        - PERCEPTION_PRIORITY_USER: User input priority (default: 1)
        - PERCEPTION_PRIORITY_INTERNET: Internet input priority (default: 2)
        - PERCEPTION_PRIORITY_ENVIRONMENT: Environment input priority (default: 3)
        - PERCEPTION_PRIORITY_SYSTEM: System input priority (default: 4)

Example:
    >>> from evo.config import Config
    >>>
    >>> # Access configuration values
    >>> print(f"Max retries: {Config.ACTION_MAX_RETRIES}")
    >>> print(f"Default skill level: {Config.CAPABILITY_DEFAULT_LEVEL}")
    >>>
    >>> # Set environment variable before import to override
    >>> import os
    >>> os.environ["ACTION_MAX_RETRIES"] = "5"
    >>> # Note: Must be set before the module is imported
"""

from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration settings for the evo system."""
    
    # Action Layer
    ACTION_RETRY_DELAY: float = float(os.getenv("ACTION_RETRY_DELAY", "0.1"))
    ACTION_MAX_RETRIES: int = int(os.getenv("ACTION_MAX_RETRIES", "1"))
    
    # Capability Registry
    CAPABILITY_DEFAULT_LEVEL: float = float(os.getenv("CAPABILITY_DEFAULT_LEVEL", "0.5"))
    CAPABILITY_MIN_LEVEL: float = 0.0
    CAPABILITY_MAX_LEVEL: float = 1.0
    
    # Safety Layer
    SAFETY_TIME_LIMIT: int = int(os.getenv("SAFETY_TIME_LIMIT", "3600"))  # 1 hour
    SAFETY_STORAGE_LIMIT: int = int(os.getenv("SAFETY_STORAGE_LIMIT", "107374182400"))  # 100GB
    SAFETY_ITERATION_LIMIT: int = int(os.getenv("SAFETY_ITERATION_LIMIT", "1000"))
    
    # Perception Gateway
    PERCEPTION_PRIORITY_SAFETY: int = int(os.getenv("PERCEPTION_PRIORITY_SAFETY", "0"))
    PERCEPTION_PRIORITY_USER: int = int(os.getenv("PERCEPTION_PRIORITY_USER", "1"))
    PERCEPTION_PRIORITY_INTERNET: int = int(os.getenv("PERCEPTION_PRIORITY_INTERNET", "2"))
    PERCEPTION_PRIORITY_ENVIRONMENT: int = int(os.getenv("PERCEPTION_PRIORITY_ENVIRONMENT", "3"))
    PERCEPTION_PRIORITY_SYSTEM: int = int(os.getenv("PERCEPTION_PRIORITY_SYSTEM", "4"))
    
    # Memory System
    MEMORY_USE_CHROMADB: bool = os.getenv("MEMORY_USE_CHROMADB", "true").lower() == "true"
    MEMORY_COLLECTION_NAME: str = os.getenv("MEMORY_COLLECTION_NAME", "episodes")
    
    # OpenAI API
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    @classmethod
    def get_all(cls) -> dict:
        """Get all configuration values as a dictionary."""
        return {
            "action_retry_delay": cls.ACTION_RETRY_DELAY,
            "action_max_retries": cls.ACTION_MAX_RETRIES,
            "capability_default_level": cls.CAPABILITY_DEFAULT_LEVEL,
            "safety_time_limit": cls.SAFETY_TIME_LIMIT,
            "safety_storage_limit": cls.SAFETY_STORAGE_LIMIT,
            "safety_iteration_limit": cls.SAFETY_ITERATION_LIMIT,
            "memory_use_chromadb": cls.MEMORY_USE_CHROMADB,
            "openai_model": cls.OPENAI_MODEL,
            "log_level": cls.LOG_LEVEL,
        }


# Default configuration instance
config = Config()
