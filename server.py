"""Application factory and entry point for the Vroom API."""
from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from vroom.db import get_engine
from vroom.routes import bp

load_dotenv()


def create_app() -> Flask:
    """Build and configure the Flask application."""
    app = Flask(__name__)
    app.config["DEBUG"] = os.environ.get("ENV_TYPE") == "Dev"

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configure the database engine from DB_CONNECTION (lazy connect).
    get_engine()

    app.register_blueprint(bp)

    return app


app = create_app()
