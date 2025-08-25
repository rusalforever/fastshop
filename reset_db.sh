#!/bin/bash
set -e

echo "Dropping and recreating public schema..."
docker compose exec -T db psql -U user -d fastapi_shop -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

echo "Stamping Alembic to head..."
docker compose exec -T web alembic stamp head

echo "Running migrations..."
docker compose exec -T web alembic upgrade head

echo "✅ Database reset complete!"