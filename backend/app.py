from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    else:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index():
        return "AI Fitness Coach Backend Running!"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
