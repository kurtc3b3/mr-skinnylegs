"""Helpers for scraper scripts to record runs in Postgres."""

from __future__ import annotations

import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterator

from sqlmodel import Session, select

from backend.db.engine import engine
from backend.models import ScraperRun, ScraperSource


def get_source_id(session: Session, slug: str) -> uuid.UUID:
    source = session.exec(select(ScraperSource).where(ScraperSource.slug == slug)).first()
    if not source:
        raise ValueError(f"Unknown scraper source slug: {slug}")
    return source.id


@dataclass
class RunTracker:
    run_id: uuid.UUID
    output_path: str | None = None
    items_scraped: int = 0
    notes: str | None = None
    _started: float = field(default_factory=time.perf_counter, repr=False)

    def _save(self, *, status: str, error_message: str | None = None) -> None:
        with Session(engine) as session:
            run = session.get(ScraperRun, self.run_id)
            if run is None:
                return
            run.status = status
            run.output_path = self.output_path
            run.items_scraped = self.items_scraped
            run.notes = self.notes
            run.error_message = error_message
            run.finished_at = datetime.now(timezone.utc)
            run.duration_ms = int((time.perf_counter() - self._started) * 1000)
            session.add(run)
            session.commit()


@contextmanager
def track_run(slug: str, url: str) -> Iterator[RunTracker]:
    """Context manager: creates a run row, marks success/failure on exit."""
    with Session(engine) as session:
        run = ScraperRun(
            source_id=get_source_id(session, slug),
            url=url,
            status="running",
            started_at=datetime.now(timezone.utc),
        )
        session.add(run)
        session.commit()
        session.refresh(run)
        tracker = RunTracker(run_id=run.id)

    try:
        yield tracker
        tracker._save(status="success")
    except Exception as exc:
        tracker._save(status="failed", error_message=str(exc)[:4096])
        raise
