#!/usr/bin/env bash
# Render build for OJAS 2026.
# Works whether Render's Root Directory is the repo root (ojus/)
# or backend/ itself.
set -o errexit
if [ -f "backend/requirements.txt" ]; then
  pip install -r backend/requirements.txt
  cd backend
elif [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "ERROR: requirements.txt not found in . or backend/ — check Root Directory." >&2
  exit 1
fi
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed_ojas || true
