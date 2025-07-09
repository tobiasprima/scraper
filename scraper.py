import argparse
import asyncio
import logging
import os
import time

from playwright.async_api import async_playwright
from scrape_classes.books import BooksToScrape

def setup_logger(name, log_file, level=logging.DEBUG):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

async def run_with_retries(scraping_class, retries, logger):
    for attempt in range(retries):
        try:
            logger.info(f"[{scraping_class.site_name}] Attempt {attempt + 1}")
            await scraping_class.scrape()
            logger.info(f"[{scraping_class.site_name}] Success")
            return
        except Exception as e:
            logger.warning(f"[{scraping_class.site_name}] Error: {e}")
            if attempt == retries - 1:
                logger.error(f"[{scraping_class.site_name}] Failed after {retries} attempts")
                raise

async def full_run(case_id: str, max_tries: int, store_dir: str, logger):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=250)
        start = time.time()

        try:
            logger.info("Browser launched")

            scraping_classes = [
                BooksToScrape(case_id),
                # Add other scrapers here if needed
            ]

            for cls in scraping_classes:
                await cls.async_init(browser)

            tasks = [
                asyncio.create_task(run_with_retries(cls, max_tries, logger))
                for cls in scraping_classes
            ]

            await asyncio.gather(*tasks)
            logger.info(f"Scraping completed in {time.time() - start:.2f} seconds.")

        finally:
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case_id", type=str, required=True, help="Unique ID for the case")
    parser.add_argument("--max_tries", type=int, default=2, help="Number of retries per site")
    args = parser.parse_args()

    store_dir = os.path.join(os.getcwd(), "scrape_output/" f"{args.case_id}")
    os.makedirs(store_dir, exist_ok=True)
    os.chdir(store_dir)

    logger = setup_logger("scraper", f"{args.case_id}.log")

    asyncio.run(full_run(args.case_id, args.max_tries, store_dir, logger))
