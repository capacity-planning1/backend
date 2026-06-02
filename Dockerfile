FROM ghcr.io/astral-sh/uv:0.11.7 AS uv

FROM python:3.13-slim-bookworm AS builder

ENV PYTHON_VERSION=3.13 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

COPY pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-install-project


FROM python:3.13-slim-bookworm AS runtime

ENV PYTHON_VERSION=3.13 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH=/app/.venv/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --create-home app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

COPY --chown=app:app alembic ./alembic
COPY --chown=app:app app ./app
COPY --chown=app:app alembic.ini ./

USER app

CMD ["gunicorn", "-c", "app/core/gunicorn_confing.py", "app.main:app"]
