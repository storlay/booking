FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY . .

RUN chmod +x ./infra/commands/*.sh