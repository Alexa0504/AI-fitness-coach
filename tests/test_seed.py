from backend.seed import seed_data
from backend.models import User, Goal, Plan

def test_seed_data_works_with_mock_db(app):
    """Secure seed test on mock (in-memory) database"""
    seed_data(app)

    with app.app_context():
        users = User.query.all()
        goals = Goal.query.all()
        plans = Plan.query.all()

        assert len(users) >= 3
        assert len(goals) >= 3
        assert len(plans) >= 2
