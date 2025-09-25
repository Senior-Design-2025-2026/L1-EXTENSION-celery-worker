FROM python:3.12-slim-bookworm

WORKDIR /celery_worker

COPY L1-celery-worker/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY L1-sqlalchemy-orm/db_orm.py ./src/
COPY L1-celery-worker/src ./src/

RUN groupadd -g 1000 celerygroup \
    && useradd -m -u 1000 -g 1000 celeryuser \
    && chown -R celeryuser:celerygroup /celery_worker

USER celeryuser

# this defaults to --concurrency=N as default (ex my mac has 8 cores -> 8 workers, pi has 4... max of 4 workers, but also running 4 containers. this could be f'd)
CMD ["celery", "-A", "src.celery_app.celery_app", "worker", "--loglevel=info"]

