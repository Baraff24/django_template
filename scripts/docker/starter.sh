#!/usr/bin/env bash
set -euo pipefail

python manage.py check
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Migrations belong in source control; generate them explicitly during development.
# Run tests separately so startup never creates a test database in production.
exec gunicorn core.asgi:application --bind 0.0.0.0:8000 \
    --worker-class uvicorn_worker.UvicornWorker --timeout 30 --workers 2
