import uuid
import pytest
from backend.models import User, Plan
from backend.utils.security_utils import generate_auth_token, hash_password
from backend.models import db

@pytest.fixture
def auth_header(app):
    """Create a user with unique username and email for each test and return auth header"""
    unique_id = uuid.uuid4().hex
    user = User(
        username=f"planuser_{unique_id}",
        email=f"user_{unique_id}@example.com",
        password_hash=hash_password("pw")
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        token = generate_auth_token(str(user.id))
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_plan(app, auth_header, client):
    """Helper fixture to create a plan and return its ID"""
    response = client.post('/api/plans/', json={"plan_type": "workout"}, headers=auth_header)
    return response.get_json()["plan"]["id"]

# ------------------- TESTS -------------------

def test_create_plan_success(client, auth_header):
    response = client.post('/api/plans/', json={"plan_type": "workout"}, headers=auth_header)
    assert response.status_code == 201
    data = response.get_json()
    assert "plan" in data
    assert "New plan created successfully" in data["message"]

def test_get_user_plans(client, auth_header):
    client.post('/api/plans/', json={"plan_type": "nutrition"}, headers=auth_header)
    response = client.get('/api/plans/', headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_single_plan(client, auth_header, create_plan):
    plan_id = create_plan
    response = client.get(f'/api/plans/{plan_id}', headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == plan_id

def test_get_single_plan_not_found(client, auth_header):
    response = client.get('/api/plans/999999', headers=auth_header)
    assert response.status_code == 404
    assert "Plan not found" in response.get_json()["message"]

def test_update_plan_success(client, auth_header, create_plan):
    plan_id = create_plan
    new_content = "Updated content"
    response = client.put(f'/api/plans/{plan_id}', json={"content": new_content}, headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["plan"]["content"] == new_content
    assert "Plan updated successfully" in data["message"]

def test_update_plan_not_found(client, auth_header):
    response = client.put('/api/plans/999999', json={"content": "x"}, headers=auth_header)
    assert response.status_code == 404
    assert "Plan not found" in response.get_json()["message"]

def test_delete_plan_success(client, auth_header, create_plan):
    plan_id = create_plan
    response = client.delete(f'/api/plans/{plan_id}', headers=auth_header)
    assert response.status_code == 200
    assert "Plan deleted successfully" in response.get_json()["message"]

def test_delete_plan_not_found(client, auth_header):
    response = client.delete('/api/plans/999999', headers=auth_header)
    assert response.status_code == 404
    assert "Plan not found" in response.get_json()["message"]

def test_create_plan_invalid_start_date(client, auth_header):
    response = client.post('/api/plans/', json={"plan_type": "workout", "start_date": "2025-99-99"}, headers=auth_header)
    assert response.status_code == 400
    assert "Invalid start_date format" in response.get_json()["message"]

def test_update_plan_invalid_start_date(client, auth_header, create_plan):
    plan_id = create_plan
    response = client.put(f'/api/plans/{plan_id}', json={"start_date": "abcd"}, headers=auth_header)
    assert response.status_code == 400
    assert "Invalid start_date format" in response.get_json()["message"]

def test_update_plan_type_changes_score(client, auth_header, create_plan):
    plan_id = create_plan
    old_response = client.get(f'/api/plans/{plan_id}', headers=auth_header)
    old_score = old_response.get_json()["score"]
    response = client.put(f'/api/plans/{plan_id}', json={"plan_type": "nutrition"}, headers=auth_header)
    assert response.status_code == 200
    new_score = response.get_json()["plan"]["score"]
    assert new_score != old_score
