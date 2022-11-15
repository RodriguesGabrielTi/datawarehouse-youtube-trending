import os
from dotenv import load_dotenv
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

import sys
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(main_dir)
from domain import models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = models.Base.metadata


def get_url():
    load_dotenv()
    url = os.getenv('DATABASE_URL', None)
    if not url:
        raise Exception('DATABASE_URL not defined')
    return url


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = create_engine(get_url())

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
