# Puppeteer scraper example

A minimal Node.js scraper that uses [Puppeteer](https://pptr.dev/) to load a page in headless Chrome and extract structured data.

## Setup

```bash
cd puppet-app
npm install
```

## Run

Default target is [quotes.toscrape.com](https://quotes.toscrape.com/):

```bash
npm run scrape
```

Scrape a custom URL:

```bash
node scraper.js https://example.com
```

Output is printed as JSON to stdout.

## PDF export

Render a page to PDF with `page.pdf()`:

```bash
npm run pdf
```

Custom URL and output path:

```bash
node pdf.js https://example.com output/example.pdf
```

The default output is `output/page.pdf`.
