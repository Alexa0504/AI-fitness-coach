from backend.app import create_app
from backend.models import db, User, Goal, Plan
from backend.utils.security_utils import hash_password
from datetime import datetime, timezone
import os

def seed_data(app):
    with app.app_context():

        db.create_all()

        # --- USERS ---
        if db.session.query(User).count() == 0:
            users = [
                User(username="alice", email="alice@example.com", password_hash=hash_password("password123")),
                User(username="bob", email="bob@example.com", password_hash=hash_password("password123")),
                User(username="charlie", email="charlie@example.com", password_hash=hash_password("password123")),
            ]
            db.session.bulk_save_objects(users)
            db.session.commit()
            print("✅ Users seeded successfully!")
        else:
            print("Users already exist — skipping user seeding.")

        # --- GOALS ---
        if db.session.query(Goal).count() == 0:
            goals = [
                Goal(user_id=1, goal_type="weight_loss", target_value=5.0, unit="kg"),
                Goal(user_id=2, goal_type="muscle_gain", target_value=3.0, unit="kg"),
                Goal(user_id=3, goal_type="endurance", target_value=None, unit=None),
            ]
            db.session.bulk_save_objects(goals)
            db.session.commit()
            print("✅ Goals seeded successfully!")
        else:
            print("Goals already exist — skipping goal seeding.")

        # --- PLANS ---
        if db.session.query(Plan).count() == 0:
            plans = [
                Plan(
                    user_id=1,
                    plan_type="workout",
                    content={"days": ["Monday", "Wednesday", "Friday"], "exercises": ["Push-ups", "Squats", "Plank"]},
                    score=75,
                    created_at=datetime.now(timezone.utc),
                ),
                Plan(
                    user_id=2,
                    plan_type="diet",
                    content={"meals": ["Oatmeal breakfast", "Grilled chicken lunch", "Salad dinner"]},
                    score=82,
                    created_at=datetime.now(timezone.utc),
                ),
            ]
            db.session.bulk_save_objects(plans)
            db.session.commit()
            print("✅ Plans seeded successfully!")
        else:
            print("Plans already exist — skipping plan seeding.")

if __name__ == "__main__":

    testing = os.environ.get("TESTING") == "1"
    app = create_app({
        "TESTING": testing
    } if testing else None)

    seed_data(app)
