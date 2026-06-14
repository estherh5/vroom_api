"""Shared pytest fixtures for the Vroom API tests."""
from __future__ import annotations

import os
from collections.abc import Iterator

import alembic.config
import pytest
import testing.postgresql
from flask import Flask
from flask.testing import FlaskClient
from testing.common.database import DatabaseFactory

from vroom import db


def _build_url(postgresql: testing.postgresql.Postgresql) -> str:
    dsn = postgresql.dsn()
    return (
        f"postgresql://{dsn['user']}@{dsn['host']}:{dsn['port']}/"
        f"{dsn['database']}"
    )


def _initialize_test_database(postgresql: testing.postgresql.Postgresql) -> None:
    """Create the schema in a freshly initialized (cached) test database."""
    url = _build_url(postgresql)
    os.environ["DB_CONNECTION"] = url
    db.init_engine(url)
    alembic.config.main(argv=["--raiseerr", "upgrade", "head"])


class _PostgresqlFactory(DatabaseFactory):
    target_class = testing.postgresql.Postgresql


# Caches the initialized database so the schema is only built once.
Postgresql = _PostgresqlFactory(
    cache_initialized_db=True, on_initialized=_initialize_test_database
)


@pytest.fixture
def app() -> Iterator[Flask]:
    from server import create_app

    postgresql = Postgresql()
    url = _build_url(postgresql)
    os.environ["DB_CONNECTION"] = url
    db.init_engine(url)

    flask_app = create_app()
    flask_app.config.update(TESTING=True)

    yield flask_app

    postgresql.stop()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
