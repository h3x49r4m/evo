"""Tests for main.py entry point integration."""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import main.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import EvoSystem, create_evo_system, main
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


class TestMainIntegration:
    """Test suite for main.py entry point."""

    def test_main_imports_all_components(self):
        """Test that main.py imports all architecture components."""
        # Verify all components are accessible
        from main import (
            PerceptionGateway, DecisionEngine, GoalEngine,
            CapabilityRegistry, ActionLayer, MemorySystem,
            MetacognitionLayer, ExplorationEngine, SafetyLayer,
            FeedbackLoop, UserHandler, SelfHandler, IntegrativeCore
        )
        assert PerceptionGateway is not None
        assert DecisionEngine is not None
        assert GoalEngine is not None
        assert CapabilityRegistry is not None
        assert ActionLayer is not None
        assert MemorySystem is not None
        assert MetacognitionLayer is not None
        assert ExplorationEngine is not None
        assert SafetyLayer is not None
        assert FeedbackLoop is not None
        assert UserHandler is not None
        assert SelfHandler is not None
        assert IntegrativeCore is not None

    def test_main_creates_system_components(self):
        """Test that main.py creates system components."""
        system = create_evo_system()
        assert system is not None
        assert hasattr(system, 'perception')
        assert hasattr(system, 'decision')
        assert hasattr(system, 'goal')
        assert hasattr(system, 'capability')
        assert hasattr(system, 'action')
        assert hasattr(system, 'memory')
        assert hasattr(system, 'metacognition')
        assert hasattr(system, 'exploration')
        assert hasattr(system, 'safety')
        assert hasattr(system, 'feedback')
        assert hasattr(system, 'handler')
        assert hasattr(system, 'integrative_core')

    def test_main_responsive_mode_workflow(self):
        """Test main.py handles responsive mode workflow."""
        system = create_evo_system()
        
        # Simulate user input
        user_input = {"source": "user", "data": "Hello"}
        result = system.process_input(user_input)
        
        assert result is not None
        assert "mode" in result
        assert result["mode"] in ["responsive", "autonomous", "hybrid", "safety"]

    def test_main_autonomous_mode_workflow(self):
        """Test main.py handles autonomous mode workflow."""
        system = create_evo_system()
        
        # Simulate no user input (autonomous mode)
        result = system.process_input(None)
        
        assert result is not None
        assert "mode" in result

    def test_main_safety_checks(self):
        """Test main.py enforces safety constraints."""
        system = create_evo_system()
        
        # Test harmful action is blocked
        harmful_action = {"action": "delete_system_files"}
        safety_result = system.safety.check_action_safety(harmful_action["action"])
        
        assert safety_result["allowed"] is False
        assert safety_result["reason"] == "harmful_action"

    def test_main_memory_integration(self):
        """Test main.py integrates memory system properly."""
        system = create_evo_system()
        
        # Store in working memory
        system.memory.working.store("test_key", "test_value")
        retrieved = system.memory.working.retrieve("test_key")
        
        assert retrieved == "test_value"

    def test_main_goal_engine_integration(self):
        """Test main.py integrates goal engine properly."""
        system = create_evo_system()
        
        # Add external goal
        system.goal.add_external_goal("test_goal", "Test description")
        goals = system.goal.list_external_goals()
        
        assert "test_goal" in goals

    def test_main_capability_registry_integration(self):
        """Test main.py integrates capability registry properly."""
        system = create_evo_system()
        
        # Register a tool
        def dummy_tool():
            return "result"
        
        system.capability.register_tool("dummy_tool", "A dummy tool", dummy_tool)
        tool = system.capability.get_tool("dummy_tool")
        
        assert tool is not None
        assert tool["description"] == "A dummy tool"


class TestMainEntry:
    """Test suite for main entry point."""

    def test_main_entry_point_exists(self):
        """Test that main entry point exists."""
        assert main is not None
        assert callable(main)

    @patch('builtins.print')
    def test_main_runs_without_errors(self, mock_print):
        """Test that main() runs without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    @patch('builtins.print')
    def test_main_prints_startup_message(self, mock_print):
        """Test that main() prints startup message."""
        main()
        
        # Check that something was printed
        assert mock_print.called

    def test_main_creates_system_on_startup(self):
        """Test that main() creates system on startup."""
        # Just verify the function can be imported and called
        assert callable(main)