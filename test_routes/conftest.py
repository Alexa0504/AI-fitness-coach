import os
import pytest
from backend.app import create_app
from backend.models import db

@pytest.fixture(scope="session")
def app():

    os.environ["TESTING"] = "1"

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/fitness_db_test",
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
    return app.test_client()
