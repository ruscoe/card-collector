import os
from flask import Flask
from . import db
from .routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/card_collector"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
