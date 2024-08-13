#!/usr/bin/env bash

set -e

echo "Applying database migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
