"""Configuration management for the evo autonomous agent system.

This module provides centralized configuration management with support for
environment variables and JSON configuration files. All magic numbers and
configuration values are consolidated here to enable easy customization across
different deployment environments.

Configuration Loading Priority:
    1. Environment variables (highest priority)
    2. .env/llm_providers.json JSON configuration
    3. Default values (lowest priority)

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
    
    LLM Configuration:
        - LLM_PROVIDER: LLM provider name (iflow, openrouter)
        - LLM_API_KEY: API key for LLM provider
        - LLM_BASE_URL: Base URL for LLM API
        - LLM_MODEL: Model identifier to use
    
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

from typing import Optional, Dict, Any
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _load_llm_providers_config() -> Dict[str, Any]:
    """Load LLM provider configuration from .env/llm_providers.json.
    
    Returns:
        Dictionary containing LLM provider configuration.
        Returns empty dict if file doesn't exist or is invalid.
    """
    config_path = Path(__file__).parent.parent / ".env" / "llm_providers.json"
    
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


# Load LLM config once at module import
_LLM_CONFIG = _load_llm_providers_config()


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
    
    # LLM Provider Configuration
    # Priority: env var > JSON config > default
    _default_provider = _LLM_CONFIG.get("default_provider", "iflow") if _LLM_CONFIG else "iflow"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", _default_provider)
    
    # Load provider-specific config from JSON
    _provider_config = {}
    if _LLM_CONFIG and "providers" in _LLM_CONFIG and LLM_PROVIDER in _LLM_CONFIG["providers"]:
        _provider_config = _LLM_CONFIG["providers"][LLM_PROVIDER]
    
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY", _provider_config.get("api_key"))
    LLM_BASE_URL: Optional[str] = os.getenv("LLM_BASE_URL", _provider_config.get("base_url"))
    LLM_MODEL: str = os.getenv("LLM_MODEL", _provider_config.get("model", "deepseek-v3"))
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))
    LLM_RETRY_DELAY: float = float(os.getenv("LLM_RETRY_DELAY", "1.0"))
    
    # Legacy OpenAI API (deprecated, use LLM_* instead)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_RETRIES: int = int(os.getenv("OPENAI_MAX_RETRIES", "3"))
    OPENAI_RETRY_DELAY: float = float(os.getenv("OPENAI_RETRY_DELAY", "1.0"))
    
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
