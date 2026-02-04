#!/bin/sh
# MLflow entrypoint script
set -e

echo "Starting MLflow server..."
exec mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB} \
    --default-artifact-root file:///mlruns
