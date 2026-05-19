from logging.config import fileConfig
from pathlib import Path

from flask import current_app

from alembic import context

config = context.config

if config.config_file_name and Path(config.config_file_name).exists():
    fileConfig(config.config_file_name)
target_db = current_app.extensions["migrate"].db


def get_engine():
    try:
        return target_db.engine
    except TypeError:
        return target_db.get_engine()


def get_metadata():
    if hasattr(target_db, "metadatas"):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    url = current_app.config.get("SQLALCHEMY_DATABASE_URI")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=get_metadata())
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
