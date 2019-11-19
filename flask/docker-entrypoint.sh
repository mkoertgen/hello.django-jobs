#!/bin/sh
set -e

if [ $# -eq 0 ]; then
    mkdir -p ${DATA_DIR}
    flask db upgrade
    gunicorn --workers=2 --threads=4 --worker-class=gthread --bind 0.0.0.0:5000 wsgi:app
fi

exec "$@"
