#!/usr/bin/env bash
set -e

# wait for DB to be ready (simple loop)
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database to be ready..."
  # Try running migrate up to n times
  n=0
  until python manage.py migrate --noinput; do
    n=$((n+1))
    if [ $n -gt 10 ]; then
      echo "Migrations failed after multiple attempts."
      break
    fi
    echo "DB not ready yet, retrying in 3s..."
    sleep 3
  done
else
  echo "No DATABASE_URL set, skipping migrations."
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "collectstatic failed"

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn MyProject.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120