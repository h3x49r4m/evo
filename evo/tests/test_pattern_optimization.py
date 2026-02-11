"""Tests for optimized pattern detection."""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.feedback import FeedbackLoop


def test_pattern_detection_uses_index():
    """Test that pattern detection uses pre-built index."""
    feedback = FeedbackLoop()
    
    # Process observations
    feedback.process_observation({"action": "search", "result": "success"})
    feedback.process_observation({"action": "search", "result": "success"})
    feedback.process_observation({"action": "send_email", "result": "success"})
    
    # Check frequency index was built
    assert feedback._action_frequency["search"] == 2
    assert feedback._action_frequency["send_email"] == 1
    
    # Detect patterns
    patterns = feedback.detect_patterns()
    assert len(patterns) == 1
    assert patterns[0]["action"] == "search"
    assert patterns[0]["frequency"] == 2


def test_pattern_detection_with_no_observations():
    """Test pattern detection with no observations."""
    feedback = FeedbackLoop()
    
    patterns = feedback.detect_patterns()
    assert patterns == []


def test_pattern_detection_single_occurrence():
    """Test that actions with single occurrence are not patterns."""
    feedback = FeedbackLoop()
    
    feedback.process_observation({"action": "test", "result": "success"})
    
    patterns = feedback.detect_patterns()
    assert patterns == []


def test_pattern_detection_multiple_patterns():
    """Test detection of multiple patterns."""
    feedback = FeedbackLoop()
    
    # Create multiple patterns
    feedback.process_observation({"action": "search", "result": "success"})
    feedback.process_observation({"action": "search", "result": "success"})
    feedback.process_observation({"action": "send_email", "result": "success"})
    feedback.process_observation({"action": "send_email", "result": "success"})
    feedback.process_observation({"action": "scrape", "result": "success"})
    
    patterns = feedback.detect_patterns()
    assert len(patterns) == 2
    
    pattern_actions = {p["action"] for p in patterns}
    assert "search" in pattern_actions
    assert "send_email" in pattern_actions
    assert "scrape" not in pattern_actions


def test_pattern_detection_frequency_tracking():
    """Test that pattern frequency is correctly tracked."""
    feedback = FeedbackLoop()
    
    for _ in range(5):
        feedback.process_observation({"action": "repeat", "result": "success"})
    
    patterns = feedback.detect_patterns()
    assert len(patterns) == 1
    assert patterns[0]["frequency"] == 5


def test_pattern_detection_performance():
    """Test pattern detection performance with many observations."""
    import time
    
    feedback = FeedbackLoop()
    
    # Add 1000 observations
    for i in range(1000):
        action = f"action_{i % 10}"  # 10 unique actions, each appears 100 times
        feedback.process_observation({"action": action, "result": "success"})
    
    # Time pattern detection - should be very fast with index
    start = time.time()
    patterns = feedback.detect_patterns()
    end = time.time()
    
    # All 10 actions should be patterns (each appears >= 2 times)
    assert len(patterns) == 10
    # Should be very fast (< 1ms)
    assert (end - start) < 0.001


def test_pattern_detection_incremental():
    """Test that pattern detection works incrementally."""
    feedback = FeedbackLoop()
    
    # First observation - no pattern
    feedback.process_observation({"action": "test", "result": "success"})
    patterns = feedback.detect_patterns()
    assert len(patterns) == 0
    
    # Second observation - pattern detected
    feedback.process_observation({"action": "test", "result": "success"})
    patterns = feedback.detect_patterns()
    assert len(patterns) == 1
    
    # Third observation - frequency updated
    feedback.process_observation({"action": "test", "result": "success"})
    patterns = feedback.detect_patterns()
    assert patterns[0]["frequency"] == 3


def test_pattern_detection_null_actions():
    """Test that null actions are handled correctly."""
    feedback = FeedbackLoop()
    
    feedback.process_observation({"action": None, "result": "success"})
    feedback.process_observation({"result": "success"})
    
    patterns = feedback.detect_patterns()
    assert patterns == []


def test_pattern_detection_mixed_actions():
    """Test pattern detection with mixed valid and null actions."""
    feedback = FeedbackLoop()
    
    feedback.process_observation({"action": "valid", "result": "success"})
    feedback.process_observation({"action": None, "result": "success"})
    feedback.process_observation({"action": "valid", "result": "success"})
    
    patterns = feedback.detect_patterns()
    assert len(patterns) == 1
    assert patterns[0]["action"] == "valid"


def test_frequency_index_state():
    """Test that frequency index is correctly maintained."""
    feedback = FeedbackLoop()
    
    # Initially empty
    assert len(feedback._action_frequency) == 0
    
    # Add some actions
    feedback.process_observation({"action": "action1", "result": "success"})
    feedback.process_observation({"action": "action2", "result": "success"})
    feedback.process_observation({"action": "action1", "result": "success"})
    
    # Check index state
    assert feedback._action_frequency["action1"] == 2
    assert feedback._action_frequency["action2"] == 1
    assert len(feedback._action_frequency) == 2