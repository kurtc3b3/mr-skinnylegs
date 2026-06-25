# Scraper Backend

crawl4ai scrapers plus a **FastAPI + SQLAdmin** service for tracking scrape sources and runs in PostgreSQL.

## Quick start

```bash
cd backend
cp .env.template .env
docker compose up --build
```

- **Admin UI:** http://localhost:8100/admin (`admin` / `changethis` from `.env`)
- **API health:** http://localhost:8100/api/health

Local dev without Docker:

```bash
docker compose up db -d   # Postgres on localhost:5433
# set POSTGRES_PORT=5433 in .env when using host port mapping
uv sync
uv run scraper-migrate
uv run scraper-api
```

## Scraper tracking from scripts

Wrap a crawl with `track_run` to persist status, timing, and errors:

```python
from backend.tracking import track_run

async def crawl_nbc_news(url: str):
    with track_run("nbc_news", url) as run:
        # ... crawl logic ...
        run.output_path = str(output_file)
        run.items_scraped = 1
```

Default sources (`nbc_news`, `bbc_news`, `pricespy_device`, `wikipedia`) are seeded on migrate.

## Layout

```
src/backend/
  api/server.py      # FastAPI app
  admin/             # SQLAdmin views
  models.py          # scraper_source, scraper_run
  tracking.py        # track_run() helper
  news/              # crawl4ai scrapers
  ecommerce/
  wikipedia/
alembic/             # migrations
docker-compose.yml   # postgres + api
```

## Note on fastapi-admin

The [`fastapi-admin`](https://github.com/fastapi-admin/fastapi-admin) package requires Tortoise ORM. This project uses **SQLModel/SQLAlchemy**, so we use **[SQLAdmin](https://github.com/smithyhq/sqladmin)** — the matching admin UI for this stack.
