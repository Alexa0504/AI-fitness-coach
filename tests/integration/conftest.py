import os
import uuid
import pytest
from backend.app import create_app
from backend.models import db, User, Tip
from backend.utils.security_utils import hash_password, generate_auth_token


os.environ["TESTING"] = "1"

@pytest.fixture(scope="session")
def app():
    """Flask app using PostgreSQL test database"""
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seeded_user(app):
    """Create a unique test user in the test DB"""
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
def auth_header(app, seeded_user):
    token = generate_auth_token(str(seeded_user))
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def seed_tips(app):
    """Seed tips in test DB"""
    with app.app_context():
        tips = [
            Tip(category="general", text="Drink 8 glasses of water daily."),
            Tip(category="general", text="Eat more vegetables"),
            Tip(category="workout", text="Do 10 pushups"),
        ]
        db.session.add_all(tips)
        db.session.commit()
        yield tips
        db.session.query(Tip).delete()
        db.session.commit()
