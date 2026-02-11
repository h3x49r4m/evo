"""Tests for Goal Engine (TDD Red Phase)."""

import pytest
from evo.goal import GoalEngine


class TestExternalGoals:
    """Tests for external goals from user."""
    
    def test_add_external_goal_adds_to_registry(self):
        """Given goal engine, When adding external goal, Then it is retrievable."""
        engine = GoalEngine()
        engine.add_external_goal("write_code", "Write Python code")
        assert "write_code" in engine.list_external_goals()
    
    def test_external_goals_override_internal(self):
        """Given goal engine with both goal types, When evaluating, Then external wins."""
        engine = GoalEngine()
        engine.add_external_goal("user_task", "Complete user task")
        engine.add_internal_goal("explore", "Explore capabilities")
        prioritized = engine.prioritize_goals()
        assert prioritized[0]["source"] == "external"
    
    def test_remove_external_goal_removes_from_registry(self):
        """Given goal engine with external goal, When removing, Then it is removed."""
        engine = GoalEngine()
        engine.add_external_goal("temp_goal", "Temporary")
        engine.remove_external_goal("temp_goal")
        assert "temp_goal" not in engine.list_external_goals()


class TestInternalGoals:
    """Tests for internal self-generated goals."""
    
    def test_curiosity_drive_generates_goal(self):
        """Given goal engine, When curiosity drive activated, Then generates learning goal."""
        engine = GoalEngine()
        goal = engine.generate_curiosity_goal()
        assert goal["drive"] == "curiosity"
        assert "reduce_uncertainty" in goal["description"]
    
    def test_competence_drive_generates_goal(self):
        """Given goal engine, When competence drive activated, Then generates improvement goal."""
        engine = GoalEngine()
        goal = engine.generate_competence_goal()
        assert goal["drive"] == "competence"
        assert "improve_capability" in goal["description"]
    
    def test_autonomy_drive_generates_goal(self):
        """Given goal engine, When autonomy drive activated, Then generates independence goal."""
        engine = GoalEngine()
        goal = engine.generate_autonomy_goal()
        assert goal["drive"] == "autonomy"
        assert "independent_action" in goal["description"]
    
    def test_meaning_drive_generates_goal(self):
        """Given goal engine, When meaning drive activated, Then generates purpose goal."""
        engine = GoalEngine()
        goal = engine.generate_meaning_goal()
        assert goal["drive"] == "meaning"
        assert "purpose" in goal["description"]
    
    def test_add_internal_goal_adds_to_registry(self):
        """Given goal engine, When adding internal goal, Then it is retrievable."""
        engine = GoalEngine()
        engine.add_internal_goal("self_improve", "Improve myself")
        assert "self_improve" in engine.list_internal_goals()
    
    def test_add_internal_goal_with_invalid_name_raises_value_error(self):
        """Given goal engine, When adding internal goal with invalid name, Then raises ValueError (line 21)."""
        engine = GoalEngine()
        with pytest.raises(ValueError, match="Invalid goal name"):
            engine.add_internal_goal("", "Empty name")
    
    def test_list_internal_goals_returns_all_internal_goal_names(self):
        """Given goal engine with internal goals, When listing, Then returns all names (line 38)."""
        engine = GoalEngine()
        engine.add_internal_goal("goal1", "Goal 1")
        engine.add_internal_goal("goal2", "Goal 2")
        engine.add_internal_goal("goal3", "Goal 3")
        
        goals = engine.list_internal_goals()
        assert len(goals) == 3
        assert "goal1" in goals
        assert "goal2" in goals
        assert "goal3" in goals
    
    def test_list_internal_goals_returns_empty_when_no_goals(self):
        """Given goal engine without internal goals, When listing, Then returns empty list."""
        engine = GoalEngine()
        goals = engine.list_internal_goals()
        assert goals == []


class TestGoalEvaluation:
    """Tests for goal evaluation and scoring."""
    
    def test_evaluate_goal_returns_feasibility_score(self):
        """Given goal engine, When evaluating goal, Then returns feasibility score."""
        engine = GoalEngine()
        goal = {"description": "simple_task", "requirements": []}
        result = engine.evaluate_goal(goal)
        assert "feasibility" in result
        assert 0 <= result["feasibility"] <= 1
    
    def test_evaluate_goal_returns_learning_potential(self):
        """Given goal engine, When evaluating goal, Then returns learning potential."""
        engine = GoalEngine()
        goal = {"description": "learn_python", "complexity": "high"}
        result = engine.evaluate_goal(goal)
        assert "learning_potential" in result
    
    def test_evaluate_goal_returns_drive_alignment(self):
        """Given goal engine, When evaluating goal, Then returns drive alignment."""
        engine = GoalEngine()
        goal = {"drive": "curiosity"}
        result = engine.evaluate_goal(goal)
        assert "drive_alignment" in result


class TestGoalEngineIntegration:
    """Integration tests for goal engine."""
    
    def test_full_workflow_add_evaluate_and_prioritize(self):
        """Given goal engine, When processing through full workflow, Then correctly processes."""
        engine = GoalEngine()
        # Add goals
        engine.add_external_goal("user_task", "Complete user task")
        engine.add_internal_goal("learn", "Learn new skill")
        # Evaluate
        external = engine.list_external_goals()[0]
        evaluated = engine.evaluate_goal({"name": external, "source": "external"})
        # Prioritize
        prioritized = engine.prioritize_goals()
        # Verify
        assert len(prioritized) >= 1
        assert prioritized[0]["source"] == "external"