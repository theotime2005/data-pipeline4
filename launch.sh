#!/bin/bash

# 🚀 Data Pipeline Iris - Quick Start Script

set -e

echo "════════════════════════════════════════════════════════════════"
echo "🎯 Data Pipeline Iris - Lancement Automatique"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker non trouvé. Installe Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  docker-compose CLI non trouvé, utilisant 'docker compose' à la place."
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "✅ Docker détecté"
echo ""

# Validation docker-compose.yml
echo "🔍 Validation du docker-compose.yml..."
$DOCKER_COMPOSE config > /dev/null && echo "✅ Fichier valide" || { echo "❌ Erreur"; exit 1; }
echo ""

# Vérification du dataset
echo "📊 Vérification du dataset iris.csv..."
if [ ! -f "iris.csv" ]; then
    echo "❌ iris.csv manquant. Crée-le d'abord."
    exit 1
fi
IRIS_LINES=$(wc -l < iris.csv)
echo "✅ iris.csv trouvé ($IRIS_LINES lignes)"
echo ""

# Lancer le pipeline
echo "🐳 Lancement du pipeline (docker compose up --build)..."
echo "⏳ Cela peut prendre 2-3 minutes..."
echo ""

$DOCKER_COMPOSE up --build

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ Pipeline lancé avec succès!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📍 Accéder aux interfaces :"
echo "   - MLflow UI:      http://localhost:5000"
echo "   - API Swagger:    http://localhost:8000/docs"
echo "   - API Health:     http://localhost:8000/health"
echo ""
echo "🧪 Tester la prédiction :"
echo "   curl -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d '{\"sepal_width\": 3.4}'"
echo ""
echo "🛑 Pour arrêter : Ctrl+C ou 'docker compose down'"
echo ""
