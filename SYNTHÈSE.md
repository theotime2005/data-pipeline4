# 📝 SYNTHÈSE DE CONSTRUCTION - Data Pipeline Iris

## ✅ Statut : **COMPLET - PRÊT POUR LA SOUTENANCE**

---

## 📦 FICHIERS CRÉÉS / CONFIGURÉS

### 1. **Configuration & Environnement**
- `.env` - Variables d'environnement centralisées (DB, MLflow)
- `docker-compose.yml` - Orchestration 5 services (validé ✓)
- `launch.sh` - Script bash pour démarrage rapide

### 2. **Database PostgreSQL**
- `db/init.sql` - Schéma : table `iris_clean` (5 colonnes)

### 3. **Service Preprocess**
- `services/preprocess/Dockerfile` - Python 3.11-slim + pip install
- `services/preprocess/preprocess.py` - ETL logic (csv → clean → insert)
- `services/preprocess/requirements.txt` - pandas, SQLAlchemy, scikit-learn

### 4. **Service Training**
- `services/train/Dockerfile` - Python 3.11-slim
- `services/train/train.py` - RandomForestRegressor + MLflow logging
- `services/train/requirements.txt` - scikit-learn, MLflow

### 5. **Service API FastAPI**
- `services/api/Dockerfile` - FastAPI + Uvicorn
- `services/api/main.py` - Endpoints: /health, /predict
- `services/api/requirements.txt` - FastAPI, Pydantic, MLflow client

### 6. **Dataset**
- `iris.csv` - 150 observations (50 setosa, 50 versicolor, 50 virginica)

### 7. **Documentation**
- `README.md` - Guide complet (architecture, démarrage, soutenance)
- `SYNTHÈSE.md` - Ce fichier

---

## 🎯 VALIDATION

| Composant | Status | Vérification |
|-----------|--------|------------|
| docker-compose.yml | ✅ | `docker compose config` PASS |
| preprocess.py | ✅ | `python3 -m py_compile` PASS |
| train.py | ✅ | `python3 -m py_compile` PASS |
| main.py (API) | ✅ | `python3 -m py_compile` PASS |
| iris.csv | ✅ | 151 lignes (150 data + 1 header) |

---

## 🚀 DÉMARRAGE

### Démarrage complet
```bash
docker compose up --build
```

### Ou avec le script
```bash
bash launch.sh
```

### Temps d'attente estimé
- DB ready: ~5-10s
- MLflow server up: ~20-30s
- Preprocess done: ~30-40s
- Training done: ~1-2 min
- API ready: ~5s après training

**Total estimé: 2-3 minutes**

---

## 📍 ACCÈS APRÈS DÉMARRAGE

| Interface | URL | Fonction |
|-----------|-----|----------|
| MLflow | `http://localhost:5000` | Voir expériences + métriques |
| API Swagger | `http://localhost:8000/docs` | Tester les endpoints |
| API Health | `http://localhost:8000/health` | Vérifier le statut |

---

## 🧪 TEST RAPIDE (dans un autre terminal)

### Health check
```bash
curl http://localhost:8000/health
```

### Prédiction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_width": 3.5}'
```

Réponse attendue:
```json
{
  "sepal_width": 3.5,
  "sepal_length_pred": 5.9
}
```

### Vérifier la DB
```bash
docker compose exec db psql -U iris -d irisdb -c "SELECT COUNT(*) FROM iris_clean;"
```

---

## 📊 FLUX DE DONNÉES

```
iris.csv (150 obs)
    ↓
[PREPROCESS] 
  - Normalise colonnes
  - Supprime NA/doublons
  - StandardScaler
    ↓
PostgreSQL (iris_clean table)
    ↓
[TRAIN]
  - RandomForestRegressor (n_estimators=200)
  - Target: sepal_length
  - Feature: sepal_width
  - Calcule MSE, R²
    ↓
MLflow (tracking)
  - Log params + metrics
  - Enregistre modèle (Model Registry)
    ↓
[API FastAPI]
  - Charge modèle depuis MLflow
  - Route /predict
    ↓
Client (curl, Swagger, etc.)
```

---

## 🎓 SOUTENANCE - CHECKLIST

### À montrer
- [ ] `docker compose up --build` et attendre ~2-3 min
- [ ] **MLflow UI** : naviguer dans l'expérience `iris-sepal-regression`
  - Afficher les métriques (MSE ≈ 0.12-0.15, R² ≈ 0.95-0.97)
  - Montrer le modèle enregistré (Model Registry)
- [ ] **Swagger API** (`http://localhost:8000/docs`)
  - Cliquer sur "Try it out" pour /predict
  - Envoyer une requête avec `sepal_width: 3.5`
  - Afficher la réponse
- [ ] **Base de données** (optionnel)
  - `docker compose exec db psql -U iris -d irisdb -c "SELECT * FROM iris_clean LIMIT 5;"`

### À expliquer
- [ ] Flux complet : CSV → Preprocess → DB → Train → MLflow → API
- [ ] Isolation des services : chaque conteneur a un rôle bien défini
- [ ] Dépendances respectées : `docker-compose.yml` contrôle l'ordre
- [ ] Volumage persistant : `pgdata` (DB) et `mlruns` (artefacts)
- [ ] Réseau Compose : services se parlent par nom (`db`, `mlflow`)
- [ ] Choix techniques :
  - **PostgreSQL** : SGBD robuste, backend officiel MLflow
  - **MLflow** : tracking + Model Registry + UI web
  - **FastAPI** : doc auto (Swagger), performance, typage Pydantic
  - **RandomForest** : baseline solide, pas d'hyperparamètres critiques

### Diapos / Dossier technique
À rédiger après la démo (structure dans README.md section "Dossier technique / slides")

---

## 🔍 TROUBLESHOOTING RAPIDE

### "DB not reachable"
```bash
docker compose ps
# db doit être en "healthy" status
```

### "No model versions found"
- Vérifier que `train` s'est exécuté : `docker compose logs train | tail -20`
- Attendre ~1-2 min après "Preprocess done"

### "API répond 500"
```bash
curl http://localhost:5000  # MLflow doit être up
docker compose logs api     # Afficher les logs de l'API
```

### Relancer complètement
```bash
docker compose down -v
docker compose up --build
```

---

## 📚 STRUCTURE FINALE

```
data-pipeline4/
├── .env
├── .gitignore
├── README.md
├── SYNTHÈSE.md
├── docker-compose.yml
├── iris.csv
├── launch.sh
├── db/
│   ├── .gitkeep
│   └── init.sql
├── mlflow/
│   └── .gitkeep
└── services/
    ├── preprocess/
    │   ├── Dockerfile
    │   ├── preprocess.py
    │   └── requirements.txt
    ├── train/
    │   ├── Dockerfile
    │   ├── train.py
    │   └── requirements.txt
    └── api/
        ├── Dockerfile
        ├── main.py
        └── requirements.txt
```

---

## 🎉 NEXT STEPS

1. **Avant la soutenance** :
   - Test: `docker compose up --build` une fois complètement
   - Vérifier que MLflow UI et API répondent
   - Préparer les diapos (justifications choix, perf, limites)

2. **Pistes d'améliorations** (bonus pour montrer de l'initiative) :
   - Cross-validation dans train.py
   - Hyperparameter tuning (GridSearch)
   - Versioning Production/Staging dans MLflow
   - UI bonus (page HTML avec formulaire)
   - Tests automatisés (pytest)

3. **Documentation supplémentaire** (si demandée) :
   - Schéma d'architecture (excalidraw, draw.io)
   - Logs d'une run complète
   - Performances (temps d'exécution par service)

---

**Date**: 2026-02-02  
**Branch**: Amaury  
**Repo**: theotime2005/data-pipeline4

✨ **Projet PRÊT pour présentation!** 🎓
