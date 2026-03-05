"""Tests for enhanced FeedbackLoop with learning integration."""

import pytest
from unittest.mock import Mock, patch
from evo.feedback import FeedbackLoop


class TestFeedbackLoopEnhanced:
    """Test suite for enhanced FeedbackLoop functionality."""

    @pytest.fixture
    def feedback_loop(self):
        """Create a fresh FeedbackLoop instance for each test."""
        return FeedbackLoop()

    def test_feedback_loop_has_get_learnings_method(self, feedback_loop):
        """Test that FeedbackLoop has a get_learnings method."""
        assert hasattr(feedback_loop, 'get_learnings'), "Should have get_learnings method"
        assert callable(feedback_loop.get_learnings), "get_learnings should be callable"

    def test_get_learnings_returns_observations(self, feedback_loop):
        """Test that get_learnings returns accumulated observations."""
        feedback_loop.process_observation({"action": "test", "result": "success"})
        
        learnings = feedback_loop.get_learnings()
        
        assert learnings is not None, "Should return learnings"
        assert "observations" in learnings, "Should include observations"
        assert len(learnings["observations"]) > 0, "Should have observations"

    def test_get_learnings_includes_patterns(self, feedback_loop):
        """Test that get_learnings includes detected patterns."""
        # Add multiple observations with same action
        for i in range(3):
            feedback_loop.process_observation({"action": "repeat", "result": "ok"})
        
        learnings = feedback_loop.get_learnings()
        
        assert "patterns" in learnings, "Should include patterns"
        assert len(learnings["patterns"]) > 0, "Should detect patterns"

    def test_get_learnings_includes_recommendations(self, feedback_loop):
        """Test that get_learnings includes action recommendations."""
        feedback_loop.process_observation({"action": "test", "result": "success"})
        
        learnings = feedback_loop.get_learnings()
        
        assert "recommendations" in learnings, "Should include recommendations"
        assert isinstance(learnings["recommendations"], list), "Recommendations should be a list"

    def test_get_learnings_tracks_success_rate(self, feedback_loop):
        """Test that get_learnings tracks success rates for actions."""
        feedback_loop.process_observation({"action": "good_action", "result": "success"})
        feedback_loop.process_observation({"action": "good_action", "result": "success"})
        feedback_loop.process_observation({"action": "good_action", "result": "failure"})
        
        learnings = feedback_loop.get_learnings()
        
        assert "success_rates" in learnings, "Should track success rates"
        assert "good_action" in learnings["success_rates"], "Should have rate for good_action"
        assert learnings["success_rates"]["good_action"] > 0, "Success rate should be positive"

    def test_get_learnings_suggests_best_actions(self, feedback_loop):
        """Test that get_learnings suggests best performing actions."""
        feedback_loop.process_observation({"action": "excellent", "result": "success"})
        feedback_loop.process_observation({"action": "poor", "result": "failure"})
        
        learnings = feedback_loop.get_learnings()
        
        assert "best_actions" in learnings, "Should suggest best actions"
        assert len(learnings["best_actions"]) > 0, "Should have best action suggestions"

    def test_get_learnings_identifies_failing_actions(self, feedback_loop):
        """Test that get_learnings identifies actions that frequently fail."""
        for i in range(3):
            feedback_loop.process_observation({"action": "failing", "result": "failure"})
        
        learnings = feedback_loop.get_learnings()
        
        assert "failing_actions" in learnings, "Should identify failing actions"
        assert len(learnings["failing_actions"]) > 0, "Should have failing actions"

    def test_get_learnings_provides_confidence_scores(self, feedback_loop):
        """Test that get_learnings provides confidence scores for recommendations."""
        feedback_loop.process_observation({"action": "test", "result": "success"})
        
        learnings = feedback_loop.get_learnings()
        
        assert "confidence" in learnings, "Should provide confidence scores"
        assert learnings["confidence"] >= 0, "Confidence should be non-negative"
        assert learnings["confidence"] <= 1, "Confidence should be <= 1"

    def test_get_learnings_handles_no_observations(self, feedback_loop):
        """Test that get_learnings handles empty observations gracefully."""
        learnings = feedback_loop.get_learnings()
        
        assert learnings is not None, "Should handle empty observations"
        assert "observations" in learnings, "Should still have observations key"
        assert "confidence" in learnings, "Should have confidence"

    def test_get_learnings_updates_semantic_memory(self, feedback_loop):
        """Test that get_learnings can update semantic memory with key learnings."""
        feedback_loop.process_observation({"action": "learn", "result": "success"})
        
        learnings = feedback_loop.get_learnings()
        
        # Should return learnings that can be stored
        assert "key_facts" in learnings, "Should extract key facts"
        assert isinstance(learnings["key_facts"], list), "Key facts should be a list"

    def test_get_learnings_tracks_learning_progress(self, feedback_loop):
        """Test that get_learnings tracks overall learning progress."""
        learnings1 = feedback_loop.get_learnings()
        feedback_loop.process_observation({"action": "test", "result": "success"})
        learnings2 = feedback_loop.get_learnings()
        
        assert "learning_score" in learnings1, "Should track learning score"
        assert "learning_score" in learnings2, "Should track learning score"
        # Learning score should increase with more observations
        assert learnings2["learning_score"] >= learnings1["learning_score"], \
            "Learning score should not decrease"