const puppeteer = require("puppeteer");

const TARGET_URL = process.argv[2] || "https://quotes.toscrape.com/";

async function scrape(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.goto(url, { waitUntil: "networkidle2", timeout: 30_000 });

    const data = await page.evaluate(() => {
      const quotes = [...document.querySelectorAll(".quote")].map((quote) => ({
        text: quote.querySelector(".text")?.textContent?.trim() ?? "",
        author: quote.querySelector(".author")?.textContent?.trim() ?? "",
        tags: [...quote.querySelectorAll(".tag")].map((tag) => tag.textContent.trim()),
      }));

      return {
        title: document.title,
        url: location.href,
        quoteCount: quotes.length,
        quotes,
      };
    });

    console.log(JSON.stringify(data, null, 2));
    return data;
  } finally {
    await browser.close();
  }
}

scrape(TARGET_URL).catch((error) => {
  console.error("Scrape failed:", error.message);
  process.exit(1);
});
