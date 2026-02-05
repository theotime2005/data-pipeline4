FROM python:3.11-slim

WORKDIR /mlruns

# Install MLflow and dependencies
RUN pip install --no-cache-dir mlflow==2.15.1 psycopg2-binary==2.9.9

# Create startup script that uses environment variables
RUN mkdir -p /app
COPY entrypoint.sh /app/entrypoint.sh
# Normalize line endings in case the file was edited on Windows
RUN sed -i 's/\r$//' /app/entrypoint.sh && \
    chmod 755 /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

