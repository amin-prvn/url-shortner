#!/bin/sh

# Only first time for add alembic for migration

# $ alembic init -t async migrations
# change 
# target_metadata = Base.metadata 
# and add 
# from app.api.config import get_settings
# config.set_main_option("sqlalchemy.url", get_settings().DB_CONFIG)
# to maigrations/env.py
# 
# $ alembic revision --autogenerate -m "init"
# $ alembic upgrade head


alembic revision --autogenerate -m 'add urls'
alembic upgrade head

exec "$@"