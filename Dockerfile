FROM python:3.12-slim-bookworm

WORKDIR /celery_worker

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../L1-sqlachemy-database ./src
COPY src ./src

RUN groupadd -g 1000 celerygroup \
    && useradd -m -u 1000 -g 1000 celeryuser \
    && chown -R celeryuser:celerygroup /celery_worker

USER celeryuser

CMD ["celery", "-A", "src.celery_app.celery_app", "worker", "--loglevel=info"]
