import os
import pytest
from backend.app import create_app
from backend.models import db


os.environ["TESTING"] = "1"

@pytest.fixture(scope="session")
def app():
    """Create Flask app with PostgreSQL test database"""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_DATABASE_URL"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():

        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Provide a Flask test client"""
    return app.test_client()


@pytest.fixture(scope="function")
def session(app):
    """Provide an isolated database session per test"""
    with app.app_context():
        yield db.session
        db.session.rollback()
