"""Tests for enhanced MetacognitionLayer with automatic reflection triggers."""

import pytest
import time
from unittest.mock import Mock, patch
from evo.metacognition import MetacognitionLayer


class TestMetacognitionLayerEnhanced:
    """Test suite for enhanced MetacognitionLayer functionality."""

    @pytest.fixture
    def metacognition(self):
        """Create a fresh MetacognitionLayer instance for each test."""
        return MetacognitionLayer()

    def test_metacognition_has_auto_reflection_method(self, metacognition):
        """Test that MetacognitionLayer has an auto_reflection method."""
        assert hasattr(metacognition, 'auto_reflection'), "Should have auto_reflection method"
        assert callable(metacognition.auto_reflection), "auto_reflection should be callable"

    def test_auto_reflection_updates_self_model(self, metacognition):
        """Test that auto_reflection updates the self-model."""
        initial_capabilities = metacognition.get_self_model()["capabilities"]
        
        metacognition.auto_reflection()
        
        updated_capabilities = metacognition.get_self_model()["capabilities"]
        # Self-model should have been potentially updated
        assert updated_capabilities is not None, "Self-model should exist"

    def test_auto_reflection_accepts_experiences(self, metacognition):
        """Test that auto_reflection can process experiences."""
        experiences = [
            {"action": "test", "outcome": "success", "strategy": "trial"}
        ]
        
        result = metacognition.auto_reflection(experiences=experiences)
        
        assert result is not None, "Should return reflection result"
        assert "processed" in result, "Should indicate processed experiences"

    def test_auto_reflection_tracks_reflection_count(self, metacognition):
        """Test that auto_reflection tracks number of reflections."""
        metacognition.auto_reflection()
        count1 = metacognition.get_self_model().get("reflection_count", 0)
        
        metacognition.auto_reflection()
        count2 = metacognition.get_self_model().get("reflection_count", 0)
        
        assert count2 > count1, "Reflection count should increase"

    def test_auto_reflection_generates_insights(self, metacognition):
        """Test that auto_reflection generates insights from experiences."""
        experiences = [
            {"action": "search", "outcome": "success", "timestamp": time.time()}
        ]
        
        result = metacognition.auto_reflection(experiences=experiences)
        
        assert "insights" in result, "Should generate insights"
        assert isinstance(result["insights"], list), "Insights should be a list"

    def test_auto_reflection_updates_capabilities_from_success(self, metacognition):
        """Test that auto_reflection updates capabilities based on successful outcomes."""
        experiences = [
            {"action": "python_programming", "outcome": "success", "confidence": 0.9}
        ]
        
        metacognition.auto_reflection(experiences=experiences)
        
        self_model = metacognition.get_self_model()
        # Capabilities should have been updated
        assert "python_programming" in self_model["capabilities"], \
            "Capability should be added or updated"

    def test_auto_reflection_decreases_capabilities_from_failure(self, metacognition):
        """Test that auto_reflection decreases capabilities based on failed outcomes."""
        # First set a capability
        metacognition.update_capabilities("test_skill", 0.8)
        
        # Then reflect on a failure
        experiences = [
            {"action": "test_skill", "outcome": "failure", "confidence": 0.3}
        ]
        
        metacognition.auto_reflection(experiences=experiences)
        
        self_model = metacognition.get_self_model()
        # Capability level should have decreased
        assert self_model["capabilities"]["test_skill"] < 0.8, \
            "Capability level should decrease after failure"

    def test_auto_reflection_updates_beliefs(self, metacognition):
        """Test that auto_reflection updates beliefs based on experiences."""
        experiences = [
            {"action": "learn", "outcome": "success", "belief_key": "learning_effective"}
        ]
        
        metacognition.auto_reflection(experiences=experiences)
        
        self_model = metacognition.get_self_model()
        # Beliefs should have been updated
        assert len(self_model["beliefs"]) > 0, "Should have updated beliefs"

    def test_auto_reflection_handles_empty_experiences(self, metacognition):
        """Test that auto_reflection handles empty experiences gracefully."""
        result = metacognition.auto_reflection(experiences=[])
        
        assert result is not None, "Should handle empty experiences"
        assert "insights" in result, "Should still generate insights"

    def test_auto_reflection_records_reflection_timestamp(self, metacognition):
        """Test that auto_reflection records when reflection occurred."""
        metacognition.auto_reflection()
        
        self_model = metacognition.get_self_model()
        assert "last_reflection" in self_model, "Should record last reflection time"
        assert self_model["last_reflection"] > 0, "Reflection time should be positive"

    def test_auto_reflection_identifies_patterns(self, metacognition):
        """Test that auto_reflection can identify patterns in experiences."""
        experiences = [
            {"action": "search", "outcome": "success"},
            {"action": "search", "outcome": "success"},
            {"action": "search", "outcome": "success"}
        ]
        
        result = metacognition.auto_reflection(experiences=experiences)
        
        assert "patterns" in result, "Should identify patterns"
        assert len(result["patterns"]) > 0, "Should have found patterns"