import pytest
from backend.utils.mock_data import get_mock_plan

def test_get_mock_plan_workout():
    plan = get_mock_plan("workout")
    assert plan["plan_name"] == "AI Full Body Workout"
    assert plan["duration_days"] == 7
    assert len(plan["exercises"]) == 7
    assert plan["exercises"][0]["activity"] == "Push-ups"
    assert plan["exercises"][0]["sets"] == 3
    assert plan["exercises"][0]["reps"] == 15

def test_get_mock_plan_diet():
    plan = get_mock_plan("diet")
    assert plan["plan_name"] == "AI Healthy Meal Plan"
    assert plan["duration_days"] == 7
    assert "meals" in plan
    assert plan["meals"][0]["breakfast"] == "Oatmeal + Banana"

def test_get_mock_plan_generic():
    plan = get_mock_plan("unknown_type")
    assert plan["plan_name"] == "Generic Fitness Plan"
    assert plan["duration_days"] == 7
    assert "message" in plan
