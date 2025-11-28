from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()
from .models import db
from backend.routes.auth import auth_bp
from backend.routes.plans import plans_bp
from backend.routes.goals import goals_bp
from backend.routes.users import users_bp
from backend.routes.tips import tips_bp
from backend.routes.stats import stats_bp
from backend.routes.progress import progress_bp
from backend.routes.xp import xp_bp

migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    if os.environ.get("TESTING") == "1":
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = "test-secret-key"
    elif test_config is not None:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"],
            "supports_credentials": True
        },
        r"/tips/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(plans_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tips_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(xp_bp)

    @app.route("/")
    def index():
        return "AI Fitness Coach Backend Running!"

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
