#!/bin/bash
set -e

# Start PostgreSQL in the background
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
until pg_isready -h 127.0.0.1 -p 5432; do
  echo "Waiting for postgres..."
  sleep 2
done

# Run Django migrations (optional)
python3 manage.py migrate

# Start Django server with Gunicorn, listening on all interfaces
gunicorn HackCheckAPI.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2