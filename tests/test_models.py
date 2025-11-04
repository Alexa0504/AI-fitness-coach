from backend.models import User, Goal, Plan, TokenBlacklist


def test_create_user_in_mock_db(session):
    user = User(username="mockuser", email="mock@example.com", password_hash="hash")
    session.add(user)
    session.commit()

    found = session.query(User).filter_by(username="mockuser").first()
    assert found is not None
    assert found.email == "mock@example.com"


def test_goal_and_plan_relations(session):
    user = User(username="testuser", email="test@example.com", password_hash="pwd")
    session.add(user)
    session.flush()

    goal = Goal(user_id=user.id, goal_type="weight_loss", target_value=5, unit="kg")
    plan = Plan(user_id=user.id, plan_type="workout", content={"ex": ["pushups"]})
    session.add_all([goal, plan])
    session.commit()

    assert len(user.goals) == 1
    assert len(user.plans) == 1
    assert user.goals[0].goal_type == "weight_loss"
    assert user.plans[0].plan_type == "workout"


def test_token_blacklist_entry(session):
    token_entry = TokenBlacklist(token="abc123")
    session.add(token_entry)
    session.commit()

    found = session.query(TokenBlacklist).filter_by(token="abc123").first()
    assert found is not None
