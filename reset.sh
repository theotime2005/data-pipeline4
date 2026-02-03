#!/bin/bash

# Reset script for soutenance - Clean restart of the entire stack
# Usage: ./reset.sh

set -e

echo "🔄 Resetting Data Pipeline Iris..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}1️⃣ Stopping and removing all containers and volumes...${NC}"
cd "$(dirname "$0")"
docker compose down -v --remove-orphans
echo -e "${GREEN}✅ Cleanup complete${NC}"
echo ""

echo -e "${YELLOW}2️⃣ Building all services...${NC}"
docker compose build --no-cache
echo -e "${GREEN}✅ Build complete${NC}"
echo ""

echo -e "${YELLOW}3️⃣ Starting all services...${NC}"
docker compose up -d
echo -e "${GREEN}✅ Services started${NC}"
echo ""

echo -e "${YELLOW}4️⃣ Waiting for services to be ready...${NC}"
max_attempts=60
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if docker compose ps | grep -q "postgres.*healthy"; then
        echo -e "${GREEN}✅ PostgreSQL is healthy${NC}"
        break
    fi
    attempt=$((attempt + 1))
    echo "⏳ Waiting for PostgreSQL... ($attempt/$max_attempts)"
    sleep 1
done

# Wait for MLflow
echo "⏳ Waiting for MLflow..."
sleep 5

# Wait for preprocess and train jobs
echo "⏳ Waiting for preprocess job..."
sleep 5
echo "⏳ Waiting for train job..."
sleep 10

# Wait for API
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API is healthy${NC}"
        break
    fi
    attempt=$((attempt + 1))
    echo "⏳ Waiting for API... ($attempt/$max_attempts)"
    sleep 1
done

echo ""
echo -e "${GREEN}✅ Stack is ready!${NC}"
echo ""
echo "📊 Services are available at:"
echo "   - UI:           http://localhost:3000"
echo "   - API:          http://localhost:8000"
echo "   - MLflow:       http://localhost:5000"
echo "   - PostgreSQL:   localhost:5432"
echo ""
echo "🔗 Available endpoints:"
echo "   - GET  http://localhost:8000/health"
echo "   - POST http://localhost:8000/predict (body: {\"sepal_width\": 3.5})"
echo "   - POST http://localhost:3000/api/predict (via UI reverse proxy)"
echo ""
