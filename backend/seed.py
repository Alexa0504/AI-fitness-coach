from werkzeug.security import generate_password_hash
from backend.app import create_app
from backend.models import db, User

def seed_users():

    users = [
        User(
            username="alice",
            email="alice@example.com",
            password_hash=generate_password_hash("password123"),
        ),
        User(
            username="bob",
            email="bob@example.com",
            password_hash=generate_password_hash("password123"),
        ),
        User(
            username="charlie",
            email="charlie@example.com",
            password_hash=generate_password_hash("password123"),
        ),
    ]


    app = create_app()
    with app.app_context():
        db.session.bulk_save_objects(users)
        db.session.commit()
        print("Seed data loaded successfully!")

if __name__ == "__main__":
    seed_users()
