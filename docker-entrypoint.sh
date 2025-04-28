#!/bin/bash
set -e

# Change PostgreSQL to listen on port 5433
sed -i "s/^#port = 5432/port = 5433/" /etc/postgresql/*/main/postgresql.conf

# Start PostgreSQL in the background
service postgresql start

# Wait for PostgreSQL to be ready on port 5433
until pg_isready -U $POSTGRES_USER -p 5433; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Create database if it doesn't exist (connect on port 5433)
su - postgres -c "psql -p 5433 -tc \"SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'\" | grep -q 1 || psql -p 5433 -c 'CREATE DATABASE $POSTGRES_DB;'"

# Run Django migrations
python manage.py migrate

# Collect static files (optional, uncomment if needed)
python manage.py collectstatic --noinput

# Start Gunicorn server with 4 workers and 2 threads each
exec gunicorn HackCheckAPI.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2
