# 🎯 Data Pipeline Iris - Architecture Dockerisée

## Vue d'ensemble

Pipeline complet **100% Dockerisé** et orchestré avec **Docker Compose**, du prétraitement des données à la prédiction via API REST.

### 📊 Flux de données
```
iris.csv
   ↓
[Preprocess Service] → nettoie, normalise
   ↓
[PostgreSQL] → stocke iris_clean
   ↓
[Training Service] → Random Forest Regressor
   ↓
[MLflow] → enregistre modèle + métriques (MSE, R²)
   ↓
[API FastAPI] → /predict → prédictions en temps réel
```

---

## 🏗️ Architecture

### Services Docker Compose

| Service | Rôle | Port | Technologie |
|---------|------|------|-------------|
| **db** | Base de données centrale | 5432 | PostgreSQL 16 |
| **mlflow** | Tracking expériences & artefacts | 5000 | MLflow + Backend Postgres |
| **preprocess** | ETL (Extract → Transform → Load) | - | Python + Pandas + SQLAlchemy |
| **train** | ML Training avec enregistrement | - | Python + scikit-learn + MLflow |
| **api** | API de prédiction | 8000 | FastAPI + Uvicorn |
| **ui** | Interface web (UI + reverse proxy) | 3000 | Nginx alpine |

---

## 🚀 Démarrage rapide

### 1️⃣ Lancer le pipeline complet

```bash
docker compose up --build
```

### 2️⃣ Accéder aux interfaces

- **UI Web** : http://localhost:3000 (interface prédiction via navigateur)
- **API Swagger** : http://localhost:8000/docs
- **MLflow UI** : http://localhost:5000

### 3️⃣ Tester la prédiction

Via API directe :
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_width": 3.4}'
```

Via UI web (reverse proxy Nginx) :
```bash
curl -X POST "http://localhost:3000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_width": 3.4}'
```

---

## ✅ Tests End‑to‑end

Un script d'intégration automatique est fourni : `scripts/e2e_test.sh`.
Il :
- rebuild la stack (`docker compose down -v && docker compose up --build -d`)
- attend que MLflow et l'API répondent
- attend que `/predict` retourne 200 et affiche la réponse

Exécuter :

```bash
./scripts/e2e_test.sh
```

---

## 📋 Services détaillés

### Preprocess
- Charge `iris.csv`
- Normalise les colonnes
- Supprime NA et doublons
- StandardScaler sur features numériques
- Écrit dans PostgreSQL (table `iris_clean`)

### Training
- Entraîne `RandomForestRegressor`
- Target : `sepal_length` | Feature : `sepal_width`
- Enregistre modèle + métriques (MSE, R²) dans MLflow

### API
- `GET /health` → `{ "status": "ok" }`
- `POST /predict` → prédiction `sepal_length` à partir de `sepal_width`

### UI
- Interface web statique (HTML/CSS/JS) servie via Nginx
- Reverse proxy Nginx : `/api/*` → `http://api:8000/`
- Permet requêtes depuis navigateur (CORS, preflight OPTIONS)
- Prédictions accessibles via `http://localhost:3000`

---

## 🔧 Configuration (.env)

Fichier `.env` dans la racine (exemple) :

```env
POSTGRES_DB=irisdb
POSTGRES_USER=iris
POSTGRES_PASSWORD=irispass
POSTGRES_HOST=db
POSTGRES_PORT=5432

MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_EXPERIMENT_NAME=iris-sepal-regression
MODEL_NAME=iris_sepal_length_regressor

# Paramètres API : retry lors du chargement du modèle (optionnel)
API_MODEL_LOAD_RETRIES=30
API_MODEL_LOAD_DELAY=3
```

---

## 🔁 Reset complet (soutenance)

Un script `reset.sh` est fourni pour un redémarrage propre sans résidus :

```bash
./reset.sh
```

Ce script :
1. Arrête et supprime les containers et volumes (`docker compose down -v`)
2. Reconstruit tous les services sans cache (`docker compose build --no-cache`)
3. Démarre la stack (`docker compose up -d`)
4. Attend que tous les services soient prêts
5. Valide les endpoints critiques

**Résultat** : Pipeline en état vierge, prêt pour la démo.

---

## 🛠️ Débogage rapide

```bash
# Voir les logs
docker compose logs -f preprocess
docker compose logs -f train
docker compose logs -f api

# Accéder à la DB
docker compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB

# État
docker compose ps
```

---

## ✅ Checklist des livrables pour la soutenance

- Pipeline fonctionnel (conteneurs + orchestration) — OK
- Dossier technique (architecture, choix, métriques, critique, répartition) — À rédiger
- Support de présentation (slides + démonstration) — À préparer

---

## Remarques et points d'amélioration

- Healthchecks & restart policies : envisager `restart`/`healthcheck` pour `api` et `mlflow` en production.
- Permissions du volume `mlruns` : actuellement les services écrivent en tant que root ; durcir si requis.
- Optionnel : endpoint de reload du modèle à chaud ou UI web pour soumettre la largeur depuis le navigateur.

---

**Repo** : theotime2005/data-pipeline4
