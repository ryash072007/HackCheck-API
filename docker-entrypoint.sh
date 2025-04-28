#!/bin/bash
set -e

# Start PostgreSQL in the background
service postgresql start

# Wait for PostgreSQL to be ready
until pg_isready -U $POSTGRES_USER; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Create database if it doesn't exist
su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'\" | grep -q 1 || psql -c 'CREATE DATABASE $POSTGRES_DB;'"

# Run Django migrations
python manage.py migrate

# Collect static files (optional, uncomment if needed)
python manage.py collectstatic --noinput

# Start Gunicorn server with 4 workers and 2 threads each
exec gunicorn HackCheckAPI.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2
