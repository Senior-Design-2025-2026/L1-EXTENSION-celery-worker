FROM python:3.12-slim-bookworm

WORKDIR /celery_worker

COPY L1-EXTENSION-celery-worker/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY L1-EXTENSION-postgres-orm/db_orm.py ./src/
COPY L1-EXTENSION-celery-worker/src ./src/

RUN groupadd -g 1000 celerygroup \
    && useradd -m -u 1000 -g 1000 celeryuser \
    && chown -R celeryuser:celerygroup /celery_worker

USER celeryuser

# CMD ["celery", "-A", "src.celery_app.celery_app", "worker", "--loglevel=info"]
CMD ["celery", "-A", "src.celery_app.celery_app", "worker"]
