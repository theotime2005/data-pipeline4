import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn

def wait_for(engine, query="SELECT 1", retries=40, delay=2):
    for _ in range(retries):
        try:
            with engine.connect() as c:
                c.execute(text(query))
            return
        except Exception:
            time.sleep(delay)
    raise RuntimeError("Service not reachable")

def main():
    db = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    pwd = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    exp_name = os.getenv("MLFLOW_EXPERIMENT_NAME", "iris-sepal-regression")
    model_name = os.getenv("MODEL_NAME", "iris_sepal_length_regressor")

    engine = create_engine(f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}")
    wait_for(engine)

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(exp_name)

    df = pd.read_sql("SELECT sepal_length, sepal_width FROM iris_clean", engine)
    X = df[["sepal_width"]]
    y = df["sepal_length"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        model = RandomForestRegressor(n_estimators=200, random_state=42)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_param("n_estimators", 200)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=model_name)

        print("Training done.")
        print(f"MSE={mse:.4f} R2={r2:.4f}")
        print(f"Registered model name: {model_name}")

if __name__ == "__main__":
    main()
