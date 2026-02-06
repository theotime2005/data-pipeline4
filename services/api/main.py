import os
import time
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Iris Sepal Length Predictor")

# Allow UI to call the API from browser; allow all origins for debugging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class PredictIn(BaseModel):
    sepal_width: float

def load_latest_model():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    model_name = os.getenv("MODEL_NAME", "iris_sepal_length_regressor")

    mlflow.set_tracking_uri(tracking_uri)

    try:
        client = mlflow.tracking.MlflowClient()
        versions = client.search_model_versions(f"name='{model_name}'")
        if not versions:
            raise RuntimeError("No model versions found. Run training first.")
        latest = sorted(versions, key=lambda v: int(v.version))[-1]
        model_uri = f"models:/{model_name}/{latest.version}"
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        raise RuntimeError(str(e))

MODEL = None

@app.on_event("startup")
def startup_event():
    global MODEL
    # Retry loop: wait for the training job to register a model in MLflow
    retries = int(os.getenv("API_MODEL_LOAD_RETRIES", "30"))
    delay = int(os.getenv("API_MODEL_LOAD_DELAY", "3"))
    for i in range(retries):
        try:
            MODEL = load_latest_model()
            print(f"✅ Model loaded successfully (attempt {i+1})")
            return
        except Exception as e:
            print(f"⏳ Model not available yet ({i+1}/{retries}): {e}")
            if i < retries - 1:
                time.sleep(delay)
    # If still not loaded after retries, API still starts but model=None
    print("⚠️ Model not loaded after retries; API will accept requests but /predict will fail")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: PredictIn):
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        df = pd.DataFrame([{"sepal_width": payload.sepal_width}])
        y = MODEL.predict(df)
        return {"sepal_width": payload.sepal_width, "sepal_length_pred": float(y[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.options("/{full_path:path}")
def options_handler(full_path: str):
    """Handle preflight CORS requests."""
    return {"status": "ok"}


@app.post('/reload')
def reload_model():
    """Force reload the latest model from MLflow (synchronous)."""
    global MODEL
    try:
        MODEL = load_latest_model()
        return {"status": "reloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
