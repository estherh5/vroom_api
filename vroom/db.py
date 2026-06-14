"""Database engine and session management for the Vroom API.

The engine is created lazily so that importing the package (for tooling,
tests, or autogeneration) does not require a live database connection.
"""
from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


# Session factory; bound to an engine via init_engine() rather than at import
# time so the database URL isn't required just to import the module.
Session = sessionmaker(expire_on_commit=False)

_engine: Engine | None = None


def init_engine(url: str | None = None) -> Engine:
    """Create the engine and bind the session factory to it."""
    global _engine
    _engine = create_engine(url or os.environ["DB_CONNECTION"])
    Session.configure(bind=_engine)
    return _engine


def get_engine() -> Engine:
    """Return the active engine, creating it from the environment if needed."""
    if _engine is None:
        return init_engine()
    return _engine
