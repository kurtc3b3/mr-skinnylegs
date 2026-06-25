FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md alembic.ini ./
COPY alembic ./alembic
COPY src ./src

RUN uv sync --frozen --no-dev

ENV API_HOST=0.0.0.0
ENV API_PORT=8100

EXPOSE 8100

CMD ["uv", "run", "scraper-api"]
