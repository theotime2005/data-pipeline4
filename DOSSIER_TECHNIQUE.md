# Dossier technique — Pipeline Iris (Prévision sepal_length depuis sepal_width)

Date : 2026-02-02
Auteurs : équipe projet (3–4 étudiants)

## 1. Contexte et objectif
Le labo souhaite estimer la longueur des sépales (`sepal_length`) à partir de leur largeur (`sepal_width`) pour automatiser l'analyse de spécimens Iris. Le livrable attend un pipeline dockerisé incluant prétraitement, base PostgreSQL, entraînement avec suivi MLflow, et API REST pour la prédiction.

## 2. Vue d'ensemble de l'architecture

Flux principal :

```
iris.csv
  ↓
preprocess (Python)  --> write --> PostgreSQL (iris_clean)
  ↓
train (Python + scikit-learn) --> log model & metrics --> MLflow (backend=Postgres, artifacts=/mlruns)
  ↓
api (FastAPI) --> charge modèle depuis MLflow --> /predict
```

Composants (Docker Compose) : `db` (Postgres), `mlflow`, `preprocess`, `train`, `api`.
Volumes persistants : `pgdata` (Postgres), `mlruns` (artefacts MLflow).

## 3. Choix techniques
- Orchestration : Docker Compose (simplicité, reproductibilité pour soutenance).
- Base : PostgreSQL 16 (persist), initialisation via `db/init.sql`.
- Tracking : MLflow 2.15.1, backend-store-uri = Postgres, artifact-root = `file:///mlruns`.
- Langage : Python 3.11, bibliothèques : pandas, SQLAlchemy, scikit-learn, mlflow, FastAPI.
- Modèle : RandomForestRegressor (implémentation scikit-learn) — choix initial simple et robuste.

Raisons : rapidité d'intégration, disponibilité des libs, MLflow facilite l'enregistrement/versioning des modèles.

## 4. Données et prétraitement
- Source : `iris.csv` (150 observations, 5 colonnes : sepal_length, sepal_width, petal_length, petal_width, species).
- Étapes Preprocess (service `preprocess`):
  - Chargement CSV (monté en volume pour respecter build context).
  - Nettoyage : suppression NA, doublons.
  - Normalisation/StandardScaler appliquée aux features numériques selon besoin.
  - Insertion dans la table `iris_clean` de la DB.

## 5. Modélisation
- Pipeline : extraction depuis Postgres → split (par défaut train/test interne) → entraînement RandomForestRegressor.
- Hyperparamètres : n_estimators = 200 (valeur par défaut dans le code actuel).
- Enregistrement : modèle + métriques (MSE, R²) loggés dans MLflow et artefacts (pickle) placés sous `/mlruns`.

Métriques observées (exécution actuelle) :
- Exemple d'un run : MSE = 1.0957, R² = -0.6086 (valeurs issues des logs d'entraînement).

Remarque : ces métriques montrent une performance faible / aberrante (R² négatif). Sources possibles : choix d'une seule feature (`sepal_width`) pour prédire `sepal_length`, absence de split/validation correct, ou erreur dans préparation/features.

## 6. Déploiement et API
- API : FastAPI exposant `/health` et `/predict`.
- Startup : l'API implémente une boucle de retry (configurable via `API_MODEL_LOAD_RETRIES`, `API_MODEL_LOAD_DELAY`) pour attendre que le modèle soit enregistré et disponible dans MLflow.
- Lorsque le modèle est chargé, `POST /predict` accepte JSON {"sepal_width": float} et renvoie la prédiction.
- Tests manuels et script `scripts/e2e_test.sh` automatisent la validation end‑to‑end.

## 7. Observations et diagnostics (problèmes rencontrés et corrections)
1. Preprocess Dockerfile tentait de `COPY` `iris.csv` hors du build context → corrigé en montant `./iris.csv:/app/iris.csv:ro` dans `docker-compose.yml`.
2. MLflow `--default-artifact-root` mal formé initialement → changé en `file:///mlruns`.
3. API échouait au démarrage si le modèle n'était pas encore enregistré → ajouté retry loop et rendu `mlruns` partageable entre `train`, `mlflow`, et `api`.
4. Permissions : initialement `api` montait `mlruns` en read-only, ce qui empêchait MLflow/loader d'écrire certains fichiers temporaires → mis en read-write pour `api` (ajustable selon politique sécurité).

## 8. Analyse critique & pistes d'amélioration
- Modèle et features
  - Utiliser plusieurs features (sepal_width, petal_length, petal_width) pour améliorer la prédiction.
  - Ajouter split train/validation (k-fold), recherche d'hyperparamètres (GridSearchCV) et enregistrement du meilleur modèle.
  - Standardiser/normaliser de façon cohérente et persister le pipeline de preprocessing (scikit-learn Pipeline) pour production.
- Robustesse & infra
  - Ajouter `healthcheck` et `restart` policies dans `docker-compose.yml` pour services critiques (mlflow, api).
  - Exposer `API_MODEL_LOAD_RETRIES`/`API_MODEL_LOAD_DELAY` dans `.env` pour paramétrage sans rebuild.
  - Mieux gérer permissions du volume `mlruns` (utilisateurs non-root, ACL) pour sécurité en production.
- Observabilité & CI
  - Ajouter tests unitaires et pipeline CI (ex: GitHub Actions) qui exécutent `scripts/e2e_test.sh` sur PR.
  - Collecte de logs structurés, métriques système et alerting pour la soutenance avancée.
- Déploiement
  - Ajouter endpoint de rechargement du modèle à chaud (webhook) ou mécanisme de watch sur `mlruns`.
  - Si besoin, containeriser une UI simple (HTML/JS) pour soumettre valeurs `sepal_width` depuis navigateur.

## 9. Répartition du travail (proposition)
- Étudiant A : Preprocess & ingestion DB, tests de données
- Étudiant B : Entraînement, logging MLflow, design modèle
- Étudiant C : API & déploiement, intégration MLflow → API
- Étudiant D (optionnel) : Documentation, slides, script e2e et CI

## 10. Reproductibilité & commandes
- Build et lancement :

```bash
docker compose up --build
```

- Reset propre :

```bash
docker compose down -v --remove-orphans
docker compose up --build
```

- Test e2e automatique :

```bash
./scripts/e2e_test.sh
```

## 11. Annexes
- Fichiers importants : `docker-compose.yml`, `services/preprocess/preprocess.py`, `services/train/train.py`, `services/api/main.py`, `scripts/e2e_test.sh`, `db/init.sql`, `iris.csv`.
- Points à documenter dans la soutenance : montrer MLflow UI (expériences + artefacts), démonstration `/predict` via Swagger et script e2e.

---

Fin du dossier technique (version initiale).