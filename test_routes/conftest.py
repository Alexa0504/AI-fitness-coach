from unittest.mock import patch

import pytest
from backend.app import create_app
from backend.models import db, User


@pytest.fixture(scope="session")
def app():
    """Flask app – in-memory SQLite for tests"""
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
def client(app):
    """Provides a test client for the Flask app"""
    return app.test_client()


@pytest.fixture(scope="function")
def session(app):
    """Provides an isolated database session per test"""
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture(scope="session", autouse=True)
def ensure_in_memory_db(app):
    """Prevent tests from touching the production DB"""
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if not uri.startswith("sqlite:///:memory:"):
        pytest.exit("ERROR: Non-test database detected!")

    # -----------------------------
    # Mock user fixture
    # -----------------------------

@pytest.fixture(scope="function")
def mock_user(session):
        user = session.query(User).filter_by(email="test@example.com").first()
        if not user:
            user = User(
                username="testuser",
                email="test@example.com",
                password_hash="hash",
                gender="female",
                height_cm=170,
                weight_kg=65,
                target_weight_kg=60,
                age=30
            )
            session.add(user)
            session.commit()
        return user
