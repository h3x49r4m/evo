"""LLM client integration for the evo autonomous agent system.

This module provides integrated LLM clients for various providers (iFlow, OpenRouter)
that can be used within the evo system instead of external API calls.

Available Clients:
    - LLMClientIFlow: iFlow API client
    - LLMClientOpenRouter: OpenRouter API client

Usage:
    >>> from evo.llm import LLMClientIFlow, ModelsIFlow
    >>> client = LLMClientIFlow(api_key="your-key")
    >>> response = client.respond(ModelsIFlow.DEEPSEEK_V3, [{"role": "user", "content": "Hello"}])
"""

from .llm_client_iflow import LLMClientIFlow, ModelsIFlow
from .llm_client_openrouter import LLMClientOpenRouter, ModelsOpenRouter

__all__ = [
    "LLMClientIFlow",
    "ModelsIFlow",
    "LLMClientOpenRouter",
    "ModelsOpenRouter",
]