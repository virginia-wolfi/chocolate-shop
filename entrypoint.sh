#!/bin/sh

echo "Waiting for database..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Database is ready!"

echo "Applying database migrations..."
poetry run python manage.py migrate
poetry run python manage.py create_groups

apk add --no-cache postgresql-client

echo "Loading initial data..."
poetry run python manage.py dbshell < categories-products-data.sql || echo "Failed to load SQL data"

echo "Starting Django server..."
exec poetry run python manage.py runserver 0.0.0.0:8000
