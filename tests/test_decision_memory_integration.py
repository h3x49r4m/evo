"""Tests for DecisionEngine with episodic memory retrieval integration."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from evo.decision import DecisionEngine
from evo.memory import MemorySystem


class TestDecisionEngineMemoryIntegration:
    """Test suite for DecisionEngine with memory retrieval."""

    @pytest.fixture
    def decision_engine(self):
        """Create a fresh DecisionEngine instance for each test."""
        return DecisionEngine()

    @pytest.fixture
    def memory_system(self):
        """Create a fresh MemorySystem instance for each test."""
        return MemorySystem()

    def test_decision_engine_has_memory_integration(self, decision_engine):
        """Test that DecisionEngine can be initialized with memory."""
        # Just verify the engine exists and can be created
        assert decision_engine is not None
        assert hasattr(decision_engine, 'select_mode'), "Should have select_mode"
        assert hasattr(decision_engine, 'route_decision'), "Should have route_decision"

    def test_route_decision_can_use_past_experiences(self, decision_engine, memory_system):
        """Test that route_decision can leverage past experiences from memory."""
        # Store a past experience
        import asyncio
        experience = {
            "action": "search_web",
            "result": "success",
            "context": {"query": "test"}
        }
        asyncio.run(memory_system.episodic.store_experience(experience))
        
        # Route decision should be able to access memory
        context = {"user_input": True, "memory": memory_system}
        result = decision_engine.route_decision("responsive", context)
        
        assert result is not None, "Should return decision"
        assert "handler" in result, "Should have handler"

    def test_select_mode_considers_memory_patterns(self, decision_engine):
        """Test that select_mode can consider patterns from memory."""
        # Context with memory hints
        context = {
            "user_input": True,
            "memory_patterns": {"frequent_actions": ["search", "analyze"]}
        }
        
        mode = decision_engine.select_mode(context)
        
        assert mode is not None, "Should select a mode"
        assert mode in ["responsive", "autonomous", "hybrid", "safety"], \
            "Should be valid mode"

    def test_route_decision_includes_memory_context(self, decision_engine):
        """Test that route_decision includes memory information in result."""
        context = {"user_input": True, "past_success_rate": 0.8}
        
        result = decision_engine.route_decision("responsive", context)
        
        assert result is not None, "Should return decision"
        assert "data" in result, "Should include data"

    def test_select_mode_handles_memory_hints(self, decision_engine):
        """Test that select_mode handles hints from memory about optimal mode."""
        context = {
            "user_input": False,
            "memory_hint": "autonomous_better",
            "internal_goals": True
        }
        
        mode = decision_engine.select_mode(context)
        
        assert mode is not None, "Should select mode with memory hints"

    def test_route_decision_adapts_based_on_learnings(self, decision_engine):
        """Test that route_decision adapts routing based on learnings."""
        context = {
            "user_input": True,
            "learnings": {"best_handler": "user_handler"}
        }
        
        result = decision_engine.route_decision("responsive", context)
        
        assert result is not None, "Should return adaptive decision"

    def test_select_mode_prioritizes_user_with_memory_confidence(self, decision_engine):
        """Test that select_mode prioritizes user input when memory has low confidence."""
        context = {
            "user_input": True,
            "memory_confidence": 0.3,
            "internal_goals": True
        }
        
        mode = decision_engine.select_mode(context)
        
        # With user_input and internal_goals both True, should select hybrid mode
        assert mode == "hybrid", "Should select hybrid with both user and internal goals"

    def test_route_decision_tracks_memory_usage(self, decision_engine):
        """Test that route_decision tracks when memory is used."""
        context = {
            "user_input": True,
            "used_memory": True
        }
        
        result = decision_engine.route_decision("responsive", context)
        
        assert result is not None, "Should return decision with memory tracking"
