# ✅ Projet Data Pipeline Iris - Soutenance 2026-02-06

## 🎯 Objectif Réalisé

Pipeline **100% Dockerisé** d'apprentissage machine (ML) avec orchestre Docker Compose :
- Données iris.csv → Nettoyage → Stockage PostgreSQL → Entraînement → MLflow → API FastAPI → Interface Web

---

## 📦 Architecture Déployée

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │ PostgreSQL  │  │   MLflow     │  │   UI (Nginx)       │ │
│  │   Port 5432 │  │   Port 5000  │  │   Port 3000        │ │
│  │   [db]      │  │  [mlflow]    │  │  [ui]              │ │
│  └─────────────┘  └──────────────┘  └────────────────────┘ │
│        ▲                  ▲                    │              │
│        │                  │                    │ Nginx proxy  │
│  ┌─────────────┐  ┌──────────────┐           ▼              │
│  │ Preprocess  │  │   Training   │  ┌────────────────────┐ │
│  │  (batch)    │  │   (batch)    │  │   FastAPI          │ │
│  │ [preprocess]│  │  [train]     │  │   Port 8000        │ │
│  └─────────────┘  └──────────────┘  │   [api]            │ │
│        ▼                  ▼           └────────────────────┘ │
│   iris.csv          ML Model              /predict          │
│                                           /health           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Services Docker

| Service | Rôle | Port | État |
|---------|------|------|------|
| **db** | PostgreSQL 16 | 5432 | ✅ Healthy |
| **mlflow** | Model Registry + Tracking | 5000 | ✅ Ready |
| **preprocess** | ETL (iris.csv → DB) | - | ✅ Completed |
| **train** | ML Training (RandomForest) | - | ✅ Model registered |
| **api** | FastAPI /predict endpoint | 8000 | ✅ Responsive |
| **ui** | Nginx reverse proxy + UI | 3000 | ✅ Serving |

---

## 🚀 Démarrage Rapide pour Soutenance

### Option 1 : Reset complet (recommandé)
```bash
./reset.sh
```
- Supprime tous les containers et volumes
- Rebuild complète (cache=off)
- Démarre fresh stack
- Valide tous les endpoints

### Option 2 : Redémarrage rapide
```bash
docker compose up -d
```

---

## 🧪 Validation

Tous les tests passent ✅

```
✅ API /health                 → 200 OK {"status": "ok"}
✅ API /predict (sepal_width=3.5) → 200 OK {"sepal_length_pred": 5.08}
✅ Nginx reverse proxy         → POST localhost:3000/api/predict → 200 OK
✅ CORS preflight (OPTIONS)    → 204 No Content with headers
✅ MLflow model registry       → Model registered & accessible
✅ PostgreSQL iris_clean       → Table populated & queryable
```

---

## 🌐 Accès Interfaces

| Service | URL | Description |
|---------|-----|-------------|
| **UI Web** | http://localhost:3000 | Interface prédiction (bonus) |
| **API Swagger** | http://localhost:8000/docs | Documentation interactive |
| **MLflow** | http://localhost:5000 | Experiments & Model Registry |
| **API Direct** | http://localhost:8000 | Endpoints REST |

---

## 📄 Livrables Inclus

✅ **docker-compose.yml** — Orchestration 6 services  
✅ **README.md** — Documentation complète  
✅ **DOSSIER_TECHNIQUE.md** — Architecture & choix tech  
✅ **SYNTHÈSE.md** — Executive summary  
✅ **slides/Presentation.md** — Slides (markdown)  
✅ **slides/Presentation.pptx** — Slides (PowerPoint)  
✅ **slides/DEMO.md** — Script de démonstration  
✅ **scripts/e2e_test.sh** — Tests intégration  
✅ **reset.sh** — Restart propre  

---

## 🔧 Structure des Fichiers

```
data-pipeline4/
├── docker-compose.yml          # Orchestration
├── .env                         # Variables d'environnement
├── iris.csv                     # Dataset
├── reset.sh                     # Script reset soutenance
├── README.md                    # Documentation
├── DOSSIER_TECHNIQUE.md         # Technical specification
├── SYNTHÈSE.md                  # Executive summary
├── db/
│   └── init.sql                 # Initialisation PostgreSQL
├── services/
│   ├── preprocess/
│   │   ├── Dockerfile
│   │   ├── preprocess.py
│   │   └── requirements.txt
│   ├── train/
│   │   ├── Dockerfile
│   │   ├── train.py
│   │   └── requirements.txt
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   └── ui/
│       ├── Dockerfile
│       ├── index.html
│       └── nginx.conf
├── scripts/
│   ├── e2e_test.sh
│   └── md_to_pptx.py
└── slides/
    ├── Presentation.md
    ├── Presentation.pptx
    └── DEMO.md
```

---

## ✨ Points Forts

✅ **Complètement conteneurisé** — Pas de dépendances locales  
✅ **Pipeline automatisé** — Preprocessing → Training → Registry → API  
✅ **Traceable** — Toutes les expériences loggées dans MLflow  
✅ **Scalable** — Docker Compose prêt pour orchestration  
✅ **Robuste** — Retry logic, healthchecks, restart policies  
✅ **Bien documenté** — README, dossier technique, slides  
✅ **Testé** — E2E test script + validation manuelle  
✅ **UI Bonus** — Interface web via Nginx reverse proxy  

---

## 📅 Prêt pour Soutenance

**Date cible** : 2026-02-06  
**État** : ✅ **COMPLET ET VALIDÉ**

**Pour la démo :**
1. Exécuter `./reset.sh`
2. Attendre ~60 secondes
3. Accéder http://localhost:3000 (UI)
4. Tester prédictions
5. Montrer MLflow http://localhost:5000
6. Démontrer API Swagger http://localhost:8000/docs

---

**Créé par** : GitHub Copilot  
**Stack** : Docker Compose, PostgreSQL, FastAPI, MLflow, scikit-learn, Nginx  
**Durée dev** : Session unique optimisée  
