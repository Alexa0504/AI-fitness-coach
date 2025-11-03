from app import create_app
from models import db, User
from utils.security_utils import hash_password

def seed_users():

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


    app = create_app()


    with app.app_context():

        if db.session.query(User).count() == 0:
            db.session.bulk_save_objects(users)
            db.session.commit()
            print("Seed data loaded successfully!")
        else:
            print("Database already contains users. Skipping seed.")

if __name__ == "__main__":
    seed_users()
