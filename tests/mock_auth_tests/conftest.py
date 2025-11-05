import pytest
from backend.app import create_app
from backend.models import db

@pytest.fixture(scope="session")
def app():
    """Create Flask app with in-memory SQLite DB for mock auth tests"""
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
    """Provide a Flask test client"""
    return app.test_client()

@pytest.fixture(scope="function")
def session(app):
    """Provide an isolated database session per test"""
    with app.app_context():
        yield db.session
        db.session.rollback()

@pytest.fixture(scope="session", autouse=True)
def ensure_in_memory_db(app):
    """Ensure tests do not touch production database"""
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if not uri.startswith("sqlite:///:memory:"):
        pytest.exit("ERROR: Attempted to use non-in-memory DB for tests!")
