#! /usr/bin/env bash
set -e
# Let the DB start
python /service/app/backend_pre_start.py

sleep 10;

# Run migrations
alembic upgrade head

# Create initial data in DB
python /service/app/initial_data.py

python /service/app/main.py