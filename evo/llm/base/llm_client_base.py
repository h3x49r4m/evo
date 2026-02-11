"""Base LLM client class for OpenAI-compatible APIs."""

import httpx
from typing import List, Dict, Any, Optional
from openai import OpenAI


class LLMClientBase:
    """Base LLM client for OpenAI-compatible APIs.
    
    This class provides a unified interface for interacting with various
    LLM providers that implement the OpenAI API specification.
    """

    def __init__(self, api_key: str, base_url: str) -> None:
        """Initialize the LLM client.
        
        Args:
            api_key: API key for the LLM provider.
            base_url: Base URL for the LLM API.
        """
        http_client = httpx.Client(
            timeout=httpx.Timeout(60.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            http_client=http_client,
            max_retries=2
        )

    def warmup(self) -> None:
        """Warm up the client by listing available models."""
        try:
            self.client.models.list()
        except Exception:
            pass

    def respond(
        self,
        model: str,
        messages: List[Dict[str, str]],
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """Get a response from the LLM.
        
        Args:
            model: Model identifier to use.
            messages: List of message dictionaries with 'role' and 'content'.
            response_format: Optional response format specification.
            
        Returns:
            The LLM response content as a string.
        """
        try:
            if response_format:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    response_format=response_format
                )
            else:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"ERROR: LLM responded failed (msg: {e}).")
            return ''

    def respond_streaming(
        self,
        model: str,
        messages: List[Dict[str, str]],
        response_format: Optional[Dict[str, str]] = None,
        debug: bool = False
    ) -> str:
        """Get a streaming response from the LLM.
        
        Args:
            model: Model identifier to use.
            messages: List of message dictionaries with 'role' and 'content'.
            response_format: Optional response format specification.
            debug: Whether to print debug information.
            
        Returns:
            The complete LLM response content as a string.
        """
        try:
            import time
            results = ''
            start = time.time()
            first_token_time = None
            token_count = 0

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    if first_token_time is None:
                        first_token_time = time.time()
                    token_count += 1
                    print(content, end="", flush=True)
                    results += content

            end = time.time()
            if debug:
                time_to_first_token = (first_token_time - start) if first_token_time else 0
                total_time = end - start
                print(f"\n\n[DEBUG] Time to first token: {time_to_first_token:.2f}s, "
                      f"Token count: {token_count}, Total time: {total_time:.2f}s")
            return results

        except Exception as e:
            print(f"ERROR: LLM responded failed (msg: {e}).")
            exit(-1)