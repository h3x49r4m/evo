"""Tests for type definitions."""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.types import (
    ToolData,
    SkillData,
    GoalData,
    ObservationData,
    ActionStep,
    ExecutionPlan,
    ContextData,
    DecisionData,
    ExperienceData,
    SelfModel,
    LearnedStrategy,
    PatternData,
    PerceptionData,
    SafetyCheckResult,
    WorkingMemoryValue,
    SemanticMemoryValue,
    BeliefValue,
    KnowledgeValue,
)


def test_tool_data_typed_dict():
    """Test ToolData TypedDict structure."""
    tool: ToolData = {
        "description": "A test tool",
        "callable": lambda: "result"
    }
    assert tool["description"] == "A test tool"
    assert callable(tool["callable"])


def test_skill_data_typed_dict():
    """Test SkillData TypedDict structure."""
    skill: SkillData = {
        "description": "A test skill",
        "level": 0.75
    }
    assert skill["description"] == "A test skill"
    assert skill["level"] == 0.75


def test_goal_data_typed_dict():
    """Test GoalData TypedDict structure (all fields optional)."""
    # Minimal goal
    goal1: GoalData = {"goal": "test goal"}
    assert goal1["goal"] == "test goal"
    
    # Full goal
    goal2: GoalData = {
        "goal": "complete goal",
        "priority": 1,
        "context": {"key": "value"},
        "tools": ["tool1", "tool2"],
        "deadline": "2025-12-31"
    }
    assert goal2["priority"] == 1
    assert len(goal2["tools"]) == 2


def test_observation_data_typed_dict():
    """Test ObservationData TypedDict structure."""
    obs: ObservationData = {
        "action": "test_action",
        "result": "success",
        "output": "completed",
        "timestamp": "2025-01-01"
    }
    assert obs["action"] == "test_action"
    assert obs["result"] == "success"


def test_action_step_typed_dict():
    """Test ActionStep TypedDict structure."""
    step: ActionStep = {
        "tool": "search",
        "action": "execute"
    }
    assert step["tool"] == "search"


def test_execution_plan_typed_dict():
    """Test ExecutionPlan TypedDict structure."""
    plan: ExecutionPlan = {
        "steps": [
            {"tool": "tool1", "action": "execute"},
            {"tool": "tool2", "action": "execute"}
        ],
        "goal": {"goal": "test goal"}
    }
    assert len(plan["steps"]) == 2


def test_context_data_typed_dict():
    """Test ContextData TypedDict structure."""
    context: ContextData = {
        "user_input": True,
        "internal_goals": True,
        "safety_alert": False,
        "data": {"key": "value"}
    }
    assert context["user_input"] is True


def test_decision_data_typed_dict():
    """Test DecisionData TypedDict structure."""
    decision: DecisionData = {
        "handler": "user_handler",
        "mode": "responsive",
        "data": {"input": "test"}
    }
    assert decision["handler"] == "user_handler"
    assert decision["mode"] == "responsive"


def test_experience_data_typed_dict():
    """Test ExperienceData TypedDict structure."""
    exp: ExperienceData = {
        "action": "test_action",
        "result": {"status": "success"},
        "outcome": "completed",
        "strategy": "test_strategy",
        "timestamp": "2025-01-01"
    }
    assert exp["action"] == "test_action"
    assert exp["outcome"] == "completed"


def test_self_model_typed_dict():
    """Test SelfModel TypedDict structure."""
    model: SelfModel = {
        "capabilities": {"skill1": 0.8, "skill2": 0.6},
        "beliefs": {"fact": "true"},
        "goal_strategy": "default"
    }
    assert model["capabilities"]["skill1"] == 0.8
    assert model["goal_strategy"] == "default"


def test_learned_strategy_typed_dict():
    """Test LearnedStrategy TypedDict structure."""
    strategy: LearnedStrategy = {
        "outcome": "success",
        "strategy": "approach1",
        "learned_at": "2025-01-01"
    }
    assert strategy["outcome"] == "success"


def test_pattern_data_typed_dict():
    """Test PatternData TypedDict structure."""
    pattern: PatternData = {
        "action": "search",
        "frequency": 5
    }
    assert pattern["frequency"] == 5


def test_perception_data_typed_dict():
    """Test PerceptionData TypedDict structure."""
    perception: PerceptionData = {
        "type": "user_input",
        "content": "hello",
        "priority": 1,
        "timestamp": "2025-01-01"
    }
    assert perception["type"] == "user_input"
    assert perception["priority"] == 1


def test_safety_check_result_typed_dict():
    """Test SafetyCheckResult TypedDict structure."""
    result: SafetyCheckResult = {
        "safe": True,
        "reason": "All checks passed",
        "action": "proceed"
    }
    assert result["safe"] is True


def test_working_memory_value_type():
    """Test WorkingMemoryValue type alias accepts various types."""
    # String
    val1: WorkingMemoryValue = "test"
    assert val1 == "test"
    
    # Integer
    val2: WorkingMemoryValue = 42
    assert val2 == 42
    
    # Float
    val3: WorkingMemoryValue = 3.14
    assert val3 == 3.14
    
    # Boolean
    val4: WorkingMemoryValue = True
    assert val4 is True
    
    # Dict
    val5: WorkingMemoryValue = {"key": "value"}
    assert val5["key"] == "value"
    
    # List
    val6: WorkingMemoryValue = [1, 2, 3]
    assert len(val6) == 3
    
    # None
    val7: WorkingMemoryValue = None
    assert val7 is None


def test_semantic_memory_value_type():
    """Test SemanticMemoryValue type alias (no None)."""
    val1: SemanticMemoryValue = "test"
    val2: SemanticMemoryValue = 42
    val3: SemanticMemoryValue = {"key": "value"}
    assert val1 == "test"


def test_belief_value_type():
    """Test BeliefValue type alias."""
    belief1: BeliefValue = "fact"
    belief2: BeliefValue = 0.5
    belief3: BeliefValue = None
    assert belief1 == "fact"
    assert belief3 is None


def test_knowledge_value_type():
    """Test KnowledgeValue type alias."""
    knowledge1: KnowledgeValue = "fact"
    knowledge2: KnowledgeValue = {"key": "value"}
    knowledge3: KnowledgeValue = None
    assert knowledge1 == "fact"
    assert knowledge3 is None