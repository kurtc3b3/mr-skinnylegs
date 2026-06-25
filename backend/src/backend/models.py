import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ScraperSource(SQLModel, table=True):
    __tablename__ = "scraper_source"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=128)
    slug: str = Field(unique=True, index=True, max_length=64)
    base_url: str | None = Field(default=None, max_length=2048)
    description: str | None = Field(default=None, max_length=512)
    is_active: bool = True
    created_at: datetime | None = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    runs: list["ScraperRun"] = Relationship(back_populates="source", cascade_delete=True)


class ScraperRun(SQLModel, table=True):
    __tablename__ = "scraper_run"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_id: uuid.UUID = Field(
        foreign_key="scraper_source.id", nullable=False, ondelete="CASCADE"
    )
    url: str = Field(max_length=2048)
    status: str = Field(default="pending", max_length=32, index=True)
    started_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    finished_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    error_message: str | None = Field(default=None, max_length=4096)
    output_path: str | None = Field(default=None, max_length=1024)
    items_scraped: int = Field(default=0)
    duration_ms: int | None = None
    notes: str | None = Field(default=None, max_length=1024)
    created_at: datetime | None = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    source: ScraperSource | None = Relationship(back_populates="runs")
