import pytest
from backend.app import create_app
from backend.models import db

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
