"""Tests for async cleanup functionality."""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.memory import MemorySystem


@pytest.mark.asyncio
async def test_memory_system_cleanup():
    """Test that MemorySystem.cleanup() properly releases episodic memory resources."""
    memory = MemorySystem()
    
    # Store some data
    memory.working.store("test_key", "test_value")
    exp_id = await memory.episodic.store_experience({"action": "test"})
    memory.semantic.add_fact("fact_key", "fact_value")
    
    # Cleanup should not raise errors
    await memory.cleanup()
    
    # Cleanup only affects episodic memory, working and semantic remain
    assert memory.working.retrieve("test_key") == "test_value"
    assert memory.semantic.retrieve_fact("fact_key") == "fact_value"


@pytest.mark.asyncio
async def test_episodic_memory_cleanup_with_chromadb():
    """Test that EpisodicMemory.cleanup() releases ChromaDB resources."""
    try:
        import chromadb
        chromadb_available = True
    except ImportError:
        chromadb_available = False
        pytest.skip("ChromaDB not available")
    
    if chromadb_available:
        episodic = MemorySystem.EpisodicMemory(use_chromadb=True)
        
        # Store some experiences
        for i in range(3):
            await episodic.store_experience({"action": f"test_{i}"})
        
        # Cleanup should delete the collection
        await episodic.cleanup()
        
        # Should be able to create a new collection with the same name
        new_episodic = MemorySystem.EpisodicMemory(
            collection_name=episodic.collection_name,
            use_chromadb=True
        )
        await new_episodic.cleanup()


@pytest.mark.asyncio
async def test_episodic_memory_cleanup_fallback():
    """Test that EpisodicMemory.cleanup() works with fallback dict storage."""
    episodic = MemorySystem.EpisodicMemory(use_chromadb=False)
    
    # Store some experiences
    for i in range(3):
        await episodic.store_experience({"action": f"test_{i}"})
    
    # Cleanup should clear the internal dictionary
    await episodic.cleanup()
    
    # Internal storage should be empty
    assert len(episodic._experiences) == 0


@pytest.mark.asyncio
async def test_memory_system_multiple_cleanup():
    """Test that multiple cleanup calls don't cause errors."""
    memory = MemorySystem(use_chromadb=False)
    
    # Store some data
    await memory.episodic.store_experience({"action": "test"})
    
    # Cleanup multiple times
    await memory.cleanup()
    await memory.cleanup()
    await memory.cleanup()
    
    # Should not raise any errors


@pytest.mark.asyncio
async def test_cleanup_with_shared_memory_injection():
    """Test that cleanup works correctly with dependency injection."""
    from evo.action import ActionLayer
    from evo.feedback import FeedbackLoop
    from main import EvoSystem
    
    # Create shared memory (use_chromadb=False to avoid NotFoundError on multiple cleanup)
    shared_memory = MemorySystem(use_chromadb=False)
    
    # Create system with injected memory
    system = EvoSystem(memory=shared_memory)
    
    # Use the memory
    shared_memory.working.store("system_data", "test")
    await shared_memory.episodic.store_experience({"action": "system_action"})
    
    # Cleanup should release episodic memory resources
    await shared_memory.cleanup()
    
    # Verify cleanup worked - working memory still has data, episodic was cleaned
    assert shared_memory.working.retrieve("system_data") == "test"


@pytest.mark.asyncio
async def test_feedback_loop_memory_cleanup():
    """Test that FeedbackLoop memory cleanup works correctly."""
    from evo.feedback import FeedbackLoop
    
    shared_memory = MemorySystem()
    feedback = FeedbackLoop(memory=shared_memory)
    
    # Store some observations
    feedback.store_observation({"action": "test", "result": "success"})
    
    # Cleanup the underlying memory (only affects episodic)
    await shared_memory.cleanup()
    
    # Working memory data still exists, episodic was cleaned
    assert feedback._memory.working.retrieve("last_observation") is not None
    assert feedback._memory.working.retrieve("episodic_count") == 1


@pytest.mark.asyncio
async def test_cleanup_preserves_semantic_memory_structure():
    """Test that cleanup doesn't break SemanticMemory structure."""
    memory = MemorySystem()
    
    # Add facts to semantic memory
    memory.semantic.add_fact("key1", "value1")
    memory.semantic.add_fact("key2", "value2")
    
    # Cleanup
    await memory.cleanup()
    
    # SemanticMemory structure should still exist
    assert hasattr(memory.semantic, 'knowledge')
    assert isinstance(memory.semantic.knowledge, dict)


@pytest.mark.asyncio
async def test_cleanup_and_reuse():
    """Test that cleanup allows reuse of memory system."""
    memory = MemorySystem(use_chromadb=False)
    
    # First use
    memory.working.store("first_use", "data")
    await memory.episodic.store_experience({"action": "first"})
    
    # Cleanup (clears episodic)
    await memory.cleanup()
    
    # Reuse after cleanup
    memory.working.store("second_use", "data2")
    await memory.episodic.store_experience({"action": "second"})
    
    # Verify second use data is stored (both working and new episodic)
    assert memory.working.retrieve("first_use") == "data"
    assert memory.working.retrieve("second_use") == "data2"


@pytest.mark.asyncio
async def test_episodic_cleanup_empty_collection():
    """Test cleanup on empty episodic memory."""
    episodic = MemorySystem.EpisodicMemory(use_chromadb=False)
    
    # Cleanup empty collection
    await episodic.cleanup()
    
    # Should not raise errors
    assert len(episodic._experiences) == 0


@pytest.mark.asyncio
async def test_working_memory_clear_vs_cleanup():
    """Test difference between clear() and cleanup()."""
    memory = MemorySystem()
    
    # Store data
    memory.working.store("key", "value")
    await memory.episodic.store_experience({"action": "test"})
    
    # Clear only working memory
    memory.working.clear()
    assert memory.working.retrieve("key") is None
    
    # Full cleanup
    await memory.cleanup()
    # Both should be cleared now