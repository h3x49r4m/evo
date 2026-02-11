"""Tests for Metacognition Layer (TDD Red Phase)."""

import pytest
from evo.metacognition import MetacognitionLayer


class TestReflectionTrigger:
    """Tests for reflection trigger."""
    
    def test_trigger_reflection_creates_reflection_event(self):
        """Given metacognition layer, When triggering reflection, Then creates event."""
        meta = MetacognitionLayer()
        event = meta.trigger_reflection("periodic")
        assert event["type"] == "reflection"
        assert event["trigger"] == "periodic"
    
    def test_trigger_reflection_with_event_data(self):
        """Given metacognition layer, When triggering with event data, Then includes data."""
        meta = MetacognitionLayer()
        event = meta.trigger_reflection("event", {"action": "completed"})
        assert event["data"]["action"] == "completed"


class TestSelfModelUpdate:
    """Tests for self-model update."""
    
    def test_update_capabilities_adds_capability(self):
        """Given metacognition layer, When updating capabilities, Then adds to model."""
        meta = MetacognitionLayer()
        meta.update_capabilities("new_skill", 0.8)
        capabilities = meta.get_self_model()["capabilities"]
        assert "new_skill" in capabilities
    
    def test_update_beliefs_updates_self_belief(self):
        """Given metacognition layer, When updating beliefs, Then changes self-belief."""
        meta = MetacognitionLayer()
        meta.update_beliefs("can_write_code", True)
        beliefs = meta.get_self_model()["beliefs"]
        assert beliefs["can_write_code"] is True


class TestMetaLearning:
    """Tests for meta-learning."""
    
    def test_learn_from_experience_updates_strategy(self):
        """Given metacognition layer, When learning from experience, Then updates strategy."""
        meta = MetacognitionLayer()
        meta.learn_from_experience({"outcome": "success", "strategy": "test"})
        strategies = meta.get_learned_strategies()
        assert len(strategies) >= 1


class TestMetacognitionIntegration:
    """Integration tests for metacognition layer."""
    
    def test_full_workflow_reflect_update_and_learn(self):
        """Given metacognition layer, When processing through full workflow, Then correctly processes."""
        meta = MetacognitionLayer()
        # Trigger reflection
        event = meta.trigger_reflection("periodic")
        # Update self-model
        meta.update_capabilities("writing", 0.9)
        # Learn from experience
        meta.learn_from_experience({"outcome": "success"})
        # Verify
        assert meta.get_self_model()["capabilities"]["writing"] == 0.9
        assert len(meta.get_learned_strategies()) >= 1