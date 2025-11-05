import time
import uuid
import pytest
from backend.app import create_app, db
from backend.models import User, Goal, Plan
from backend.utils.security_utils import hash_password


@pytest.fixture(scope="function")
def test_client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test-secret"
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()


            user = User(
                username="perf_user",
                email="perf@test.com",
                password_hash=hash_password("test123")
            )
            db.session.add(user)
            db.session.commit()

            yield client
            db.session.remove()
            db.drop_all()


def test_auth_login_performance(test_client):
    """Performance test: /api/auth/login should respond < 0.5s"""
    start = time.time()
    response = test_client.post("/api/auth/login", json={
        "email": "perf@test.com",
        "password": "test123"
    })
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.5
    print(f"LOGIN endpoint response time: {duration:.4f}s")


def test_goals_list_performance(test_client):
    """Performance test for GET /api/goals/ with many records"""
    from backend.models import Goal


    user = User.query.first()
    for i in range(300):
        db.session.add(Goal(user_id=user.id, goal_type=f"goal{i}", target_value=10, unit="kg"))
    db.session.commit()


    login = test_client.post("/api/auth/login", json={"email": "perf@test.com", "password": "test123"})
    token = login.get_json()["token"]

    start = time.time()
    response = test_client.get("/api/goals/", headers={"Authorization": f"Bearer {token}"})
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.7
    print(f"GET /goals performance: {duration:.4f}s")


def test_plan_creation_performance(test_client):
    """Performance: Creating a mocked AI plan < 0.8s"""
    login = test_client.post("/api/auth/login", json={"email": "perf@test.com", "password": "test123"})
    token = login.get_json()["token"]

    start = time.time()
    response = test_client.post("/api/plans/", headers={"Authorization": f"Bearer {token}"}, json={
        "plan_type": "workout"
    })
    duration = time.time() - start

    assert response.status_code == 201
    assert duration < 0.8
    print(f"POST /plans performance: {duration:.4f}s")
