import pytest
import os
from backend.app import create_app
from backend.models import db

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
