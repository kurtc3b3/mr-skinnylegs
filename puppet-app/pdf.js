const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const TARGET_URL = process.argv[2] || "https://quotes.toscrape.com/";
const OUTPUT_PATH =
  process.argv[3] || path.join(__dirname, "output", "page.pdf");

async function savePdf(url, outputPath) {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.goto(url, { waitUntil: "networkidle2", timeout: 30_000 });

    await page.pdf({
      path: outputPath,
      format: "A4",
      printBackground: true,
      margin: { top: "20mm", right: "15mm", bottom: "20mm", left: "15mm" },
    });

    console.log(`Saved PDF: ${outputPath}`);
    return outputPath;
  } finally {
    await browser.close();
  }
}

savePdf(TARGET_URL, OUTPUT_PATH).catch((error) => {
  console.error("PDF export failed:", error.message);
  process.exit(1);
});
