import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import time

# Attendre que PostgreSQL soit prêt
time.sleep(5)

# Connexion PostgreSQL
conn = psycopg2.connect(
    host="postgres",
    database="iris_db",
    user="iris_user",
    password="iris_password"
)

query = "SELECT sepal_width, sepal_length FROM iris;"
df = pd.read_sql(query, conn)
conn.close()

X = df[["sepal_width"]]
y = df["sepal_length"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Iris Sepal Length Prediction")

with mlflow.start_run():
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5

    r2 = r2_score(y_test, y_pred)

    mlflow.log_param("model_type", "RandomForestRegressor")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    mlflow.sklearn.log_model(model, "model")

print("✅ Modèle entraîné et enregistré dans MLflow")
