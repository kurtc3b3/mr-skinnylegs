"""Async HTTP fetching with AsyncFetcher."""

import asyncio

from scrapling.fetchers import AsyncFetcher


async def scrape_page(url: str):
    page = await AsyncFetcher.get(url)
    return [
        {
            "text": quote.css("span.text::text").get(""),
            "author": quote.css("small.author::text").get(""),
        }
        for quote in page.css("div.quote")
    ]


async def scrape_pages_concurrently():
    urls = [
        "https://quotes.toscrape.com",
        "https://quotes.toscrape.com/page/2/",
    ]
    results = await asyncio.gather(*(scrape_page(url) for url in urls))
    return [item for page_items in results for item in page_items]


async def main():
    # Single async request
    page = await AsyncFetcher.get("https://quotes.toscrape.com")
    print("status:", page.status)
    print("first quote:", page.css("span.text::text").get())

    # Fetch multiple pages in parallel
    print("\nconcurrent scrape:")
    for item in await scrape_pages_concurrently():
        print(f"  {item['author']}: {item['text'][:50]}...")


if __name__ == "__main__":
    asyncio.run(main())
