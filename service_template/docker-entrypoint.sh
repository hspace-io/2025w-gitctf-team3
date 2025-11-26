#!/bin/sh
set -e

mkdir -p /app/static/uploads /app/static/wargame_attachments

if [ "${DB_ENGINE:-sqlite}" = "mysql" ]; then
  echo "Waiting for MySQL at ${DB_HOST:-db}:${DB_PORT:-3306}..."
  python - <<'PY'
import os
import socket
import sys
import time

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "3306"))
timeout = 60
start = time.time()

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        if time.time() - start > timeout:
            sys.exit(f"Timed out waiting for {host}:{port}")
        time.sleep(2)
PY
fi

echo "Ensuring database tables exist..."
python - <<'PY'
from app import create_app
from extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    # Seed sample team posts to ensure random-match has rows
    from models.research import TeamPost
    if TeamPost.query.count() < 2:
        db.session.add(TeamPost(title="t1", owner="o1"))
        db.session.add(TeamPost(title="t2", owner="o2"))
        db.session.commit()
PY

echo "Starting server: $@"
exec "$@"
