from backend.app import app
from backend.seed import seed_data
from backend.tips_seed import seed_tips

if __name__ == "__main__":
    with app.app_context():
        seed_data(app)
        seed_tips(app)
    app.run(debug=True, host="0.0.0.0", port=5000)