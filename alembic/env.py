import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from vroom import models

# Alembic Config object, providing access to the values within the .ini file.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model metadata for 'autogenerate' support.
target_metadata = models.Base.metadata

# Set the database URL from the environment.
config.set_main_option("sqlalchemy.url", os.environ["DB_CONNECTION"])


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (URL only, no Engine/DBAPI)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (Engine + connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
