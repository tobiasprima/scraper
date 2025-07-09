from website import Website
from datetime import datetime

class BooksToScrape(Website):
    site_name = "books_to_scrape"

    def __init__(self, case_id, address=None):
        super().__init__()
        self.case_number = case_id
        self.address = address
        self.JSON_FILE["Site Name"] = self.site_name
        self.JSON_FILE["Case Number"] = case_id
        self.JSON_FILE["start_time"] = str(datetime.now())

    async def scrape(self):
        page = await self.context.new_page()
        await page.goto("http://books.toscrape.com/")

        books = await page.query_selector_all(".product_pod")
        results = []

        for book in books[:5]:
            title_el = await book.query_selector("h3 a")
            price_el = await book.query_selector(".price_color")

            title = await title_el.get_attribute("title") if title_el else "N/A"
            price = await price_el.text_content() if price_el else "N/A"

            results.append({"title": title.strip(), "price": price.strip()})

        self.JSON_FILE["books"] = results
        await self.save_JSON_FILE()
