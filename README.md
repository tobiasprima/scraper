# Async Web Scraper with Playwright (Python)

This project demonstrates a clean and modular **asynchronous web scraper** built using [Playwright](https://playwright.dev/python/).
---

## 🚀 Features

-  Asynchronous scraping with `asyncio` + `playwright.async_api`
-  Modular object-oriented design using a reusable `Website` base class
-  Built-in retry logic
-  Structured JSON output with runtime metadata
-  Robust logging to file
-  Ready for scraping real websites like:
  -  [Books to Scrape](http://books.toscrape.com/) (demonstration)
---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/async-playwright-scraper.git
cd async-playwright-scraper
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt

```

### 4. Install Playwright browser binaries
```bash
playwright install
```
