#!/bin/bash
set -e
cd "$(dirname "$0")"
python manage.py migrate --noinput
python manage.py collectstatic --noinput 2>/dev/null || true
exec gunicorn --bind "0.0.0.0:${PORT:-3000}" --workers 2 --timeout 120 vias_seguras.wsgi:application
