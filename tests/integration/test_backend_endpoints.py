import pytest
from backend.models import db, User
from backend.utils.token_blacklist import is_token_blacklisted
from backend.utils.security_utils import hash_password, generate_auth_token
import json

# ---------------------------
# AUTH INTEGRATION TESTS
# ---------------------------
def test_register_and_login(client):
    # REGISTER
    response = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "pass123"
    })
    assert response.status_code == 201
    assert "token" in response.get_json()

    # LOGIN
    response = client.post("/api/auth/login", json={
        "email": "alice@test.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_register_duplicate(client):
    client.post("/api/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "pass123"
    })
    response = client.post("/api/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "pass123"
    })
    assert response.status_code == 409


def test_login_invalid_credentials(client):
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_logout_blacklist(client, auth_header):
    response = client.post("/api/auth/logout", headers=auth_header)
    assert response.status_code == 200
    token = auth_header["Authorization"].split(" ")[1]
    assert is_token_blacklisted(token)


# ---------------------------
# GOALS INTEGRATION TESTS
# ---------------------------
def test_create_get_update_delete_goal(client, auth_header):
    # CREATE
    response = client.post("/api/goals/", headers=auth_header, json={
        "goal_type": "weight_loss",
        "target_value": 5,
        "unit": "kg"
    })
    goal_id = response.get_json()["goal"]["id"]
    assert response.status_code == 201

    # GET
    response = client.get("/api/goals/", headers=auth_header)
    assert response.status_code == 200
    assert any(g["id"] == goal_id for g in response.get_json())

    # UPDATE
    response = client.put(f"/api/goals/{goal_id}", headers=auth_header, json={"target_value": 6})
    assert response.status_code == 200
    assert response.get_json()["goal"]["target_value"] == 6

    # DELETE
    response = client.delete(f"/api/goals/{goal_id}", headers=auth_header)
    assert response.status_code == 200


def test_create_get_toggle_weekly_goal(client, auth_header):
    # CREATE
    response = client.post("/api/goals/weekly", headers=auth_header, json={"goal_name": "3x workout"})
    assert response.status_code == 201
    goal = response.get_json()["goal"]
    goal_id = goal["id"]

    # GET
    response = client.get("/api/goals/weekly", headers=auth_header)
    assert response.status_code == 200
    assert any(g["id"] == goal_id for g in response.get_json())

    # TOGGLE
    response = client.patch(f"/api/goals/weekly/{goal_id}/toggle", headers=auth_header)
    assert response.status_code == 200
    toggled_goal = response.get_json()["goal"]
    assert toggled_goal["is_completed"] is True

    # TOGGLE BACK
    response = client.patch(f"/api/goals/weekly/{goal_id}/toggle", headers=auth_header)
    assert response.status_code == 200
    toggled_goal = response.get_json()["goal"]
    assert toggled_goal["is_completed"] is False


# ---------------------------
# PLANS INTEGRATION TESTS
# ---------------------------
def test_create_get_update_delete_plan(client, auth_header):
    # CREATE
    response = client.post("/api/plans/", headers=auth_header, json={"plan_type": "workout"})
    plan_id = response.get_json()["plan"]["id"]
    plan_content = response.get_json()["plan"]["content"]

    if "days" not in plan_content or not plan_content["days"]:
        plan_content["days"] = [{"day": 1, "completed": False}]
        client.put(f"/api/plans/{plan_id}", headers=auth_header, json={"content": plan_content})

    assert response.status_code == 201

    # GET ALL
    response = client.get("/api/plans/", headers=auth_header)
    assert response.status_code == 200
    assert any(p["id"] == plan_id for p in response.get_json())

    # GET SINGLE
    response = client.get(f"/api/plans/{plan_id}", headers=auth_header)
    assert response.status_code == 200

    # UPDATE
    response = client.put(f"/api/plans/{plan_id}", headers=auth_header, json={"plan_type": "diet"})
    assert response.status_code == 200
    assert response.get_json()["plan"]["plan_type"] == "diet"

    # DELETE
    response = client.delete(f"/api/plans/{plan_id}", headers=auth_header)
    assert response.status_code == 200


def test_toggle_plan_invalid_type(client, auth_header):
    response = client.patch("/api/plans/9999/toggle", headers=auth_header, json={"type": "invalid_type"})
    assert response.status_code in (400, 404)


# ---------------------------
# USERS / PROFILE INTEGRATION TESTS
# ---------------------------
def test_update_user_profile_invalid_age(client, auth_header):
    response = client.put("/api/users/profile", headers=auth_header, json={"age": "notanumber"})
    assert response.status_code == 400

def test_update_user_profile_valid(client, auth_header):
    response = client.put("/api/users/profile", headers=auth_header, json={
        "height_cm": 180,
        "weight_kg": 75,
        "target_weight_kg": 70,
        "gender": "male",
        "age": 30
    })
    assert response.status_code == 200
    data = response.get_json()["user"]
    assert data["height_cm"] == 180
    assert data["weight_kg"] == 75
    assert data["target_weight_kg"] == 70
    assert data["gender"] == "male"
    assert data["age"] == 30


# ---------------------------
# TOKEN REQUIRED DECORATOR TEST
# ---------------------------
def test_protected_route_requires_token(client):
    response = client.get("/api/goals/")
    assert response.status_code == 401
    assert "Token is missing" in response.get_json()["message"]


# ---------------------------
# FULL WORKFLOW INTEGRATION TEST
# ---------------------------
def test_full_user_workflow(client):
    # Register
    resp = client.post("/api/auth/register", json={
        "username": "charlie",
        "email": "charlie@test.com",
        "password": "pass123"
    })
    token = resp.get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create goal
    resp = client.post("/api/goals/", headers=headers, json={"goal_type": "strength", "target_value": 10})
    assert resp.status_code == 201
    goal_id = resp.get_json()["goal"]["id"]

    # Create weekly goal
    resp = client.post("/api/goals/weekly", headers=headers, json={"goal_name": "5x workout"})
    assert resp.status_code == 201
    weekly_goal_id = resp.get_json()["goal"]["id"]

    # Create plan
    resp = client.post("/api/plans/", headers=headers, json={"plan_type": "workout"})
    assert resp.status_code == 201
    plan_id = resp.get_json()["plan"]["id"]

    # Ensure plan has at least 1 day
    plan_content = resp.get_json()["plan"]["content"]

    if "days" not in plan_content or not plan_content["days"]:
        plan_content["days"] = [{"day": 1, "completed": False}]
        client.put(f"/api/plans/{plan_id}", headers=headers, json={"content": plan_content})

    # Toggle plan day
    resp = client.patch(f"/api/plans/{plan_id}/toggle", headers=headers, json={"type": "workout_day", "day": 1})
    assert resp.status_code == 200

    # Update profile
    resp = client.put("/api/users/profile", headers=headers, json={"height_cm": 180, "weight_kg": 75})
    assert resp.status_code == 200

    # Logout
    resp = client.post("/api/auth/logout", headers=headers)
    assert resp.status_code == 200
    assert is_token_blacklisted(token)
