"""Initial scraper tracking tables

Revision ID: 001_scraper
Revises:
Create Date: 2026-06-25

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


revision = "001_scraper"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scraper_source",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=128), nullable=False),
        sa.Column("slug", sqlmodel.sql.sqltypes.AutoString(length=64), nullable=False),
        sa.Column("base_url", sqlmodel.sql.sqltypes.AutoString(length=2048), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=512), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scraper_source_slug"), "scraper_source", ["slug"], unique=True)

    op.create_table(
        "scraper_run",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("source_id", sa.Uuid(), nullable=False),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(length=2048), nullable=False),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sqlmodel.sql.sqltypes.AutoString(length=4096), nullable=True),
        sa.Column("output_path", sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=True),
        sa.Column("items_scraped", sa.Integer(), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("notes", sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["scraper_source.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scraper_run_status"), "scraper_run", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_scraper_run_status"), table_name="scraper_run")
    op.drop_table("scraper_run")
    op.drop_index(op.f("ix_scraper_source_slug"), table_name="scraper_source")
    op.drop_table("scraper_source")
