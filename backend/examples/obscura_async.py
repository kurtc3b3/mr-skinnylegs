import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()
        await page.goto("https://quotes.toscrape.com")
        quotes = await page.eval_on_selector_all(
            "div.quote",
            "els => els.map(el => el.querySelector('span.text').innerText)",
        )
        print(quotes)
        await browser.close()

asyncio.run(main())
