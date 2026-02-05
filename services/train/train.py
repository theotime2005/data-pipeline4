import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.data import from_pandas
from mlflow.tracking import MlflowClient
from mlflow.exceptions import MlflowException

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
    run_prefix = os.getenv("MLFLOW_RUN_PREFIX", "iris_sepal_regression")
    expected_rows = int(os.getenv("DATASET_EXPECTED_ROWS", "149"))
    n_estimators = int(os.getenv("MODEL_N_ESTIMATORS", "100"))

    engine = create_engine(f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}")
    wait_for(engine)

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(exp_name)

    client = MlflowClient()
    exp = mlflow.get_experiment_by_name(exp_name)
    if exp:
        runs = client.search_runs([exp.experiment_id], order_by=["attributes.start_time DESC"], max_results=5000)
        for run in runs:
            client.delete_run(run.info.run_id)
        if runs:
            print(f"Deleted {len(runs)} previous runs in experiment '{exp_name}'.")

    try:
        versions = client.search_model_versions(f"name='{model_name}'")
        for version in versions:
            client.delete_model_version(name=model_name, version=version.version)
        if versions:
            client.delete_registered_model(model_name)
            print(f"Removed existing registered model '{model_name}' before retraining.")
    except MlflowException as exc:
        # Ignore missing resources; re-raise other issues
        if getattr(exc, "error_code", None) != "RESOURCE_DOES_NOT_EXIST":
            raise

    df = pd.read_sql("SELECT sepal_length, sepal_width FROM iris_clean", engine)
    row_count = len(df)
    if row_count != expected_rows:
        print(f"⚠️ Dataset row count {row_count} differs from expected {expected_rows}.")
    run_name = f"{run_prefix}_{time.strftime('%Y%m%d_%H%M%S')}"

    X = df[["sepal_width"]]
    y = df["sepal_length"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run(run_name=run_name):
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("dataset_source", "iris.csv -> iris_clean table")
        mlflow.log_param("dataset_rows", row_count)

        dataset = from_pandas(df, name="iris_clean")
        mlflow.log_input(dataset, context="training")

        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=model_name)

        print("Training done.")
        print(f"MSE={mse:.4f} R2={r2:.4f}")
        print(f"Registered model name: {model_name}")

if __name__ == "__main__":
    main()
