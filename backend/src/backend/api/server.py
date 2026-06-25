import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.admin import setup_admin
from backend.api.routes import router
from backend.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Scraper API", version="0.1.0")
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
    app.include_router(router, prefix="/api")
    setup_admin(app)
    return app


app = create_app()


def run() -> None:
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    uvicorn.run(
        "backend.api.server:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=reload,
    )


if __name__ == "__main__":
    run()
