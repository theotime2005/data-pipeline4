# Scénario de démonstration (script)

1. Préparer l'environnement (machine avec Docker)

```bash
cd /workspaces/data-pipeline4
./scripts/e2e_test.sh
```

2. Vérifier manuellement (si besoin)

```bash
# MLflow UI
open http://localhost:5000

# Swagger
open http://localhost:8000/docs
```

3. Commandes utiles pour la soutenance

```bash
# Logs en temps réel
docker compose logs -f mlflow
docker compose logs -f api

# Repartir d'un état propre
docker compose down -v --remove-orphans
docker compose up --build
```

Notes:
- Le script e2e montre que le pipeline s'exécute entièrement et que `/predict` renvoie 200.
- Si `/predict` renvoie 400 ou 500 : consulter `docker compose logs api` et `docker compose logs train`.
