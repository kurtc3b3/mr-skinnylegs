import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
    CrawlResult
)
from pathlib import Path

output_dir = Path("output") / "pricespy_device"
output_dir.mkdir(parents=True, exist_ok=True)


async def crawl_pricespy_device(url: str):
    browser_config = BrowserConfig(
        headless=False,
        verbose=True,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        crawler_config = CrawlerRunConfig(
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter()
            ),
        )
        result: CrawlResult = await crawler.arun(
            url=url, config=crawler_config
        )
        with open(output_dir / f"{url.split('/')[-1]}.md", "w") as f:
            f.write(result.markdown.fit_markdown)

if __name__ == "__main__":
    asyncio.run(crawl_pricespy_device("https://pricespy.co.uk/product.php?p=14969878"))
