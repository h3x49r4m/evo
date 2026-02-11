"""Tests for Feedback Loop (TDD Red Phase)."""

import pytest
from evo.feedback import FeedbackLoop


class TestObservationProcessor:
    """Tests for observation processor."""
    
    def test_process_observation_extracts_key_info(self):
        """Given feedback loop, When processing observation, Then extracts key info."""
        feedback = FeedbackLoop()
        observation = {"action": "write_code", "result": "success", "output": "file written"}
        processed = feedback.process_observation(observation)
        assert "action" in processed
        assert "result" in processed
    
    def test_process_observation_detects_patterns(self):
        """Given feedback loop, When processing multiple observations, Then detects patterns."""
        feedback = FeedbackLoop()
        feedback.process_observation({"action": "write_code", "result": "success"})
        feedback.process_observation({"action": "write_code", "result": "success"})
        patterns = feedback.detect_patterns()
        assert len(patterns) >= 1


class TestMemoryManager:
    """Tests for memory manager."""
    
    def test_store_observation_in_working_memory(self):
        """Given feedback loop, When storing observation, Then saves to working memory."""
        feedback = FeedbackLoop()
        feedback.store_observation({"action": "test"})
        assert feedback.get_working_memory_size() >= 1
    
    def test_store_observation_in_episodic_memory(self):
        """Given feedback loop, When storing observation, Then saves to episodic memory."""
        feedback = FeedbackLoop()
        feedback.store_observation({"action": "test"})
        episodic_count = feedback.get_episodic_memory_count()
        assert episodic_count >= 1
    
    def test_update_semantic_memory_with_learnings(self):
        """Given feedback loop, When extracting learnings, Then updates semantic memory."""
        feedback = FeedbackLoop()
        feedback.update_semantic_memory("python_writing", "Python code writing skill")
        fact = feedback.get_semantic_fact("python_writing")
        assert fact == "Python code writing skill"


class TestFeedbackLoopIntegration:
    """Integration tests for feedback loop."""
    
    def test_full_workflow_process_store_and_learn(self):
        """Given feedback loop, When processing through full workflow, Then correctly processes."""
        feedback = FeedbackLoop()
        # Process observation
        observation = {"action": "write_code", "result": "success"}
        processed = feedback.process_observation(observation)
        # Store in memory
        feedback.store_observation(processed)
        # Extract learnings
        feedback.update_semantic_memory("code_writing", "Can write code successfully")
        # Verify
        assert feedback.get_working_memory_size() >= 1
        assert feedback.get_semantic_fact("code_writing") is not None