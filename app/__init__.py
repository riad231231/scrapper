from flask import Flask
import os
from .db import init_db


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.getenv("SECRET_KEY", "prospection-studio-riad-2026")

    with app.app_context():
        init_db()

    from .routes import bp
    app.register_blueprint(bp)

    return app
