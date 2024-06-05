#!/bin/sh
export FLASK_APP=core/server.py
export PYTHONPATH=.:$PYTHONPATH
flask db upgrade -d core/migrations
exec "$@"

