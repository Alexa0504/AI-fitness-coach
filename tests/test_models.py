from datetime import date

from backend.models import User, Goal, Plan, TokenBlacklist, UserGoal, Tip


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

def test_progress_state_json(session):
    user = User(username="j", email="j@j.com", password_hash="x")
    user.set_progress_state({"steps": 1000})

    session.add(user)
    session.commit()

    found = session.query(User).filter_by(username="j").first()

    assert found.get_progress_state() == {"steps": 1000}

def test_user_goal_creation(session):
    user = User(username="goaluser", email="goal@user.com", password_hash="pwd")
    session.add(user)
    session.flush()

    user_goal = UserGoal(user_id=user.id, goal_name="Run 5km", week_start=date.today())
    session.add(user_goal)
    session.commit()

    found = session.query(UserGoal).filter_by(user_id=user.id).first()
    assert found is not None
    assert found.goal_name == "Run 5km"
    assert found.to_dict()["goal_name"] == "Run 5km"

    def test_tip_creation(session):
        tip = Tip(category="nutrition", text="Drink water")
        session.add(tip)
        session.commit()

        found = session.query(Tip).filter_by(category="nutrition").first()
        assert found is not None
        assert found.text == "Drink water"
        assert found.to_dict()["text"] == "Drink water"

def test_to_dict_methods(session):
    user = User(username="dictuser", email="dict@user.com", password_hash="pwd")
    session.add(user)
    session.flush()

    goal = Goal(user_id=user.id, goal_type="muscle_gain", target_value=2, unit="kg")
    plan = Plan(user_id=user.id, plan_type="workout", content={"ex": ["squat"]}, score=50)
    token = TokenBlacklist(token="tokentest")
    session.add_all([goal, plan, token])
    session.commit()

    assert isinstance(user.to_dict(), dict)
    assert isinstance(goal.to_dict(), dict)
    assert isinstance(plan.to_dict(), dict)
    assert isinstance(token.__repr__(), str)
