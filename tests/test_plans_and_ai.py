import json
import pytest

from backend.utils.ai_integration import (
    generate_plan
)
from backend.routes.plans import _parse_plan_content_field, _plan_to_response
from backend.utils.mock_data import get_mock_plan
from backend.models import Plan, db


#  AI INTEGRATION TESTS

def test_parse_plan_content_field_dict():
    data = {"a": 1}
    assert _parse_plan_content_field(data) == data


def test_parse_plan_content_field_json_string():
    s = '{"x": 123}'
    assert _parse_plan_content_field(s) == {"x": 123}


def test_parse_plan_content_field_invalid_json():
    s = "{invalid-json}"
    assert _parse_plan_content_field(s) == s


class DummyPlan:
    def __init__(self):
        self.content = '{"days":[{"day":1}]}'
        self.plan_type = "workout"

    def to_dict(self):
        return {"content": self.content, "plan_type": self.plan_type}


def test_plan_to_response_parses_content():
    plan = DummyPlan()
    out = _plan_to_response(plan)
    assert isinstance(out["content"], dict)
    assert out["content"]["days"][0]["day"] == 1


def test_generate_plan_returns_mock_on_failure(monkeypatch):

    monkeypatch.setattr("backend.utils.ai_integration.client", None)

    user_data = {
        "age": 30,
        "weight_kg": 80,
        "height_cm": 180,
        "goal": "muscle gain",
        "fitness_level": "beginner",
        "weekly_workouts": 4,
        "dietary_restrictions": "none",
    }

    result = generate_plan(user_data, "workout")

    assert result["error"] is not None
    parsed = json.loads(result["plan_content_string"])
    assert parsed == get_mock_plan("workout")


#  ROUTE TESTS

def test_get_latest_returns_mock_when_empty(client, auth_header):
    res = client.get("/api/plans/latest", headers=auth_header)
    assert res.status_code == 200

    data = res.get_json()
    assert "plans" in data
    assert len(data["plans"]) == 2  # workout + diet


def test_get_latest_returns_real_plans(client, auth_header, test_user):
    plan = Plan(
        user_id=test_user.id,
        plan_type="workout",
        content=json.dumps({"days": [{"day": 1}]}),
    )
    db.session.add(plan)
    db.session.commit()

    res = client.get("/api/plans/latest", headers=auth_header)
    assert res.status_code == 200

    data = res.get_json()
    assert data["plans"][0]["content"]["days"][0]["day"] == 1


def test_toggle_workout_day(client, auth_header, test_user):
    plan = Plan(
        user_id=test_user.id,
        plan_type="workout",
        content=json.dumps({"days": [{"day": 1, "completed": False}]}),
    )
    db.session.add(plan)
    db.session.commit()

    payload = {"type": "workout_day", "day": 1}
    res = client.patch(f"/api/plans/{plan.id}/toggle", json=payload, headers=auth_header)
    assert res.status_code == 200

    updated = res.get_json()["plan"]["content"]
    assert updated["days"][0]["completed"] is True


def test_toggle_diet_meal(client, auth_header, test_user):
    plan = Plan(
        user_id=test_user.id,
        plan_type="diet",
        content=json.dumps({"meals": [{"day": 1, "breakfast": "eggs"}]}),
    )
    db.session.add(plan)
    db.session.commit()

    payload = {"type": "diet_meal", "day": 1, "meal": "breakfast"}
    res = client.patch(f"/api/plans/{plan.id}/toggle", json=payload, headers=auth_header)
    assert res.status_code == 200

    updated = res.get_json()["plan"]["content"]
    assert updated["meals"][0]["breakfast_completed"] is True


def test_toggle_nonexistent_plan(client, auth_header):
    res = client.patch(
        "/api/plans/999/toggle",
        json={"type": "workout_day", "day": 1},
        headers=auth_header,
    )
    assert res.status_code == 404
