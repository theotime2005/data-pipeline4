import pandas as pd
import psycopg2
import time

print("🚀 Démarrage du preprocessing...")

# Attendre que PostgreSQL soit prêt
time.sleep(5)

# Connexion à PostgreSQL
conn = psycopg2.connect(
    host="postgres",
    database="iris_db",
    user="iris_user",
    password="iris_password"
)

cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS iris (
    sepal_length FLOAT,
    sepal_width FLOAT,
    petal_length FLOAT,
    petal_width FLOAT,
    species TEXT
);
""")

# Charger le CSV
df = pd.read_csv("/data/iris.csv")

# Renommer les colonnes
df.columns = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "species"
]

# Supprimer les données existantes
cursor.execute("DELETE FROM iris;")

# Insertion ligne par ligne
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO iris (sepal_length, sepal_width, petal_length, petal_width, species)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            row["sepal_length"],
            row["sepal_width"],
            row["petal_length"],
            row["petal_width"],
            row["species"],
        )
    )

conn.commit()
cursor.close()
conn.close()

print(f"✅ {len(df)} lignes insérées dans PostgreSQL")
print("✅ Prétraitement terminé")
