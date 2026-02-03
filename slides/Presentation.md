# Présentation — Pipeline Iris

---

# Titre

Pipeline Dockerisé pour prédire la longueur des sépales (Iris)

- Équipe : 3–4 étudiants
- Soutenance : 06/02/2026

---

# Objectif

Automatiser l'estimation de `sepal_length` à partir de `sepal_width`.
Concevoir un pipeline reproductible et observable utilisant Docker, PostgreSQL et MLflow.

---

# Architecture — Vue globale

- `preprocess` : charge `iris.csv`, nettoie, normalise, écrit en PostgreSQL
- `train` : lit la table, entraîne RandomForest, enregistre dans MLflow
- `mlflow` : UI + Model Registry (backend=Postgres, artifacts=/mlruns)
- `api` : FastAPI qui charge le modèle et expose `/predict`

(Schéma simple à afficher sur la slide)

---

# Choix techniques

- Docker Compose pour orchestration (simplicité pour la soutenance)
- PostgreSQL pour persistance (initialisation via `db/init.sql`)
- MLflow (traçage + registry)
- FastAPI pour l'API (docs Swagger intégrées)
- RandomForestRegressor (scikit-learn) comme baseline

---

# Flux de démonstration (ordre)

1. Lancer : `docker compose up --build`
2. Ouvrir MLflow UI : `http://localhost:5000` — montrer expérience et artefacts
3. Ouvrir Swagger : `http://localhost:8000/docs` — tester `/predict`
4. Exécuter script e2e : `./scripts/e2e_test.sh` (valide pipeline end-to-end)

---

# Résultats & métriques

- Exemple de métriques (run actuel) :
  - MSE = 1.0957
  - R² = -0.6086

Remarque : ces valeurs indiquent une performance faible — expliquer limite (1 feature seulement).

---

# Analyse critique

- Points faibles : features insuffisantes, pipeline de preprocessing non persisté (scaler non sérialisé), métriques à améliorer.
- Améliorations proposées : utiliser plusieurs features, pipeline scikit-learn, GridSearchCV, CI et tests, endpoint reload modèle.

---

# Répartition du travail

- A : Preprocess & ingestion DB
- B : Training & MLflow
- C : API & déploiement
- D : Docs, tests e2e, slides

---

# Démo live

- Montrer MLflow (run, artefacts)
- Lancer une prédiction via Swagger
- Lancer `./scripts/e2e_test.sh` (montre reproductibilité)

---

# Q&A

Fin de la présentation.
