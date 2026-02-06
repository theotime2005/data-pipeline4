import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.preprocessing import StandardScaler

def wait_for_db(engine, retries=30, delay=2):
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception:
            time.sleep(delay)
    raise RuntimeError("DB not reachable")

def main():
    db = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    pwd = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")

    engine = create_engine(f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}")
    wait_for_db(engine)

    df = pd.read_csv("iris.csv")
    # Normalize column names: lowercase, no spaces, no dots
    df.columns = [c.strip().lower().replace(" ", "_").replace(".", "_") for c in df.columns]

    required = {"sepal_length", "sepal_width", "petal_length", "petal_width", "species"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}. Found: {df.columns.tolist()}")

    # Simple cleaning: drop rows with nulls or duplicates
    df = df.dropna().drop_duplicates()

    scaler = StandardScaler()
    numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    _ = scaler.fit_transform(df[numeric_cols])

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE iris_clean RESTART IDENTITY;"))

    df.to_sql("iris_clean", engine, if_exists="append", index=False)
    print(f"Inserted {len(df)} rows into iris_clean")

if __name__ == "__main__":
    main()
