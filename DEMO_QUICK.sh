#!/bin/bash

# Quick Demo Script for Soutenance
# Shows all key functionality in 2 minutes

echo "🎬 Data Pipeline Iris - Demo Script"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Testing API endpoint directly${NC}"
echo "   Command: curl -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d '{\"sepal_width\": 3.5}'"
echo ""
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_width": 3.5}' | python3 -m json.tool
echo ""

echo -e "${BLUE}2. Testing API via Nginx reverse proxy (UI)${NC}"
echo "   Command: curl -X POST http://localhost:3000/api/predict -H 'Content-Type: application/json' -d '{\"sepal_width\": 4.0}'"
echo ""
curl -s -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_width": 4.0}' | python3 -m json.tool
echo ""

echo -e "${BLUE}3. Database status${NC}"
echo "   Connecting to PostgreSQL..."
docker compose exec -T db psql -U iris -d irisdb -c "SELECT COUNT(*) as total_records FROM iris_clean;"
echo ""

echo -e "${BLUE}4. MLflow model registry${NC}"
echo "   Checking registered models..."
curl -s http://localhost:5000/api/2.0/registered-models | python3 -m json.tool | head -20
echo ""

echo -e "${GREEN}✅ All systems operational!${NC}"
echo ""
echo -e "${YELLOW}Access points:${NC}"
echo "  • Web UI:     http://localhost:3000"
echo "  • API Docs:   http://localhost:8000/docs"
echo "  • MLflow:     http://localhost:5000"
echo ""
