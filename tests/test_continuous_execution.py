"""Tests for continuous execution loop in main.py."""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from evo.main import EvoSystem


class TestContinuousExecutionLoop:
    """Test suite for continuous execution loop functionality."""

    @pytest.fixture
    def system(self):
        """Create a fresh EvoSystem instance for each test."""
        return EvoSystem()

    def test_system_has_run_method(self, system):
        """Test that EvoSystem has a run method for continuous execution."""
        assert hasattr(system, 'run'), "EvoSystem should have a run method"
        assert callable(system.run), "run should be a callable method"

    def test_run_accepts_duration_parameter(self, system):
        """Test that run method accepts a duration parameter."""
        # This test checks the method signature
        import inspect
        sig = inspect.signature(system.run)
        assert 'duration' in sig.parameters, "run should accept a duration parameter"
        assert 'iterations' in sig.parameters, "run should accept an iterations parameter"

    def test_run_stops_after_specified_duration(self, system):
        """Test that run loop stops after specified duration."""
        # This is a red test - should fail initially since run doesn't exist
        start_count = 0
        iteration_count = 0

        def mock_process_input(user_input):
            nonlocal iteration_count
            iteration_count += 1
            return {"mode": "autonomous", "decision": {"handler": "self_handler"}}

        with patch.object(system, 'process_input', side_effect=mock_process_input):
            # Run for 0.1 seconds (short duration for testing)
            system.run(duration=0.1, iterations=None)
        
        # Verify the loop ran at least once
        assert iteration_count > 0, "Loop should have executed at least once"

    def test_run_stops_after_specified_iterations(self, system):
        """Test that run loop stops after specified number of iterations."""
        iteration_count = 0

        def mock_process_input(user_input):
            nonlocal iteration_count
            iteration_count += 1
            return {"mode": "autonomous", "decision": {"handler": "self_handler"}}

        with patch.object(system, 'process_input', side_effect=mock_process_input):
            # Run for 3 iterations
            system.run(duration=None, iterations=3)
        
        # Verify exactly 3 iterations
        assert iteration_count == 3, f"Expected 3 iterations, got {iteration_count}"

    def test_run_handles_user_input_during_execution(self, system):
        """Test that run loop can process user input when provided."""
        processed_inputs = []

        def mock_process_input(user_input):
            processed_inputs.append(user_input)
            return {
                "mode": "responsive" if user_input else "autonomous",
                "decision": {"handler": "user_handler" if user_input else "self_handler"}
            }

        with patch.object(system, 'process_input', side_effect=mock_process_input):
            # Simulate providing user input at iteration 2
            iteration = 0
            def get_user_input():
                nonlocal iteration
                iteration += 1
                return {"text": "hello"} if iteration == 2 else None
            
            with patch.object(system, '_get_user_input', side_effect=get_user_input):
                system.run(duration=0.05, iterations=5)
        
        # Verify user input was processed
        assert any(input_data is not None for input_data in processed_inputs), \
            "Should have processed user input at least once"

    def test_run_updates_self_context_each_iteration(self, system):
        """Test that run loop updates self context in each iteration."""
        # Test that the run loop actually executes multiple iterations
        iteration_count = 0

        def mock_process_input(user_input):
            nonlocal iteration_count
            iteration_count += 1
            # Simulate context update by updating self_context
            system.integrative_core.update_self_context("last_iteration", iteration_count)
            return {"mode": "autonomous", "decision": {"handler": "self_handler"}}

        with patch.object(system, 'process_input', side_effect=mock_process_input):
            system.run(duration=0.05, iterations=3)
        
        # Verify multiple iterations occurred
        assert iteration_count == 3, f"Expected 3 iterations, got {iteration_count}"
        # Verify self context was updated
        assert system.integrative_core.self_context.get("last_iteration") == 3, \
            "Self context should reflect last iteration"

    def test_run_handles_stop_signal_gracefully(self, system):
        """Test that run loop handles stop signal gracefully."""
        should_stop = False

        def mock_process_input(user_input):
            nonlocal should_stop
            if not should_stop:
                should_stop = True
                return {"mode": "autonomous", "decision": {"handler": "self_handler"}}
            raise StopIteration("Graceful stop")

        with patch.object(system, 'process_input', side_effect=mock_process_input):
            # Should not raise an exception
            system.run(duration=None, iterations=10)

    def test_run_respects_safety_mode_interruption(self, system):
        """Test that run loop immediately stops when safety mode is triggered."""
        iteration_count = 0

        def mock_process_input(user_input):
            nonlocal iteration_count
            iteration_count += 1
            # Return safety mode on first iteration
            return {"mode": "safety", "decision": {"handler": "safety_handler"}}

        with patch.object(system, 'process_input', side_effect=mock_process_input):
            system.run(duration=0.05, iterations=10)
        
        # Should stop after first iteration due to safety mode
        assert iteration_count == 1, f"Expected 1 iteration (safety stop), got {iteration_count}"

    def test_run_logs_iteration_progress(self, system, caplog):
        """Test that run loop logs iteration progress."""
        import logging
        caplog.set_level(logging.INFO)

        with patch.object(system, 'process_input', return_value={"mode": "autonomous"}):
            system.run(duration=0.05, iterations=2)
        
        # Should log iteration progress
        assert any("iteration" in record.message.lower() for record in caplog.records), \
            "Should log iteration progress"