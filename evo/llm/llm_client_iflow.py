"""iFlow LLM client integration."""

from enum import Enum
from typing import Optional
from evo.llm.base import LLMClientBase


class LLMClientIFlow(LLMClientBase):
    """iFlow API LLM client.
    
    Ref: https://platform.iflow.cn/models
    """

    def __init__(self, api_key: str, base_url: str = 'https://apis.iflow.cn/v1') -> None:
        """Initialize the iFlow LLM client.
        
        Args:
            api_key: iFlow API key.
            base_url: Base URL for iFlow API (default: https://apis.iflow.cn/v1).
        """
        super().__init__(api_key, base_url)


class ModelsIFlow(str, Enum):
    """Available models on iFlow platform.
    
    Ref: https://platform.iflow.cn/models
    """

    # iFlow
    IFLOW_ROME = 'iflow-rome-30ba3b'

    # GLM
    GLM_46 = 'glm-4.6'

    # Kimi
    KIMI_K2 = 'kimi-k2'
    KIMI_K2_0905 = 'kimi-k2-0905'

    # Qwen
    QWEN3_32B = 'qwen3-32b'
    QWEN3_235B = 'qwen3-235b'
    QWEN3_235B_A22B_INSTRUCT = 'qwen3-235b-a22b-instruct'
    QWEN3_235B_A22B_THINKING_2507 = 'qwen3-235b-a22b-thinking-2507'
    QWEN3_MAX = 'qwen3-max'
    QWEN3_MAX_PREVIEW = 'qwen3-max-preview'
    QWEN3_VL_PLUS = 'qwen3-vl-plus'
    QWEN3_CODER_PLUS = 'qwen3-coder-plus'

    # DeepSeek
    DEEPSEEK_V3 = 'deepseek-v3'
    DEEPSEKK_V32 = 'deepseek-v3.2'
    DEEPSEEK_R1 = 'deepseek-r1'