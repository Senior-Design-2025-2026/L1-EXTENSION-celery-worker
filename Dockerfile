FROM astral/uv:python3.12-bookworm-slim
WORKDIR /web

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY app ./app

# same image, but different command for the worker
CMD [uv, run, celery, -A, app.app.celery_app, worker, -l, info]

