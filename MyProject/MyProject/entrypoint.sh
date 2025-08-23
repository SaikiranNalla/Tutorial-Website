#!/bin/sh
set -e

# Wait for DB to be ready (simple loop)
echo "Waiting for database..."
until python manage.py showmigrations >/dev/null 2>&1; do
  sleep 1
done

# Run migrations (safe for dev)
python manage.py migrate --noinput

# Collect static in case you need static files (nofail)
python manage.py collectstatic --noinput || true

# Execute CMD
exec "$@"