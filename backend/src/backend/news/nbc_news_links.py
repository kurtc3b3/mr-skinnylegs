from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
import asyncio


async def link_analysis():
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        exclude_external_links=True,
        exclude_social_media_links=True,
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            config=crawler_config,
        )
        print(f"Found {len(result.links['internal'])} internal links")
        print(f"Found {len(result.links['external'])} external links")

        for link in result.links["internal"][:5]:
            print(f"Href: {link['href']}\nText: {link['text']}\n")

if __name__ == "__main__":
    asyncio.run(link_analysis())
