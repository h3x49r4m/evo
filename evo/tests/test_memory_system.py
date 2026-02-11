"""Tests for Memory System (TDD Red Phase)."""

import pytest
from evo.memory import MemorySystem


class TestWorkingMemory:
    """Tests for Working Memory component."""
    
    def test_working_memory_init_creates_empty_context(self):
        """Given a new working memory instance, When initialized, Then creates empty context dict."""
        working_memory = MemorySystem.WorkingMemory()
        assert working_memory.context == {}
    
    def test_working_memory_store_adds_key_value_pair(self):
        """Given a working memory instance, When storing a key-value pair, Then it is retrievable."""
        working_memory = MemorySystem.WorkingMemory()
        working_memory.store("user_input", "Hello, world!")
        assert working_memory.retrieve("user_input") == "Hello, world!"
    
    def test_working_memory_retrieve_nonexistent_key_returns_none(self):
        """Given a working memory instance, When retrieving nonexistent key, Then returns None."""
        working_memory = MemorySystem.WorkingMemory()
        assert working_memory.retrieve("nonexistent") is None
    
    def test_working_memory_clear_empties_all_context(self):
        """Given a working memory with data, When cleared, Then all data is removed."""
        working_memory = MemorySystem.WorkingMemory()
        working_memory.store("key1", "value1")
        working_memory.store("key2", "value2")
        working_memory.clear()
        assert working_memory.context == {}


class TestEpisodicMemory:
    """Tests for Episodic Memory component."""
    
    @pytest.mark.asyncio
    async def test_episodic_memory_init_creates_vector_db(self):
        """Given a new episodic memory instance, When initialized, Then creates vector database."""
        episodic_memory = MemorySystem.EpisodicMemory(collection_name="test_episodes")
        assert episodic_memory.collection is not None
        await episodic_memory.cleanup()
    
    @pytest.mark.asyncio
    async def test_episodic_memory_init_without_chromadb_falls_back_to_dict(self):
        """Given new episodic memory without ChromaDB, When initialized, Then uses dictionary fallback (lines 10-11)."""
        episodic_memory = MemorySystem.EpisodicMemory(
            collection_name="test_episodes",
            use_chromadb=False
        )
        # Should use in-memory dictionary
        assert episodic_memory.collection == episodic_memory  # Self fallback
        assert episodic_memory.client is None
        assert isinstance(episodic_memory._experiences, dict)
    
    @pytest.mark.asyncio
    async def test_episodic_memory_store_experience_returns_id(self):
        """Given an episodic memory instance, When storing an experience, Then returns experience ID."""
        episodic_memory = MemorySystem.EpisodicMemory(collection_name="test_episodes")
        experience = {"action": "test_action", "outcome": "success"}
        experience_id = await episodic_memory.store_experience(experience)
        assert experience_id is not None
        await episodic_memory.cleanup()
    
    @pytest.mark.asyncio
    async def test_episodic_memory_retrieve_similar_returns_experiences(self):
        """Given episodic memory with experiences, When retrieving similar, Then returns matching experiences."""
        episodic_memory = MemorySystem.EpisodicMemory(collection_name="test_episodes")
        exp1 = {"action": "code_write", "outcome": "success"}
        exp2 = {"action": "test_write", "outcome": "failure"}
        await episodic_memory.store_experience(exp1)
        await episodic_memory.store_experience(exp2)
        similar = await episodic_memory.retrieve_similar("code_write", k=1)
        assert len(similar) >= 1
        await episodic_memory.cleanup()
    
    @pytest.mark.asyncio
    async def test_episodic_memory_cleanup_without_chromadb_clears_dict(self):
        """Given episodic memory without ChromaDB, When cleaning up, Then clears dictionary (line 134)."""
        episodic_memory = MemorySystem.EpisodicMemory(
            collection_name="test_episodes",
            use_chromadb=False
        )
        # Store some experiences
        await episodic_memory.store_experience({"action": "test1"})
        await episodic_memory.store_experience({"action": "test2"})
        assert len(episodic_memory._experiences) == 2
        
        # Cleanup should clear the dictionary
        await episodic_memory.cleanup()
        assert len(episodic_memory._experiences) == 0


class TestSemanticMemory:
    """Tests for Semantic Memory component."""
    
    def test_semantic_memory_init_creates_empty_knowledge_base(self):
        """Given a new semantic memory instance, When initialized, Then creates empty knowledge base."""
        semantic_memory = MemorySystem.SemanticMemory()
        assert semantic_memory.knowledge == {}
    
    def test_semantic_memory_add_fact_stores_key_value(self):
        """Given a semantic memory instance, When adding a fact, Then it is retrievable."""
        semantic_memory = MemorySystem.SemanticMemory()
        semantic_memory.add_fact("python_version", "3.12")
        assert semantic_memory.retrieve_fact("python_version") == "3.12"
    
    def test_semantic_memory_add_fact_overwrites_existing(self):
        """Given semantic memory with existing fact, When adding same key, Then overwrites value."""
        semantic_memory = MemorySystem.SemanticMemory()
        semantic_memory.add_fact("key", "old_value")
        semantic_memory.add_fact("key", "new_value")
        assert semantic_memory.retrieve_fact("key") == "new_value"
    
    def test_semantic_memory_retrieve_nonexistent_returns_none(self):
        """Given semantic memory instance, When retrieving nonexistent fact, Then returns None."""
        semantic_memory = MemorySystem.SemanticMemory()
        assert semantic_memory.retrieve_fact("unknown") is None


class TestMemorySystemIntegration:
    """Integration tests for Memory System."""
    
    @pytest.mark.asyncio
    async def test_memory_system_init_creates_all_memory_components(self):
        """Given memory system instance, When initialized, Then creates all three memory components."""
        memory_system = MemorySystem(collection_name="test_memory")
        assert memory_system.working is not None
        assert memory_system.episodic is not None
        assert memory_system.semantic is not None
        await memory_system.cleanup()
    
    @pytest.mark.asyncio
    async def test_memory_system_workflow_integration(self):
        """Given memory system, When storing and retrieving across memories, Then data flows correctly."""
        memory_system = MemorySystem(collection_name="test_memory")
        # Store in working memory
        memory_system.working.store("current_goal", "write_code")
        # Store experience in episodic
        await memory_system.episodic.store_experience({"goal": "write_code", "result": "success"})
        # Store fact in semantic
        memory_system.semantic.add_fact("code_language", "python")
        # Verify all retrievable
        assert memory_system.working.retrieve("current_goal") == "write_code"
        similar = await memory_system.episodic.retrieve_similar("write_code")
        assert len(similar) >= 1
        assert memory_system.semantic.retrieve_fact("code_language") == "python"
        await memory_system.cleanup()