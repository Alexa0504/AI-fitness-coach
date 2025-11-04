import pytest
from backend.models import User

@pytest.fixture
def client(app):
    """Provides a Flask test client"""
    return app.test_client()


# ------------------------------
#  REGISTER ENDPOINT TESTS
# ------------------------------

def test_register_user_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        "username": "unituser",
        "email": "unit@example.com",
        "password": "secret123"
    })
    assert response.status_code == 201

    data = response.get_json()
    assert data["message"] == "Registration successful."
    assert "token" in data
    assert data["user"]["username"] == "unituser"


def test_register_missing_fields(client):
    """Test registration with missing fields"""
    response = client.post('/api/auth/register', json={})
    assert response.status_code == 400
    assert "Missing required fields" in response.get_json()["message"]


def test_register_duplicate_email(client):
    """Test registration with duplicate email"""

    client.post('/api/auth/register', json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "pass123"
    })


    response = client.post('/api/auth/register', json={
        "username": "anotheruser",
        "email": "dup@example.com",
        "password": "pass456"
    })

    assert response.status_code == 409
    assert "already registered" in response.get_json()["message"]


# ------------------------------
#  LOGIN ENDPOINT TESTS
# ------------------------------

def test_login_success(client):
    """Test successful login with valid credentials"""
    client.post('/api/auth/register', json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "secret123"
    })

    response = client.post('/api/auth/login', json={
        "identifier": "login@example.com",
        "password": "secret123"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful."
    assert "token" in data


def test_login_invalid_credentials(client):
    """Test login with invalid username or password"""
    response = client.post('/api/auth/login', json={
        "identifier": "notexists@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert "Invalid" in response.get_json()["message"]


# ------------------------------
#  LOGOUT ENDPOINT TESTS
# ------------------------------

def test_logout_success(client):
    """Test logout with valid token (should be blacklisted)"""

    register_response = client.post('/api/auth/register', json={
        "username": "logoutuser",
        "email": "logout@example.com",
        "password": "secret123"
    })
    token = register_response.get_json()["token"]


    response = client.post(
        '/api/auth/logout',
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Logout successful."


def test_logout_missing_token(client):
    """Test logout without providing a token"""
    response = client.post('/api/auth/logout')
    data = response.get_json()
    assert response.status_code == 401
    assert "Token is missing" in data["message"]
