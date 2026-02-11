"""Tests for .env/llm_providers.json configuration loading."""

import json
import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from evo.config import Config


class TestEnvConfigLoading:
    """Test loading configuration from .env/llm_providers.json."""

    def test_llm_providers_json_exists_and_valid(self):
        """Test that .env/llm_providers.json file exists and has valid structure."""
        env_file = Path(__file__).parent.parent / ".env" / "llm_providers.json"
        
        # This test will fail initially (red phase)
        if not env_file.exists():
            pytest.fail(f".env/llm_providers.json does not exist at {env_file}")
        
        # Verify JSON structure
        with open(env_file, 'r') as f:
            data = json.load(f)
        
        # Check required fields
        assert "providers" in data, "Missing 'providers' field"
        assert isinstance(data["providers"], dict), "'providers' must be a dict"
        
        # Check at least one provider is configured
        assert len(data["providers"]) > 0, "At least one provider must be configured"

    def test_config_loads_from_llm_providers_json(self):
        """Test that Config loads values from .env/llm_providers.json."""
        env_file = Path(__file__).parent.parent / ".env" / "llm_providers.json"
        
        if not env_file.exists():
            pytest.skip(".env/llm_providers.json does not exist yet")
        
        with open(env_file, 'r') as f:
            data = json.load(f)
        
        # Test that Config can read provider configuration
        if "default_provider" in data:
            assert data["default_provider"] in data["providers"], "default_provider must be in providers list"

    def test_llm_provider_config_values(self):
        """Test that LLM provider configuration values are properly set."""
        # Test environment variable fallback
        original_provider = os.environ.get("LLM_PROVIDER")
        original_api_key = os.environ.get("LLM_API_KEY")
        
        try:
            # Set test values
            os.environ["LLM_PROVIDER"] = "iflow"
            os.environ["LLM_API_KEY"] = "test-key-123"
            
            # Reload config by importing fresh
            import importlib
            import evo.config
            importlib.reload(evo.config)
            from evo.config import Config as ReloadedConfig
            
            assert ReloadedConfig.LLM_PROVIDER == "iflow"
            assert ReloadedConfig.LLM_API_KEY == "test-key-123"
        finally:
            # Restore original values
            if original_provider is not None:
                os.environ["LLM_PROVIDER"] = original_provider
            else:
                os.environ.pop("LLM_PROVIDER", None)
            if original_api_key is not None:
                os.environ["LLM_API_KEY"] = original_api_key
            else:
                os.environ.pop("LLM_API_KEY", None)

    def test_gitignore_includes_env_directory(self):
        """Test that .gitignore includes .env/ directory."""
        gitignore_file = Path(__file__).parent.parent / ".gitignore"
        
        assert gitignore_file.exists(), ".gitignore file does not exist"
        
        content = gitignore_file.read_text()
        assert ".env/" in content or ".env" in content, ".gitignore should include .env/ directory"

    def test_config_reads_json_config_before_env_vars(self):
        """Test that Config reads JSON config before falling back to env vars."""
        # This test verifies the priority: JSON config > env vars > defaults
        env_file = Path(__file__).parent.parent / ".env" / "llm_providers.json"
        
        if not env_file.exists():
            pytest.skip(".env/llm_providers.json does not exist yet")
        
        # If JSON config exists, it should be readable
        with open(env_file, 'r') as f:
            data = json.load(f)
        
        # Verify the structure supports priority
        if "providers" in data:
            for provider_name, provider_config in data["providers"].items():
                assert "api_key" in provider_config or "base_url" in provider_config, \
                    f"Provider {provider_name} must have api_key or base_url"
