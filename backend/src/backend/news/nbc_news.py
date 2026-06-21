from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, CosineStrategy
import asyncio
import json
from pathlib import Path
from structlog import get_logger

logger = get_logger()

output_dir = Path("output") / "nbc_news"
output_dir.mkdir(parents=True, exist_ok=True)


async def crawl_nbc_news(url: str):
    crawl_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        exclude_external_images=True,
        extraction_strategy=CosineStrategy(
            word_count_threshold=10,
            max_dist=0.2,  # Maximum distance between two words
            linkage_method="ward",  # Linkage method for hierarchical clustering (ward, complete, average, single)
            top_k=3,  # Number of top keywords to extract
            sim_threshold=0.3,  # Similarity threshold for clustering
            semantic_filter="McDonald's economic impact, American consumer trends",  # Keywords to filter the content semantically using embeddings
            verbose=True,
        ),
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=crawl_config,
        )
        logger.info(f"Extracted content length: {len(result.extracted_content)}", url=url, crawler_config=crawl_config)
        with open(output_dir / f"{url.split('/')[-1]}.json", "w") as f:
            f.write(json.dumps(json.loads(result.extracted_content), indent=4))
        logger.info(f"Extracted content saved to {output_dir / f"{url.split('/')[-1]}.json"}", url=url, crawler_config=crawl_config)

        for img in result.media["images"][:5]:
            logger.info(f"Image URL: {img['src']}, Alt: {img['alt']}, Score: {img['score']}", url=url, crawler_config=crawl_config)

if __name__ == "__main__":
    asyncio.run(crawl_nbc_news("https://www.nbcnews.com/business/consumer/how-mcdonalds-e-coli-crisis-inflation-politics-reflect-american-story-rcna177156"))
