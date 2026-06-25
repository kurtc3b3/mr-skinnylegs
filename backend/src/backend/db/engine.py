from sqlmodel import Session, create_engine, select

from backend.core.config import settings
from backend.models import ScraperSource

engine = create_engine(settings.database_url)

DEFAULT_SOURCES = [
    {
        "name": "NBC News",
        "slug": "nbc_news",
        "base_url": "https://www.nbcnews.com",
        "description": "NBC News crawl4ai scraper",
    },
    {
        "name": "BBC News",
        "slug": "bbc_news",
        "base_url": "https://www.bbc.com/news",
        "description": "BBC News crawl4ai scraper",
    },
    {
        "name": "PriceSpy",
        "slug": "pricespy_device",
        "base_url": "https://www.pricespy.co.uk",
        "description": "PriceSpy product pages",
    },
    {
        "name": "Wikipedia",
        "slug": "wikipedia",
        "base_url": "https://en.wikipedia.org",
        "description": "Wikipedia article scraper",
    },
]


def seed_sources(session: Session) -> None:
    for source in DEFAULT_SOURCES:
        exists = session.exec(
            select(ScraperSource).where(ScraperSource.slug == source["slug"])
        ).first()
        if exists:
            continue
        session.add(ScraperSource(**source))
    session.commit()
