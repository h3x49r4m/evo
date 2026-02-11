"""Configuration module for the evo system."""

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
    PERCEPTION_PRIORITY_SAFETY: int = 0
    PERCEPTION_PRIORITY_USER: int = 1
    PERCEPTION_PRIORITY_INTERNET: int = 2
    PERCEPTION_PRIORITY_ENVIRONMENT: int = 3
    PERCEPTION_PRIORITY_SYSTEM: int = 4
    
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
