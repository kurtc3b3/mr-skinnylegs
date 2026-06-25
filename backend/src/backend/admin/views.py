from sqladmin import ModelView

from backend.models import ScraperRun, ScraperSource


class ScraperSourceAdmin(ModelView, model=ScraperSource):
    name = "Scraper Source"
    name_plural = "Scraper Sources"
    icon = "fa-solid fa-spider"

    column_list = [
        ScraperSource.id,
        ScraperSource.name,
        ScraperSource.slug,
        ScraperSource.is_active,
        ScraperSource.base_url,
        ScraperSource.created_at,
    ]
    column_searchable_list = [ScraperSource.name, ScraperSource.slug]
    column_sortable_list = [ScraperSource.name, ScraperSource.created_at]
    form_columns = [
        ScraperSource.name,
        ScraperSource.slug,
        ScraperSource.base_url,
        ScraperSource.description,
        ScraperSource.is_active,
    ]


class ScraperRunAdmin(ModelView, model=ScraperRun):
    name = "Scraper Run"
    name_plural = "Scraper Runs"
    icon = "fa-solid fa-list-check"

    column_list = [
        ScraperRun.id,
        ScraperRun.source_id,
        ScraperRun.status,
        ScraperRun.url,
        ScraperRun.items_scraped,
        ScraperRun.duration_ms,
        ScraperRun.started_at,
        ScraperRun.finished_at,
        ScraperRun.output_path,
        ScraperRun.created_at,
    ]
    column_searchable_list = [ScraperRun.url, ScraperRun.status, ScraperRun.output_path]
    column_sortable_list = [
        ScraperRun.status,
        ScraperRun.created_at,
        ScraperRun.started_at,
        ScraperRun.finished_at,
    ]
    column_default_sort = [(ScraperRun.created_at, True)]
    form_columns = [
        ScraperRun.source_id,
        ScraperRun.url,
        ScraperRun.status,
        ScraperRun.started_at,
        ScraperRun.finished_at,
        ScraperRun.items_scraped,
        ScraperRun.duration_ms,
        ScraperRun.output_path,
        ScraperRun.error_message,
        ScraperRun.notes,
    ]
