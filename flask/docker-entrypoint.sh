#!/bin/sh
set -e

if [ $# -eq 0 ]; then
    mkdir -p ${DATA_DIR}
    # TODO: run flask migrations
    gunicorn --workers=2 --threads=4 --worker-class=gthread --bind 0.0.0.0:5000 app:app
fi

exec "$@"
