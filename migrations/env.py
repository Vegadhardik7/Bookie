"""
This file configures Alembic for database migrations.
It sets up the database connection, configures logging, and defines functions for running migrations in both offline and online modes.
"""

import asyncio  # Import asyncio for handling asynchronous operations.
from logging.config import fileConfig  # Import fileConfig for configuring logging.

from sqlalchemy import pool  # Import pool for database connection pooling.
from sqlalchemy.engine import Connection  # Import Connection for database connections.
from sqlalchemy.ext.asyncio import async_engine_from_config  # Import async_engine_from_config for creating asynchronous database engines.
from src.db.models import User, BookModel  # Import the User and BookModel from the database models.
from src.config import Config  # Import the Config class for accessing configuration settings.
from sqlmodel import SQLModel  # Import SQLModel for handling SQLAlchemy models.
from alembic import context  # Import context from Alembic for migration context.

database_url = Config.DATABASE_URL  # Get the database URL from the configuration.

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", database_url)  # Set the database URL in the Alembic configuration.

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)  # Configure logging using the config file.

# Add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata  # Set the target metadata for autogenerate support.

# Other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")  # Get the database URL from the Alembic configuration.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )  # Configure the context for offline mode.

    with context.begin_transaction():
        context.run_migrations()  # Run the migrations.

def do_run_migrations(connection: Connection) -> None:
    """Run migrations using a connection."""
    context.configure(connection=connection, target_metadata=target_metadata)  # Configure the context with the connection.

    with context.begin_transaction():
        context.run_migrations()  # Run the migrations.

async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )  # Create an asynchronous engine from the Alembic configuration.

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)  # Run the migrations using the connection.

    await connectable.dispose()  # Dispose of the engine.

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())  # Run the asynchronous migrations.

if context.is_offline_mode():
    run_migrations_offline()  # Run migrations in offline mode if the context is in offline mode.
else:
    run_migrations_online()  # Run migrations in online mode if the context is in online mode.