"""OpenRouter LLM client integration."""

from enum import Enum
from typing import Optional
from evo.llm.base import LLMClientBase


class LLMClientOpenRouter(LLMClientBase):
    """OpenRouter API LLM client.
    
    Ref: https://openrouter.ai/
    """

    def __init__(self, api_key: str, base_url: str = 'https://openrouter.ai/api/v1') -> None:
        """Initialize the OpenRouter LLM client.
        
        Args:
            api_key: OpenRouter API key.
            base_url: Base URL for OpenRouter API (default: https://openrouter.ai/api/v1).
        """
        super().__init__(api_key, base_url)


class ModelsOpenRouter(str, Enum):
    """Available models on OpenRouter platform."""

    # DeepSeek
    DEEPSEEK_R1_0528 = 'deepseek/deepseek-r1-0528:free'

    # OpenAI
    OPENAI_GPT_OSS_120B = 'openai/gpt-oss-120b:free'

    # Qwen
    QWEN3_CODER = 'qwen/qwen3-coder:free'

    # Pony
    PONY_ALPHA = 'openrouter/pony-alpha'