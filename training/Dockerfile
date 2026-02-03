FROM python:3.10-slim

WORKDIR /app

COPY train.py .

RUN pip install pandas psycopg2-binary scikit-learn mlflow==2.10.2

CMD ["python", "train.py"]