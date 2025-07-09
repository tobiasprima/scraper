from scrape_classes.website import Website

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

        for book in books[:5]:  # scrape first 5
            title = await book.query_selector_eval("h3 a", "el => el.title")
            price = await book.query_selector_eval(".price_color", "el => el.textContent")
            results.append({"title": title, "price": price})

        self.JSON_FILE["books"] = results
        await self.save_JSON_FILE()