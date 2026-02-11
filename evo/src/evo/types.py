"""Type definitions for the evo autonomous agent system.

This module provides TypedDict classes and type aliases for commonly used
data structures throughout the evo autonomous agent system. Using strongly-typed
data structures improves code clarity, enables better IDE support, and catches
type-related errors early in development.

Common Use Cases:
    - Define input/output contracts between components
    - Document expected data structures in function signatures
    - Enable static type checking with mypy or similar tools
    - Improve code readability and maintainability

Component Interactions:
    - ActionLayer uses ExecutionPlan and GoalData for action planning
    - FeedbackLoop uses ObservationData and PatternData for learning
    - MemorySystem uses WorkingMemoryValue and SemanticMemoryValue for storage
    - MetacognitionLayer uses SelfModel and LearnedStrategy for self-reflection
    - DecisionEngine uses ContextData and DecisionData for routing

Example:
    >>> from evo.types import GoalData, ExecutionPlan, ActionStep
    >>>
    >>> # Define a goal
    >>> goal: GoalData = {
    ...     "goal": "Search for information",
    ...     "priority": 1,
    ...     "context": {"query": "AI research"},
    ...     "tools": ["search_web", "analyze_results"]
    ... }
    >>>
    >>> # Create an execution plan
    >>> plan: ExecutionPlan = {
    ...     "steps": [
    ...         {"tool": "search_web", "action": "execute"},
    ...         {"tool": "analyze_results", "action": "execute"}
    ...     ],
    ...     "goal": goal
    ... }

Type Categories:
    - TypedDict classes for structured data (e.g., GoalData, ObservationData)
    - Type aliases for simple values (e.g., WorkingMemoryValue, BeliefValue)
    - All types are designed to be compatible with mypy and other type checkers
"""

from typing import Any, Dict, List, Optional, TypedDict, Union


class ToolData(TypedDict):
    """Type definition for tool registration data."""
    description: str
    callable: Optional[Any]


class SkillData(TypedDict):
    """Type definition for skill registration data."""
    description: str
    level: float


class GoalData(TypedDict, total=False):
    """Type definition for goal data.
    
    All fields are optional to allow partial goal specifications.
    """
    goal: str
    priority: int
    context: Dict[str, Any]
    tools: List[str]
    deadline: Optional[str]


class ObservationData(TypedDict, total=False):
    """Type definition for observation data.
    
    All fields are optional to allow flexible observation formats.
    """
    action: Optional[str]
    result: Optional[Any]
    output: Optional[str]
    timestamp: Optional[str]


class ActionStep(TypedDict):
    """Type definition for a single action step in an execution plan."""
    tool: str
    action: str


class ExecutionPlan(TypedDict):
    """Type definition for an execution plan."""
    steps: List[ActionStep]
    goal: GoalData


class ContextData(TypedDict, total=False):
    """Type definition for context data passed between components.
    
    All fields are optional to allow flexible context usage.
    """
    user_input: bool
    internal_goals: bool
    safety_alert: bool
    alert_type: Optional[str]
    data: Optional[Dict[str, Any]]


class DecisionData(TypedDict):
    """Type definition for decision routing data."""
    handler: str
    mode: str
    data: Dict[str, Any]


class ExperienceData(TypedDict, total=False):
    """Type definition for experience data stored in episodic memory.
    
    All fields are optional to allow flexible experience formats.
    """
    action: str
    result: Any
    outcome: Optional[str]
    strategy: Optional[str]
    timestamp: Optional[str]


class SelfModel(TypedDict):
    """Type definition for the system's self-model."""
    capabilities: Dict[str, float]
    beliefs: Dict[str, Any]
    goal_strategy: str


class LearnedStrategy(TypedDict):
    """Type definition for a learned strategy."""
    outcome: Optional[str]
    strategy: Optional[str]
    learned_at: str


class PatternData(TypedDict):
    """Type definition for detected pattern data."""
    action: str
    frequency: int


class PerceptionData(TypedDict, total=False):
    """Type definition for perception gateway data.
    
    All fields are optional to allow flexible perception formats.
    """
    type: str
    content: str
    priority: int
    timestamp: Optional[str]


class SafetyCheckResult(TypedDict):
    """Type definition for safety check results."""
    safe: bool
    reason: Optional[str]
    action: Optional[str]


# Type aliases for common use cases
WorkingMemoryValue = Union[str, int, float, bool, Dict[str, Any], List[Any], None]
SemanticMemoryValue = Union[str, int, float, bool, Dict[str, Any], List[Any]]
BeliefValue = Union[str, int, float, bool, Dict[str, Any], List[Any], None]
KnowledgeValue = Union[str, int, float, bool, Dict[str, Any], List[Any], None]