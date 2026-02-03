#!/usr/bin/env bash
set -euo pipefail

# Script E2E: rebuild stack, wait services, test MLflow UI, API /health and /predict
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "[e2e] Cleaning and starting stack (this may take ~1-2 minutes)..."
docker compose down -v --remove-orphans || true
docker compose up --build -d

# wait for services
echo "[e2e] Waiting for MLflow UI (http://localhost:5000) and API /health (http://localhost:8000/health)..."
MAX_WAIT=180
SLEEP=3
elapsed=0

until [ "$elapsed" -ge "$MAX_WAIT" ]; do
  mlflow_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 || echo "000")
  api_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")
  echo "[e2e] MLflow:$mlflow_code API:$api_code (waited ${elapsed}s)"
  if [ "$mlflow_code" = "200" ] && [ "$api_code" = "200" ]; then
    break
  fi
  sleep $SLEEP
  elapsed=$((elapsed + SLEEP))
done

if [ "$mlflow_code" != "200" ] || [ "$api_code" != "200" ]; then
  echo "[e2e][ERROR] Services didn't become ready within $MAX_WAIT seconds"
  docker compose ps
  exit 2
fi

# Wait for model to be available via /predict; allow longer as train may run
echo "[e2e] Waiting for /predict to return 200 (model load)..."
MAX_WAIT2=180
elapsed=0

while [ "$elapsed" -lt "$MAX_WAIT2" ]; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"sepal_width":3.5}' || echo "000")
  echo "[e2e] /predict -> $code (waited ${elapsed}s)"
  if [ "$code" = "200" ]; then
    echo "[e2e] SUCCESS: /predict returned 200"
    # show response
    curl -s -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"sepal_width":3.5}'
    exit 0
  fi
  if [ "$code" = "400" ]; then
    # Bad request likely due to payload; fail
    echo "[e2e][ERROR] /predict returned 400 (bad request)"
    docker compose logs api --tail=200
    exit 3
  fi
  sleep $SLEEP
  elapsed=$((elapsed + SLEEP))
done

echo "[e2e][ERROR] /predict did not return 200 within $MAX_WAIT2 seconds"
docker compose logs train --tail=200
docker compose logs api --tail=200
exit 4
