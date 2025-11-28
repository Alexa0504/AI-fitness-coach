import os
import pytest
import uuid
from backend.app import create_app
from backend.models import db, User
from backend.utils.security_utils import hash_password, generate_auth_token


os.environ["TESTING"] = "1"


TEST_DB_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DB_URL:
    raise RuntimeError("TEST_DATABASE_URL must be set in your environment (.env)")

@pytest.fixture(scope="session")
def app():
    """Flask app connected to PostgreSQL test database"""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DB_URL,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })


    if os.getenv("DATABASE_URL") == TEST_DB_URL:
        pytest.exit("ERROR: TEST_DATABASE_URL must not be the production DB!")

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def session(app):
    """Provide an isolated database session per test"""
    with app.app_context():
        yield db.session
        db.session.rollback()

@pytest.fixture()
def client(app):
    """Flask test client"""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create a user in the test database."""
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
    """Generate a valid token for the test user"""
    return generate_auth_token(str(test_user.id))

@pytest.fixture()
def auth_header(auth_token):
    """Flask Authorization header for protected routes"""
    return {"Authorization": f"Bearer {auth_token}"}
