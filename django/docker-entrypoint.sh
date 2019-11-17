#!/bin/sh
set -e

if [ $# -eq 0 ]; then
    mkdir -p ${DATA_DIR}
    python manage.py migrate
    gunicorn --bind 0.0.0.0:8000 wsgi:application
fi

exec "$@"
