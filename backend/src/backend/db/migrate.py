import os
import subprocess
import sys
from pathlib import Path

from sqlmodel import Session

from backend.db.engine import engine, seed_sources

BACKEND_ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    subprocess.run(
        ["alembic", "upgrade", "head"],
        check=True,
        cwd=BACKEND_ROOT,
    )
    with Session(engine) as session:
        seed_sources(session)
    print("Migrations applied and scraper sources seeded.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
