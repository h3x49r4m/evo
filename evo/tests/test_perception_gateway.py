"""Tests for Perception Gateway (TDD Red Phase)."""

import pytest
from evo.perception import PerceptionGateway


class TestInputFiltering:
    """Tests for filtering and prioritizing inputs."""
    
    def test_filter_user_input_returns_user_context(self):
        """Given perception gateway, When filtering user input, Then routes to user context."""
        gateway = PerceptionGateway()
        input_data = {"source": "user", "content": "Hello, world!"}
        result = gateway.filter_and_route(input_data)
        assert result["context"] == "user"
        assert result["data"]["content"] == "Hello, world!"
    
    def test_filter_environment_input_returns_sensor_context(self):
        """Given perception gateway, When filtering environment input, Then routes to sensor context."""
        gateway = PerceptionGateway()
        input_data = {"source": "environment", "sensor": "temperature", "value": 25}
        result = gateway.filter_and_route(input_data)
        assert result["context"] == "sensor"
        assert result["data"]["sensor"] == "temperature"
    
    def test_filter_internet_input_returns_network_context(self):
        """Given perception gateway, When filtering internet input, Then routes to network context."""
        gateway = PerceptionGateway()
        input_data = {"source": "internet", "url": "https://example.com", "content": "data"}
        result = gateway.filter_and_route(input_data)
        assert result["context"] == "network"
        assert result["data"]["url"] == "https://example.com"
    
    def test_filter_unknown_source_returns_system_context(self):
        """Given perception gateway, When filtering unknown source, Then routes to system context."""
        gateway = PerceptionGateway()
        input_data = {"source": "unknown", "data": "something"}
        result = gateway.filter_and_route(input_data)
        assert result["context"] == "system"
    
    def test_filter_empty_input_returns_none(self):
        """Given perception gateway, When filtering empty input, Then returns None."""
        gateway = PerceptionGateway()
        result = gateway.filter_and_route({})
        assert result is None


class TestInputPrioritization:
    """Tests for prioritizing incoming inputs."""
    
    def test_prioritize_user_input_highest_priority(self):
        """Given perception gateway, When prioritizing user input, Then gives higher priority than environment."""
        gateway = PerceptionGateway()
        gateway.add_input({"source": "user", "content": "urgent"})
        gateway.add_input({"source": "environment", "data": "info"})
        prioritized = gateway.get_prioritized_inputs()
        # User (priority 1) should come before environment (priority 3)
        assert prioritized[0]["source"] == "user"
        assert prioritized[1]["source"] == "environment"
    
    def test_prioritize_safety_input_above_environment(self):
        """Given perception gateway, When prioritizing safety input, Then prioritizes above environment."""
        gateway = PerceptionGateway()
        gateway.add_input({"source": "safety", "alert": "critical"})
        gateway.add_input({"source": "environment", "data": "info"})
        prioritized = gateway.get_prioritized_inputs()
        assert prioritized[0]["source"] == "safety"
    
    def test_prioritize_by_explicit_priority(self):
        """Given perception gateway, When inputs have explicit priority, Then sorts by priority."""
        gateway = PerceptionGateway()
        gateway.add_input({"source": "task1", "priority": 2})
        gateway.add_input({"source": "task2", "priority": 1})
        gateway.add_input({"source": "task3", "priority": 3})
        prioritized = gateway.get_prioritized_inputs()
        assert prioritized[0]["priority"] == 1
        assert prioritized[1]["priority"] == 2
        assert prioritized[2]["priority"] == 3


class TestInputQueue:
    """Tests for managing input queue."""
    
    def test_add_input_adds_to_queue(self):
        """Given perception gateway, When adding input, Then adds to queue."""
        gateway = PerceptionGateway()
        gateway.add_input({"source": "user", "content": "test"})
        assert gateway.queue_size() == 1
    
    def test_add_multiple_inputs_increases_queue_size(self):
        """Given perception gateway, When adding multiple inputs, Then queue size increases."""
        gateway = PerceptionGateway()
        for i in range(5):
            gateway.add_input({"source": f"source_{i}", "data": i})
        assert gateway.queue_size() == 5
    
    def test_get_next_input_removes_from_queue(self):
        """Given perception gateway with inputs, When getting next, Then removes from queue."""
        gateway = PerceptionGateway()
        gateway.add_input({"source": "user", "content": "test"})
        next_input = gateway.get_next_input()
        assert gateway.queue_size() == 0
        assert next_input is not None
    
    def test_get_next_input_on_empty_queue_returns_none(self):
        """Given empty perception gateway, When getting next input, Then returns None."""
        gateway = PerceptionGateway()
        next_input = gateway.get_next_input()
        assert next_input is None


class TestPerceptionIntegration:
    """Integration tests for perception gateway."""
    
    def test_perception_gateway_init_creates_empty_queue(self):
        """Given perception gateway instance, When initialized, Then has empty queue."""
        gateway = PerceptionGateway()
        assert gateway.queue_size() == 0
    
    def test_full_workflow_filter_prioritize_and_route(self):
        """Given perception gateway, When processing input through full workflow, Then correctly processes."""
        gateway = PerceptionGateway()
        # Add inputs
        gateway.add_input({"source": "user", "content": "Help me"})
        gateway.add_input({"source": "environment", "sensor": "temp", "value": 20})
        gateway.add_input({"source": "safety", "alert": "timeout"})
        # Get prioritized
        prioritized = gateway.get_prioritized_inputs()
        # Process each
        processed = []
        for input_data in prioritized:
            result = gateway.filter_and_route(input_data)
            if result:
                processed.append(result)
        # Verify safety was processed first, then user
        assert len(processed) == 3
        assert processed[0]["context"] == "safety"
        assert processed[1]["context"] == "user"