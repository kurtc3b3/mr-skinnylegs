from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode
)
import asyncio
from pathlib import Path
from structlog import get_logger

logger = get_logger()

output_dir = Path("output") / "bbc_news"
output_dir.mkdir(parents=True, exist_ok=True)


async def crawl_bbc_news(url: str):
    browser_config = BrowserConfig(headless=True, browser_type="chromium")
    # firefox, webkit
    crawler_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, screenshot=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=crawler_config)
        logger.info(f"Markdown length: {len(result.markdown)}", url=url, crawler_config=crawler_config)

        if result.success and result.screenshot:
            import base64

            screenshot_data = base64.b64decode(result.screenshot)
            with open(output_dir / f"{url.split('/')[-1]}.png", "wb") as f:
                f.write(screenshot_data)
            logger.info(f"Screenshot saved successfully to {output_dir / f"{url.split('/')[-1]}.png"}", url=url, crawler_config=crawler_config)
        else:
            logger.error("Failed to capture screenshot", url=url, crawler_config=crawler_config)

if __name__ == "__main__":
    asyncio.run(crawl_bbc_news("https://www.bbc.co.uk/news/business"))
