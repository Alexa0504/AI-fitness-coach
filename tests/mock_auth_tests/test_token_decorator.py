import os
import pytest
from flask import Flask, jsonify
from backend.app import create_app
from backend.models import db, User
from backend.utils.auth_decorator import token_required

os.environ["TESTING"] = "1"

# ---------------------------
# APP FIXTURE
# ---------------------------
@pytest.fixture(scope="session")
def app():
    """Create Flask app with PostgreSQL test database"""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_DATABASE_URL"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })


    @app.route("/protected")
    @token_required
    def protected_route(current_user):
        return jsonify({"message": f"Hello {current_user.username}"}), 200

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# ---------------------------
# CLIENT FIXTURE
# ---------------------------
@pytest.fixture
def client(app):
    """Provide a Flask test client"""
    return app.test_client()

# ---------------------------
# SESSION FIXTURE
# ---------------------------
@pytest.fixture(scope="function")
def session(app):
    """Provide an isolated database session per test"""
    with app.app_context():
        yield db.session
        db.session.rollback()

# ---------------------------
# TOKEN DECORATOR TESTS
# ---------------------------
def test_token_missing(client):
    response = client.get("/protected")
    assert response.status_code == 401
    assert "Token is missing" in response.get_json()["message"]

def test_token_blacklisted(client, monkeypatch):
    monkeypatch.setattr("backend.utils.auth_decorator.is_token_blacklisted", lambda t: True)
    response = client.get("/protected", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 401
    assert "revoked" in response.get_json()["message"]

def test_token_invalid(client, monkeypatch):
    monkeypatch.setattr("backend.utils.auth_decorator.is_token_blacklisted", lambda t: False)
    monkeypatch.setattr("backend.utils.auth_decorator.decode_auth_token", lambda t: None)
    response = client.get("/protected", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 401
    assert "invalid or expired" in response.get_json()["message"]

def test_user_not_found(client, monkeypatch):
    monkeypatch.setattr("backend.utils.auth_decorator.is_token_blacklisted", lambda t: False)
    monkeypatch.setattr("backend.utils.auth_decorator.decode_auth_token", lambda t: 999)
    response = client.get("/protected", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 404
    assert "User not found" in response.get_json()["message"]

def test_successful_access(client, monkeypatch):
    with client.application.app_context():
        user = User(id=1, username="testuser", email="test@test.com", password_hash="dummyhash")
        db.session.add(user)
        db.session.commit()

    monkeypatch.setattr("backend.utils.auth_decorator.is_token_blacklisted", lambda t: False)
    monkeypatch.setattr("backend.utils.auth_decorator.decode_auth_token", lambda t: 1)

    response = client.get("/protected", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 200
    assert "Hello testuser" in response.get_json()["message"]
