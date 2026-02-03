CREATE TABLE IF NOT EXISTS iris_clean (
  id SERIAL PRIMARY KEY,
  sepal_length DOUBLE PRECISION,
  sepal_width DOUBLE PRECISION,
  petal_length DOUBLE PRECISION,
  petal_width DOUBLE PRECISION,
  species TEXT
);
