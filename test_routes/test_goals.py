import uuid
import pytest
from backend.models import Goal, User
from backend.utils.security_utils import generate_auth_token, hash_password

@pytest.fixture
def auth_header(session):
    """Create a user with unique username and email for each test and return auth header"""
    unique_id = uuid.uuid4().hex
    user = User(
        username=f"goaluser_{unique_id}",
        email=f"user_{unique_id}@example.com",
        password_hash=hash_password("pw")
    )
    session.add(user)
    session.commit()

    token = generate_auth_token(str(user.id))
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def client(app):
    return app.test_client()


# -----------------------
# CREATE
# -----------------------
def test_create_goal_success(client, auth_header):
    response = client.post('/api/goals/', json={
        "goal_type": "weight_loss",
        "target_value": 5,
        "unit": "kg"
    }, headers=auth_header)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Goal created"
    assert response.get_json()["goal"]["goal_type"] == "weight_loss"


def test_create_goal_missing_field(client, auth_header):
    response = client.post('/api/goals/', json={}, headers=auth_header)
    assert response.status_code == 400
    assert "goal_type is required" in response.get_json()["message"]


# -----------------------
# READ
# -----------------------
def test_get_goals(client, auth_header):

    client.post('/api/goals/', json={
        "goal_type": "muscle_gain",
        "target_value": 3,
        "unit": "kg"
    }, headers=auth_header)

    response = client.get('/api/goals/', headers=auth_header)
    assert response.status_code == 200
    goals = response.get_json()
    assert isinstance(goals, list)
    assert any(g["goal_type"] == "muscle_gain" for g in goals)


# -----------------------
# UPDATE
# -----------------------
def test_update_goal_success(client, auth_header):

    create_resp = client.post('/api/goals/', json={
        "goal_type": "weight_loss",
        "target_value": 5,
        "unit": "kg"
    }, headers=auth_header)
    goal_id = create_resp.get_json()["goal"]["id"]


    update_resp = client.put(f'/api/goals/{goal_id}', json={
        "goal_type": "muscle_gain",
        "target_value": 6
    }, headers=auth_header)

    assert update_resp.status_code == 200
    data = update_resp.get_json()
    assert data["message"] == "Goal updated successfully"
    assert data["goal"]["goal_type"] == "muscle_gain"
    assert data["goal"]["target_value"] == 6


def test_update_goal_not_found(client, auth_header):
    response = client.put('/api/goals/9999', json={
        "goal_type": "muscle_gain"
    }, headers=auth_header)
    assert response.status_code == 404
    assert response.get_json()["message"] == "Goal not found"


# -----------------------
# DELETE
# -----------------------
def test_delete_goal_success(client, auth_header):

    create_resp = client.post('/api/goals/', json={
        "goal_type": "weight_loss",
        "target_value": 5,
        "unit": "kg"
    }, headers=auth_header)
    goal_id = create_resp.get_json()["goal"]["id"]


    delete_resp = client.delete(f'/api/goals/{goal_id}', headers=auth_header)
    assert delete_resp.status_code == 200
    assert delete_resp.get_json()["message"] == "Goal deleted successfully"


    get_resp = client.get('/api/goals/', headers=auth_header)
    assert all(g["id"] != goal_id for g in get_resp.get_json())


def test_delete_goal_not_found(client, auth_header):
    response = client.delete('/api/goals/9999', headers=auth_header)
    assert response.status_code == 404
    assert response.get_json()["message"] == "Goal not found"


# -----------------------
# AUTH EDGE CASES
# -----------------------
def test_access_without_token(client):
    response = client.get('/api/goals/')
    assert response.status_code == 401  # assuming token_required returns 401
    assert "message" in response.get_json()


def test_access_with_invalid_token(client):
    response = client.get('/api/goals/', headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert "message" in response.get_json()

# -----------------------
# WEEKLY GOALS
# -----------------------
def test_create_weekly_goal_success(client, auth_header):
    response = client.post('/api/goals/weekly', json={
        "goal_name": "Workout 3 times"
    }, headers=auth_header)

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Weekly goal created"
    assert data["goal"]["goal_name"] == "Workout 3 times"
    assert "week_start" in data["goal"]


def test_create_weekly_goal_missing_field(client, auth_header):
    response = client.post('/api/goals/weekly', json={}, headers=auth_header)

    assert response.status_code == 400
    assert "goal_name is required" in response.get_json()["message"]


def test_get_weekly_goals(client, auth_header):
    # first create
    client.post('/api/goals/weekly', json={
        "goal_name": "Run 10km"
    }, headers=auth_header)

    # then fetch
    response = client.get('/api/goals/weekly', headers=auth_header)

    assert response.status_code == 200
    goals = response.get_json()
    assert isinstance(goals, list)
    assert any(g["goal_name"] == "Run 10km" for g in goals)


def test_toggle_weekly_goal(client, auth_header):
    # create weekly goal
    create_resp = client.post('/api/goals/weekly', json={
        "goal_name": "Drink more water"
    }, headers=auth_header)

    goal_id = create_resp.get_json()["goal"]["id"]

    # toggle
    toggle_resp = client.patch(f'/api/goals/weekly/{goal_id}/toggle', headers=auth_header)
    assert toggle_resp.status_code == 200
    assert "completed" in toggle_resp.get_json()["message"].lower()

    # toggle again
    toggle_resp = client.patch(f'/api/goals/weekly/{goal_id}/toggle', headers=auth_header)
    assert toggle_resp.status_code == 200
    assert "pending" in toggle_resp.get_json()["message"].lower()


def test_toggle_weekly_goal_not_found(client, auth_header):
    response = client.patch('/api/goals/weekly/9999/toggle', headers=auth_header)
    assert response.status_code == 404
    assert response.get_json()["message"] == "Weekly goal not found"
