"""Tests for Exploration Engine (TDD Red Phase)."""

import pytest
from evo.exploration import ExplorationEngine


class TestNoveltyDetector:
    """Tests for novelty detector."""
    
    def test_detect_novelty_finds_unused_capabilities(self):
        """Given exploration engine, When detecting novelty, Then finds unused capabilities."""
        engine = ExplorationEngine()
        engine.register_capability("used_skill", True)
        engine.register_capability("unused_skill", False)
        novel = engine.detect_novelty()
        assert "unused_skill" in str(novel)
    
    def test_detect_novelty_with_all_used_returns_empty(self):
        """Given exploration engine with all used, When detecting, Then returns empty."""
        engine = ExplorationEngine()
        engine.register_capability("skill1", True)
        engine.register_capability("skill2", True)
        novel = engine.detect_novelty()
        assert len(novel) == 0


class TestRandomExploration:
    """Tests for random exploration."""
    
    def test_random_exploration_returns_exploration_goal(self):
        """Given exploration engine, When doing random exploration, Then returns goal."""
        engine = ExplorationEngine()
        goal = engine.random_exploration()
        assert "goal" in goal
        assert "type" in goal


class TestPurposeSynthesis:
    """Tests for purpose synthesis."""
    
    def test_synthesize_purpose_creates_purpose_statement(self):
        """Given exploration engine, When synthesizing purpose, Then creates statement."""
        engine = ExplorationEngine()
        purpose = engine.synthesize_purpose({"reflection": "I learn and improve"})
        assert "purpose" in purpose
        assert "statement" in purpose


class TestExplorationEngineIntegration:
    """Integration tests for exploration engine."""
    
    def test_full_workflow_detect_explore_and_synthesize(self):
        """Given exploration engine, When processing through full workflow, Then correctly processes."""
        engine = ExplorationEngine()
        # Register capabilities
        engine.register_capability("new_skill", False)
        # Detect novelty
        novel = engine.detect_novelty()
        # Random exploration
        exploration = engine.random_exploration()
        # Synthesize purpose
        purpose = engine.synthesize_purpose({"reflections": ["I exist to learn"]})
        # Verify
        assert len(novel) >= 1 or exploration is not None
        assert "purpose" in purpose