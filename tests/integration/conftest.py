import uuid

import pytest
from backend.app import create_app
from backend.models import db, User
from backend.utils.security_utils import hash_password, generate_auth_token

@pytest.fixture(scope="session")
def app():
    """Flask app with in-memory SQLite DB"""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seeded_user(app):
    """Create a unique test user"""
    with app.app_context():
        unique_username = f"testuser-{uuid.uuid4()}"
        unique_email = f"{unique_username}@test.com"

        user = User(
            username=unique_username,
            email=unique_email,
            password_hash=hash_password("password123")
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def auth_header(seeded_user):
    token = generate_auth_token(str(seeded_user))
    return {"Authorization": f"Bearer {token}"}
