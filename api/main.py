from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
import pandas as pd

app = FastAPI(title="Iris Sepal Length Prediction API")

# Config MLflow
mlflow.set_tracking_uri("http://mlflow:5000")
EXPERIMENT_NAME = "Iris Sepal Length Prediction"

# Charger le dernier modèle
def load_latest_model():
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["attributes.start_time DESC"],
        max_results=1
    )

    run_id = runs[0].info.run_id
    model_uri = f"runs:/{run_id}/model"
    return mlflow.sklearn.load_model(model_uri)

model = load_latest_model()

# Schéma d'entrée
class PredictRequest(BaseModel):
    sepal_width: float

@app.post("/predict")
def predict(data: PredictRequest):
    df = pd.DataFrame([[data.sepal_width]], columns=["sepal_width"])
    prediction = model.predict(df)[0]
    return {"predicted_sepal_length": float(prediction)}
