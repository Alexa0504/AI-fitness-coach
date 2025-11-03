from backend.app import create_app
from backend.models import db, User
from backend.utils.security_utils import hash_password


def seed_users(app):
    users = [
        User(
            username="alice",
            email="alice@example.com",
            password_hash=hash_password("password123"),
        ),
        User(
            username="bob",
            email="bob@example.com",
            password_hash=hash_password("password123"),
        ),
        User(
            username="charlie",
            email="charlie@example.com",
            password_hash=hash_password("password123"),
        ),
    ]

    with app.app_context():

        if db.session.query(User).count() == 0:
            db.session.bulk_save_objects(users)
            db.session.commit()
            print("Seed data loaded successfully!")
        else:
            print("Database already contains users. Skipping seed.")


if __name__ == "__main__":
    app = create_app()
    seed_users(app)
