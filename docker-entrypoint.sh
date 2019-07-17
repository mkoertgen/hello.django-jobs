#!/bin/sh
set -e

if [ $# -eq 0 ]; then
    ./manage.py migrate
    gunicorn --bind 0.0.0.0:8000 wsgi:application
fi

exec "$@"
