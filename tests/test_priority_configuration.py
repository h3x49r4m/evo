"""Tests for configurable priority mapping."""

import pytest
import sys
import os
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.perception import PerceptionGateway
from evo.config import Config


def test_default_priority_map():
    """Test that default priority map is correctly configured."""
    gateway = PerceptionGateway()
    
    assert gateway.PRIORITY_MAP["safety"] == 0
    assert gateway.PRIORITY_MAP["user"] == 1
    assert gateway.PRIORITY_MAP["internet"] == 2
    assert gateway.PRIORITY_MAP["environment"] == 3
    assert gateway.PRIORITY_MAP["system"] == 4


def test_config_priority_values():
    """Test that Config has priority configuration values."""
    assert hasattr(Config, "PERCEPTION_PRIORITY_SAFETY")
    assert hasattr(Config, "PERCEPTION_PRIORITY_USER")
    assert hasattr(Config, "PERCEPTION_PRIORITY_INTERNET")
    assert hasattr(Config, "PERCEPTION_PRIORITY_ENVIRONMENT")
    assert hasattr(Config, "PERCEPTION_PRIORITY_SYSTEM")


def test_get_prioritized_inputs_uses_priority_map():
    """Test that get_prioritized_inputs uses the configured priority map."""
    gateway = PerceptionGateway()
    
    # Add inputs in random order
    gateway.add_input({"source": "system", "data": "system_msg"})
    gateway.add_input({"source": "safety", "data": "safety_alert"})
    gateway.add_input({"source": "user", "data": "user_input"})
    gateway.add_input({"source": "environment", "data": "sensor_data"})
    
    prioritized = gateway.get_prioritized_inputs()
    
    # Should be sorted by priority (safety first, system last)
    sources = [inp["source"] for inp in prioritized]
    assert sources.index("safety") < sources.index("user")
    assert sources.index("user") < sources.index("environment")
    assert sources.index("environment") < sources.index("system")


def test_custom_priority_in_input():
    """Test that custom priority in input overrides map priority."""
    gateway = PerceptionGateway()
    
    gateway.add_input({"source": "system", "priority": 0, "data": "urgent_system"})
    gateway.add_input({"source": "safety", "data": "safety_alert"})
    
    prioritized = gateway.get_prioritized_inputs()
    
    # First input should be system with custom priority 0
    assert prioritized[0]["source"] == "system"
    assert prioritized[0]["priority"] == 0


def test_unknown_source_priority():
    """Test that unknown sources get default high priority (999)."""
    gateway = PerceptionGateway()
    
    gateway.add_input({"source": "unknown", "data": "unknown_source"})
    gateway.add_input({"source": "system", "data": "system_msg"})
    
    prioritized = gateway.get_prioritized_inputs()
    
    # Unknown source has priority 999, which is higher (worse) than system's 4
    # So system should come first
    assert prioritized[0]["source"] == "system"
    assert prioritized[1]["source"] == "unknown"


def test_config_values_used_in_priority_map():
    """Test that Config values are used in PRIORITY_MAP."""
    # The PRIORITY_MAP should reference Config values
    assert PerceptionGateway.PRIORITY_MAP["safety"] == Config.PERCEPTION_PRIORITY_SAFETY
    assert PerceptionGateway.PRIORITY_MAP["user"] == Config.PERCEPTION_PRIORITY_USER
    assert PerceptionGateway.PRIORITY_MAP["internet"] == Config.PERCEPTION_PRIORITY_INTERNET
    assert PerceptionGateway.PRIORITY_MAP["environment"] == Config.PERCEPTION_PRIORITY_ENVIRONMENT
    assert PerceptionGateway.PRIORITY_MAP["system"] == Config.PERCEPTION_PRIORITY_SYSTEM


def test_priority_map_is_dict():
    """Test that PRIORITY_MAP is a dictionary."""
    assert isinstance(PerceptionGateway.PRIORITY_MAP, dict)


def test_priority_map_has_all_sources():
    """Test that PRIORITY_MAP contains all expected sources."""
    expected_sources = ["safety", "user", "internet", "environment", "system"]
    for source in expected_sources:
        assert source in PerceptionGateway.PRIORITY_MAP


def test_prioritization_with_equal_priorities():
    """Test that inputs with equal priorities maintain order."""
    gateway = PerceptionGateway()
    
    gateway.add_input({"source": "user", "data": "first"})
    gateway.add_input({"source": "user", "data": "second"})
    
    prioritized = gateway.get_prioritized_inputs()
    
    # Both have same priority, order should be preserved
    assert prioritized[0]["data"] == "first"
    assert prioritized[1]["data"] == "second"


def test_empty_queue_prioritization():
    """Test prioritization with empty queue."""
    gateway = PerceptionGateway()
    
    prioritized = gateway.get_prioritized_inputs()
    
    assert prioritized == []


def test_filter_and_route_with_priority_map():
    """Test that filter_and_route works with configured priority map."""
    gateway = PerceptionGateway()
    
    input_data = {"source": "user", "content": "test"}
    routed = gateway.filter_and_route(input_data)
    
    assert routed is not None
    assert routed["context"] == "user"
    assert routed["data"]["source"] == "user"


def test_config_get_all_returns_all_configuration_values():
    """Given Config class, When calling get_all, Then returns dictionary with all config values (line 102)."""
    config_dict = Config.get_all()
    
    assert isinstance(config_dict, dict)
    assert "action_retry_delay" in config_dict
    assert "action_max_retries" in config_dict
    assert "capability_default_level" in config_dict
    assert "safety_time_limit" in config_dict
    assert "safety_storage_limit" in config_dict
    assert "safety_iteration_limit" in config_dict
    assert "memory_use_chromadb" in config_dict
    assert "openai_model" in config_dict
    assert "log_level" in config_dict
    
    # Verify values match Config class attributes
    assert config_dict["action_retry_delay"] == Config.ACTION_RETRY_DELAY
    assert config_dict["action_max_retries"] == Config.ACTION_MAX_RETRIES
    assert config_dict["capability_default_level"] == Config.CAPABILITY_DEFAULT_LEVEL