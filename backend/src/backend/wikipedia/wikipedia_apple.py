from crawl4ai import (
    AsyncWebCrawler,
    CacheMode,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
)
import asyncio
from pathlib import Path

output_dir = Path("output") / "wikipedia"
output_dir.mkdir(parents=True, exist_ok=True)


async def crawl_wikipedia(url: str):
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["nav", "footer", "aside"],
        remove_overlay_elements=True,
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.48, threshold_type="fixed", min_word_threshold=0
            ),
            options={"ignore_links": True},
        ),
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=crawler_config,
        )
        with open(output_dir / f"{url.split('/')[-1]}.md", "w") as f:
            f.write(result.markdown.fit_markdown)

if __name__ == "__main__":
    asyncio.run(crawl_wikipedia("https://en.wikipedia.org/wiki/Apple"))
