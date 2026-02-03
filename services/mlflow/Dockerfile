FROM python:3.11-slim

WORKDIR /mlruns

# Install MLflow and dependencies
RUN pip install --no-cache-dir mlflow==2.15.1 psycopg2-binary==2.9.9

# Create startup script that uses environment variables
RUN mkdir -p /app
COPY --chmod=755 entrypoint.sh /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

