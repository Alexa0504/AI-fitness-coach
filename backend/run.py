from app import app
from seed import seed_users

if __name__ == "__main__":
    with app.app_context():
        seed_users()
    app.run(debug=True, host="0.0.0.0", port=5000)