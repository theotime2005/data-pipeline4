# 📋 Checklist Soutenance 2026-02-06

## ✅ Avant la Présentation

### Infrastructure
- [ ] Exécuter `./reset.sh` pour démarrage propre
- [ ] Attendre le message "Stack is ready!" (~60s)
- [ ] Tester `curl http://localhost:8000/health` → retour `{"status":"ok"}`
- [ ] Vérifier que http://localhost:3000 est accessible (UI web)

### Accès Préalable
- [ ] Ouvrir 3 onglets navigateur :
  - [ ] http://localhost:3000 (UI - utiliser pour démo)
  - [ ] http://localhost:8000/docs (API documentation)
  - [ ] http://localhost:5000 (MLflow UI)
- [ ] Garder terminal ouvert pour `docker compose logs -f`

---

## 🎬 Pendant la Présentation

### Démo 1 : Interface Web (2 min)
- [ ] Montrer http://localhost:3000 (interface prédiction)
- [ ] Entrer `sepal_width = 3.5` et cliquer "Predict"
- [ ] Montrer la réponse : `sepal_length_pred ≈ 5.08`
- [ ] Essayer plusieurs valeurs (3.0, 4.0, 5.0)
- [ ] Vérifier en console du navigateur (aucune erreur CORS)

### Démo 2 : Architecture (3 min)
- [ ] Ouvrir http://localhost:5000 (MLflow)
- [ ] Naviguer vers "Models" → iris_sepal_length_regressor
- [ ] Montrer les métriques (MSE, R², accuracy)
- [ ] Montrer les artefacts (modèle RandomForest)
- [ ] Expliquer la persistance des données

### Démo 3 : API (2 min)
- [ ] Ouvrir http://localhost:8000/docs (Swagger)
- [ ] Tester `/health` endpoint (GET)
- [ ] Tester `/predict` endpoint (POST) avec 3.5
- [ ] Afficher la réponse JSON

### Démo 4 : Données & DB (1 min)
- [ ] Terminal : `docker compose exec db psql -U iris -d irisdb -c "SELECT COUNT(*) FROM iris_clean;"`
- [ ] Montrer le nombre de lignes (150)
- [ ] Montrer que les données sont persisted (ils ont survécu aux redémarrages)

### Démo 5 : Logs (1 min)
- [ ] Terminal : `docker compose logs api --tail 20`
- [ ] Montrer les logs de prédictions récentes
- [ ] Expliquer le retry logic au startup

---

## 🛑 Troubleshooting Rapide

### Problème : Port 3000/8000 occupé
```bash
lsof -i :3000
kill -9 <PID>
./reset.sh
```

### Problème : Services ne démarrent pas
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Problème : Modèle non chargé
```bash
# Attendre 30-60s, vérifier les logs
docker compose logs api | grep "Model loaded"
```

### Problème : DB vide
```bash
# Vérifier que preprocess a tourné
docker compose logs preprocess
# Vérifier init.sql
docker compose exec db psql -U iris -d irisdb -c "\dt"
```

---

## 📊 Métriques à Montrer

- **Modèle** : RandomForestRegressor (100 estimators)
- **MSE (Mean Squared Error)** : Affichée sur MLflow
- **R² Score** : Affichée sur MLflow (0.8+)
- **Données d'entraînement** : 150 samples (iris dataset)
- **Feature** : sepal_width
- **Target** : sepal_length
- **Prédictions** : sepal_length_pred (float)

---

## 🗣️ Points de Discussion

### Architecture
> "Le pipeline utilise Docker Compose pour orchestrer 6 services :
> - PostgreSQL pour la persistance
> - Preprocess pour le nettoyage (ETL)
> - Train pour l'entraînement ML
> - MLflow pour le tracking d'expériences
> - API FastAPI pour les prédictions
> - UI Nginx comme reverse proxy"

### Robustesse
> "L'API inclut une retry logic (30 tentatives) pour attendre que le modèle
> soit disponible dans MLflow. Les volumes persists les données entre redémarrages."

### Scalabilité
> "Docker Compose peut être remplacé par Kubernetes en production.
> Les Dockerfiles sont optimisés (multi-stage builds si besoin).
> MLflow scale via PostgreSQL backend."

### Innovations
> "Bonus : Interface web statique servie via Nginx, qui agit comme
> reverse proxy pour l'API. Cela simule un vrai environnement production."

---

## 📄 Livrables à Mentionner

- ✅ Code source complet (GitHub-ready)
- ✅ Documentation technique (DOSSIER_TECHNIQUE.md)
- ✅ Support de présentation (Presentation.pptx)
- ✅ Tests E2E (scripts/e2e_test.sh)
- ✅ Script de reset (reset.sh)
- ✅ Dockerfile optimisés
- ✅ docker-compose.yml orchestration-ready

---

## ⏱️ Timing Estimé

- Setup : 2 min (./reset.sh)
- Présentation globale : 2 min
- Démo UI : 2 min
- Démo MLflow : 2 min
- Démo API : 2 min
- Démo DB : 1 min
- Discussion/Questions : 5 min
- **Total : ~16 minutes**

---

## 🎯 Ce à Éviter

❌ Ne pas redémarrer les services pendant la démo (stick à un reset.sh au début)  
❌ Ne pas parler trop bas (microphone activé)  
❌ Ne pas cliquer "Predict" 50 fois (max 5-6 fois)  
❌ Ne pas afficher de credentials en plain-text à l'écran  
❌ Ne pas oublier d'expliquer WHY c'est dockerisé (portabilité, reproductibilité)

---

## ✨ Points Clés à Retenir

1. **Pipeline complet** : De csv à API, 100% automatisé
2. **Traceable** : MLflow enregistre toutes les expériences
3. **Robuste** : Retry logic, healthchecks, restart policies
4. **Scalable** : Dockerisé, prêt pour production
5. **Bien documenté** : README, dossier technique, slides

---

**Bonne chance pour la soutenance ! 🎓**

---

## Commandes Rapides à Copier/Coller

```bash
# Reset complet
./reset.sh

# Quick demo
./DEMO_QUICK.sh

# View logs
docker compose logs -f api

# Test endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_width": 3.5}'

# Query database
docker compose exec db psql -U iris -d irisdb -c "SELECT * FROM iris_clean LIMIT 5;"

# Stop everything
docker compose down

# Clean everything
docker compose down -v
```
