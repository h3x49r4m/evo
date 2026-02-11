"""Tests for dependency injection of shared memory system."""

import pytest

from evo.main import EvoSystem
from evo.action import ActionLayer
from evo.feedback import FeedbackLoop


def test_evo_system_with_injected_memory():
    """Test that EvoSystem accepts injected MemorySystem."""
    from evo.memory import MemorySystem
    
    # Create a shared memory instance
    shared_memory = MemorySystem()
    
    # Create system with injected memory
    system = EvoSystem(memory=shared_memory)
    
    # Verify system uses the injected memory
    assert system.memory is shared_memory
    assert system.action.memory is shared_memory
    assert system.feedback._memory is shared_memory


def test_evo_system_creates_own_memory():
    """Test that EvoSystem creates its own MemorySystem when none injected."""
    system = EvoSystem()
    
    # Verify system has a memory instance
    assert system.memory is not None
    
    # Verify action layer has reference to the same memory
    assert system.action.memory is system.memory
    
    # Verify feedback loop has reference to the same memory
    assert system.feedback._memory is system.memory


def test_action_layer_with_injected_memory():
    """Test that ActionLayer accepts injected memory."""
    from evo.memory import MemorySystem
    
    shared_memory = MemorySystem()
    action = ActionLayer(memory=shared_memory)
    
    assert action.memory is shared_memory


def test_action_layer_without_memory():
    """Test that ActionLayer works without injected memory."""
    action = ActionLayer()
    
    assert action.memory is None
    # Should still be able to perform basic operations
    result = action.plan_action({"goal": "test"})
    assert "steps" in result


def test_feedback_loop_with_injected_memory():
    """Test that FeedbackLoop accepts injected memory."""
    from evo.memory import MemorySystem
    
    shared_memory = MemorySystem()
    feedback = FeedbackLoop(memory=shared_memory)
    
    assert feedback._memory is shared_memory


def test_feedback_loop_without_memory():
    """Test that FeedbackLoop creates its own memory when none injected."""
    feedback = FeedbackLoop()
    
    assert feedback._memory is not None
    # Should be able to store observations
    obs = feedback.process_observation({"action": "test", "result": "success"})
    assert obs["action"] == "test"


def test_shared_memory_state_across_components():
    """Test that components share memory state via dependency injection."""
    from evo.memory import MemorySystem
    
    shared_memory = MemorySystem()
    
    # Store data in working memory via feedback loop
    feedback = FeedbackLoop(memory=shared_memory)
    feedback.store_observation({"action": "test", "result": "success"})
    
    # Retrieve the same data via system memory
    assert shared_memory.working.retrieve("last_observation") is not None
    assert shared_memory.working.retrieve("episodic_count") == 1


def test_multiple_systems_share_memory():
    """Test that multiple EvoSystem instances can share the same memory."""
    from evo.memory import MemorySystem
    
    shared_memory = MemorySystem()
    
    system1 = EvoSystem(memory=shared_memory)
    system2 = EvoSystem(memory=shared_memory)
    
    # Both systems reference the same memory
    assert system1.memory is system2.memory
    assert system1.action.memory is system2.action.memory
    assert system1.feedback._memory is system2.feedback._memory