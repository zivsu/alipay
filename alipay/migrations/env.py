from __future__ import with_statement
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

import define
from tornado.options import options

# Update options arguments from cammand line
cmd_options_x = config.cmd_opts.x or []
cmd_x_dict = dict(map(lambda x: x.split('=', 2), cmd_options_x))

for k, v in cmd_x_dict.items():
    if k in options: options[k] = v

# For 'autogenerate' support
from models import BaseModel, DB_URL, engine
from models.product import Product
from models.trade import Trade
from models.payment import Payment
from models.logtrade import LogTrade
target_metadata = BaseModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=DB_URL, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()