from backend.app import app
from backend.seed import seed_data

if __name__ == "__main__":
    with app.app_context():
        seed_data(app)
    app.run(debug=True, host="0.0.0.0", port=5000)