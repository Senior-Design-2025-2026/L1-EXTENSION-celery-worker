FROM python:3.12-slim-bookworm
WORKDIR /celery_worker

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt 

COPY src ./src
CMD ["celery", "-A", "src.celery_app.celery_app", "worker", "--loglevel=info"]

