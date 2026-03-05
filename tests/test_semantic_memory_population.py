"""Tests for semantic memory population with learned facts and patterns."""

import pytest
from evo.memory import MemorySystem


class TestSemanticMemoryPopulation:
    """Test suite for semantic memory population functionality."""

    @pytest.fixture
    def memory(self):
        """Create a fresh MemorySystem instance for each test."""
        return MemorySystem()

    def test_semantic_memory_can_populate_facts(self, memory):
        """Test that semantic memory can be populated with facts."""
        memory.semantic.add_fact("learned_fact", "test_value")
        
        retrieved = memory.semantic.retrieve_fact("learned_fact")
        assert retrieved == "test_value", "Should retrieve stored fact"

    def test_populate_from_patterns(self, memory):
        """Test that semantic memory can be populated from detected patterns."""
        patterns = [
            {"action": "search", "frequency": 5, "success_rate": 0.9}
        ]
        
        # Simulate populating from patterns
        for pattern in patterns:
            key = f"pattern_{pattern['action']}"
            value = f"High frequency action: {pattern['frequency']} times"
            memory.semantic.add_fact(key, value)
        
        # Verify fact was stored
        retrieved = memory.semantic.retrieve_fact("pattern_search")
        assert retrieved is not None, "Should store pattern as fact"

    def test_populate_from_success_rates(self, memory):
        """Test that semantic memory can store success rate information."""
        success_rates = {
            "python": 0.95,
            "search": 0.8,
            "analyze": 0.7
        }
        
        # Store success rates
        for action, rate in success_rates.items():
            memory.semantic.add_fact(f"success_rate_{action}", rate)
        
        # Verify all rates stored
        for action in success_rates:
            key = f"success_rate_{action}"
            retrieved = memory.semantic.retrieve_fact(key)
            assert retrieved is not None, f"Should retrieve success rate for {action}"

    def test_populate_from_recommendations(self, memory):
        """Test that semantic memory can store action recommendations."""
        recommendations = [
            "Use python for high success tasks",
            "Avoid search for complex queries"
        ]
        
        for i, rec in enumerate(recommendations):
            memory.semantic.add_fact(f"recommendation_{i}", rec)
        
        # Verify recommendations stored
        rec0 = memory.semantic.retrieve_fact("recommendation_0")
        assert rec0 == "Use python for high success tasks", "Should store recommendation"

    def test_populate_from_insights(self, memory):
        """Test that semantic memory can store learned insights."""
        insights = [
            {"type": "pattern", "message": "Search succeeds 90% of the time"},
            {"type": "trend", "message": "Python usage increasing"}
        ]
        
        for insight in insights:
            key = f"insight_{insight['type']}"
            memory.semantic.add_fact(key, insight["message"])
        
        # Verify insights stored
        retrieved = memory.semantic.retrieve_fact("insight_pattern")
        assert retrieved is not None, "Should store insight"

    def test_populate_from_best_actions(self, memory):
        """Test that semantic memory can track best performing actions."""
        best_actions = ["python", "analyze", "summarize"]
        
        memory.semantic.add_fact("best_actions", best_actions)
        
        retrieved = memory.semantic.retrieve_fact("best_actions")
        assert retrieved == best_actions, "Should track best actions"

    def test_populate_from_failing_actions(self, memory):
        """Test that semantic memory can track actions to avoid."""
        failing_actions = ["deprecated_api", "slow_method"]
        
        memory.semantic.add_fact("failing_actions", failing_actions)
        
        retrieved = memory.semantic.retrieve_fact("failing_actions")
        assert retrieved == failing_actions, "Should track failing actions"

    def test_populate_updates_existing_facts(self, memory):
        """Test that populating semantic memory updates existing facts."""
        memory.semantic.add_fact("dynamic_fact", "initial_value")
        
        # Update the fact
        memory.semantic.add_fact("dynamic_fact", "updated_value")
        
        retrieved = memory.semantic.retrieve_fact("dynamic_fact")
        assert retrieved == "updated_value", "Should update existing fact"

    def test_populate_from_metacognition(self, memory):
        """Test that semantic memory can store metacognitive learnings."""
        metacognition_data = {
            "reflection_count": 5,
            "last_reflection": "2026-03-05",
            "learning_score": 0.75
        }
        
        for key, value in metacognition_data.items():
            memory.semantic.add_fact(f"meta_{key}", value)
        
        # Verify all metacognitive data stored
        for key in metacognition_data:
            retrieved = memory.semantic.retrieve_fact(f"meta_{key}")
            assert retrieved is not None, f"Should store meta_{key}"

    def test_populate_from_exploration(self, memory):
        """Test that semantic memory can store exploration findings."""
        exploration_results = {
            "capabilities_discovered": 3,
            "new_purposes": ["learning", "adaptation"]
        }
        
        for key, value in exploration_results.items():
            memory.semantic.add_fact(f"explore_{key}", value)
        
        # Verify exploration data stored
        discovered = memory.semantic.retrieve_fact("explore_capabilities_discovered")
        assert discovered == 3, "Should store exploration findings"

    def test_populate_preserves_facts_across_operations(self, memory):
        """Test that populated facts persist across memory operations."""
        # Store a fact
        memory.semantic.add_fact("persistent_fact", "should_remain")
        
        # Perform other operations
        memory.working.store("temp", "temporary")
        
        # Verify fact still exists
        retrieved = memory.semantic.retrieve_fact("persistent_fact")
        assert retrieved == "should_remain", "Facts should persist"

    def test_populate_handles_complex_data_structures(self, memory):
        """Test that semantic memory can store complex data structures."""
        complex_data = {
            "nested": {
                "level1": {
                    "level2": ["item1", "item2"]
                }
            }
        }
        
        memory.semantic.add_fact("complex_data", complex_data)
        
        retrieved = memory.semantic.retrieve_fact("complex_data")
        assert retrieved is not None, "Should store complex data"
        assert retrieved["nested"]["level1"]["level2"][0] == "item1", "Should preserve structure"