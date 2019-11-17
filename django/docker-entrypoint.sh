#!/bin/sh
set -e

if [ $# -eq 0 ]; then
    mkdir -p ${DATA_DIR}
    python manage.py migrate
    gunicorn --workers=2 --threads=4 --worker-class=gthread --bind 0.0.0.0:8000 mysite.wsgi:application
fi

exec "$@"
