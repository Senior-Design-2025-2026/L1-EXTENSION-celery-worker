FROM python:3.12-slim-bookworm
WORKDIR /celery_worker

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY src ./src
CMD ["python", "src/celery_app.py"]

