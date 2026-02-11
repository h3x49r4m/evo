"""Tests to verify project structure after refactoring."""

import sys
from pathlib import Path


def test_project_root_structure():
    """Test that project root has expected structure."""
    root = Path(__file__).parent.parent
    
    # Check that evo package is at root level (not in src/evo)
    evo_package = root / "evo"
    assert evo_package.exists(), f"evo package should be at {evo_package}"
    assert (evo_package / "__init__.py").exists(), "evo/__init__.py should exist"
    
    # Check that tests directory is at root level
    tests_dir = root / "tests"
    assert tests_dir.exists(), f"tests directory should be at {tests_dir}"
    
    # Check that pyproject.toml is at root level
    pyproject = root / "pyproject.toml"
    assert pyproject.exists(), f"pyproject.toml should be at {pyproject}"
    
    # Check that main.py is at root level
    main_py = root / "main.py"
    assert main_py.exists(), f"main.py should be at {main_py}"


def test_evo_package_structure():
    """Test that evo package has expected modules."""
    root = Path(__file__).parent.parent
    evo_package = root / "evo"
    
    expected_modules = [
        "action",
        "capability",
        "decision",
        "exploration",
        "feedback",
        "goal",
        "handler",
        "integrative_core",
        "memory",
        "metacognition",
        "perception",
        "safety",
    ]
    
    for module in expected_modules:
        module_path = evo_package / module
        assert module_path.exists(), f"evo/{module} should exist"
        assert (module_path / "__init__.py").exists(), f"evo/{module}/__init__.py should exist"


def test_imports_work_correctly():
    """Test that imports work correctly after refactoring."""
    try:
        from evo.main import EvoSystem, create_evo_system, main
        assert EvoSystem is not None
        assert create_evo_system is not None
        assert main is not None
    except ImportError as e:
        pytest.fail(f"Failed to import from evo.main: {e}")
    
    try:
        from evo.perception import PerceptionGateway
        from evo.decision import DecisionEngine
        from evo.goal import GoalEngine
        from evo.capability import CapabilityRegistry
        from evo.action import ActionLayer
        from evo.memory import MemorySystem
        from evo.metacognition import MetacognitionLayer
        from evo.exploration import ExplorationEngine
        from evo.safety import SafetyLayer
        from evo.feedback import FeedbackLoop
        from evo.handler import UserHandler, SelfHandler
        from evo.integrative_core import IntegrativeCore
    except ImportError as e:
        pytest.fail(f"Failed to import evo modules: {e}")


def test_main_py_wrapper():
    """Test that main.py wrapper works correctly."""
    root = Path(__file__).parent.parent
    main_py = root / "main.py"
    
    content = main_py.read_text()
    
    # Check that main.py is a simple wrapper (no sys.path manipulation needed)
    assert "from evo.main import main" in content or "from evo import" in content


def test_pyproject_configuration():
    """Test that pyproject.toml has correct configuration."""
    root = Path(__file__).parent.parent
    pyproject = root / "pyproject.toml"
    
    content = pyproject.read_text()
    
    # Check pythonpath - should not include "src" anymore
    assert 'pythonpath = [""]' in content or 'pythonpath = ["."]' in content or 'pythonpath' not in content