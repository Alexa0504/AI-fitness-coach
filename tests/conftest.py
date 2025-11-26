import pytest
import os
from backend.app import create_app
from backend.models import db, User
from backend.utils.security_utils import hash_password, generate_auth_token


@pytest.fixture(scope="session")
def app():
    """Test app – with SQLite in-memory database"""
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

@pytest.fixture()
def session(app):
    """Isolated session for every test"""
    with app.app_context():
        yield db.session
        db.session.rollback()

@pytest.fixture(scope="session", autouse=True)
def ensure_in_memory_db(app):
    """Safety check to ensure tests never touch the production database"""
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if not uri.startswith("sqlite:///:memory:"):
        pytest.exit("ERROR: Test attempted to use a non-mock (non-in-memory) database!")

@pytest.fixture()
def client(app):
    """Flask test client"""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a user in the in-memory DB."""
    import uuid
    user = User(
        username=f"tester_{uuid.uuid4().hex[:6]}",
        email=f"tester_{uuid.uuid4().hex[:6]}@example.com",
        password_hash=hash_password("password123")
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def auth_token(test_user):
    """Generate a valid token using the real auth system."""
    return generate_auth_token(str(test_user.id))


@pytest.fixture()
def auth_header(auth_token):
    """Flask header used to authenticate protected routes."""
    return {"Authorization": f"Bearer {auth_token}"}
