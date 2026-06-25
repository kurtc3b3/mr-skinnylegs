from fastapi import FastAPI
from sqladmin import Admin

from backend.admin.auth import get_admin_auth
from backend.admin.views import ScraperRunAdmin, ScraperSourceAdmin
from backend.core.config import settings
from backend.db.engine import engine


def setup_admin(app: FastAPI) -> Admin:
    admin = Admin(
        app,
        engine,
        authentication_backend=get_admin_auth(),
        base_url="/admin",
        title="Scraper Tracking Admin",
    )
    admin.add_view(ScraperSourceAdmin)
    admin.add_view(ScraperRunAdmin)
    return admin
