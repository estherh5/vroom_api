"""Application factory and entry point for the Vroom API."""
from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from vroom.db import get_engine
from vroom.routes import bp

load_dotenv()

# A booking is seven short fields; anything near this size is not one.
MAX_BODY_BYTES = 16 * 1024

# The only browser client. Per-IP request rate is capped at the edge by a
# Vercel Firewall rule ("Booking per-IP rate limit"), not in this process.
FRONTEND_ORIGIN = "https://vroom.crystalprism.io"
DEV_ORIGIN = "http://localhost:3000"


def create_app() -> Flask:
    """Build and configure the Flask application."""
    app = Flask(__name__)
    app.config["DEBUG"] = os.environ.get("ENV_TYPE") == "Dev"
    app.config["MAX_CONTENT_LENGTH"] = MAX_BODY_BYTES

    origins = [FRONTEND_ORIGIN] + ([DEV_ORIGIN] if app.config["DEBUG"] else [])
    CORS(app, resources={r"/api/*": {"origins": origins}})

    # Configure the database engine from DB_CONNECTION (lazy connect).
    get_engine()

    app.register_blueprint(bp)

    return app


app = create_app()
