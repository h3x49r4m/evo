"""Tests for main.py module import and initialization."""

import pytest


def test_main_module_imports():
    """Test that main.py can import all required modules."""
    # This test will fail initially if imports are broken
    # It should pass after we fix the import paths
    try:
        from evo.main import EvoSystem, create_evo_system, main
        assert EvoSystem is not None
        assert create_evo_system is not None
        assert main is not None
    except ImportError as e:
        pytest.fail(f"Failed to import from main.py: {e}")


def test_evo_system_creation():
    """Test that EvoSystem can be instantiated."""
    from evo.main import create_evo_system
    
    system = create_evo_system()
    assert system is not None
    assert hasattr(system, 'memory')
    assert hasattr(system, 'perception')
    assert hasattr(system, 'decision')
    assert hasattr(system, 'goal')
    assert hasattr(system, 'capability')
    assert hasattr(system, 'action')
    assert hasattr(system, 'metacognition')
    assert hasattr(system, 'exploration')
    assert hasattr(system, 'safety')
    assert hasattr(system, 'feedback')
    assert hasattr(system, 'integrative_core')
    assert hasattr(system, 'handler')


def test_process_input():
    """Test that process_input method works correctly."""
    from evo.main import create_evo_system
    
    system = create_evo_system()
    
    # Test with user input
    result = system.process_input({"text": "test input"})
    assert result is not None
    assert "mode" in result
    assert "decision" in result
    assert "integrated" in result
    
    # Test without user input
    result = system.process_input(None)
    assert result is not None
    assert "mode" in result