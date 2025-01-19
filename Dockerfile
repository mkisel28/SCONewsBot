FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml \
    uv.lock ./

# Development stage
FROM builder AS dev

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --frozen --extra dev

ENV PATH="/app/.venv/bin:$PATH"

COPY . /app

