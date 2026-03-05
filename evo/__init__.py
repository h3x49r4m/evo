"""Self-Evolving AI System."""

__version__ = "0.1.0"


# Custom Exceptions
class EvoException(Exception):
    """Base exception for all Evo system errors."""
    pass


class LLMConnectionError(EvoException):
    """Raised when LLM API connection fails."""
    pass


class LLMResponseError(EvoException):
    """Raised when LLM response is invalid or parsing fails."""
    pass


class LLMStreamingError(EvoException):
    """Raised when LLM streaming response fails."""
    pass


class ToolNotFoundError(EvoException):
    """Raised when a requested tool is not found in the registry."""
    pass


class ConfigurationError(EvoException):
    """Raised when configuration is invalid or missing."""
    pass


class DependencyError(EvoException):
    """Raised when an optional dependency is required but not available."""
    pass