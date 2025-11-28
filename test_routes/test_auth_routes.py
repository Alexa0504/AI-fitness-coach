from unittest.mock import patch

# ------------------------------
#  REGISTER ENDPOINT TESZTEK
# ------------------------------

def test_register_user_success(client):
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
    response = client.post('/api/auth/register', json={})
    assert response.status_code == 400
    assert "Missing required fields" in response.get_json()["message"]

def test_register_duplicate_email(client):
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

def test_register_db_commit_exception(client, monkeypatch):
    def fake_commit():
        raise Exception("DB commit error")
    monkeypatch.setattr("backend.models.db.session.commit", fake_commit)

    response = client.post('/api/auth/register', json={
        "username": "dberror",
        "email": "dberror@example.com",
        "password": "secret123"
    })
    assert response.status_code == 500
    assert "internal error" in response.get_json()["message"].lower()

# ------------------------------
#  LOGIN ENDPOINT TESZTEK
# ------------------------------

def test_login_success(client):
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
    response = client.post('/api/auth/login', json={
        "identifier": "notexists@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert "Invalid" in response.get_json()["message"]

def test_login_missing_password(client):
    response = client.post('/api/auth/login', json={
        "identifier": "anyuser@example.com"
    })
    assert response.status_code == 400
    assert "Missing username/email or password" in response.get_json()["message"]

def test_login_with_username(client):
    client.post('/api/auth/register', json={
        "username": "userwithname",
        "email": "userwithname@example.com",
        "password": "secret123"
    })
    response = client.post('/api/auth/login', json={
        "identifier": "userwithname",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()

# ------------------------------
#  LOGOUT ENDPOINT TESZTEK
# ------------------------------

def test_logout_success(client):
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
    response = client.post('/api/auth/logout')
    data = response.get_json()
    assert response.status_code == 401
    assert "Token is missing" in data["message"]

def test_logout_blacklist_failure(client):
    register_response = client.post('/api/auth/register', json={
        "username": "faillogout",
        "email": "faillogout@example.com",
        "password": "secret123"
    })
    token = register_response.get_json()["token"]

    with patch('backend.routes.auth.add_token_to_blacklist', return_value=False):
        response = client.post('/api/auth/logout', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 500
        assert "Failed to blacklist token" in response.get_json()["message"]
