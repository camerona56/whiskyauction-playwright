import scrapy
from scrapy_playwright.page import PageMethod
from whiskyscraper.itemloaders import WhiskyItemLoader
from whiskyscraper.items import WhiskyItem

class WhiskyspiderSpider(scrapy.Spider):
    name = 'whiskyspider'
    start_urls = ['https://whiskyauction.com/wac/whiskyBrowser']
    start_page = 500
    num_pages = 1

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div.cardcontent-title'),
                    PageMethod('click', '#paginate_input_top'),
                    PageMethod('fill', '#paginate_input_top', str(self.start_page)),
                    PageMethod('press', '#paginate_input_top', 'Enter'),
                    PageMethod('wait_for_selector', 'div.cardcontent-title')
                ],
            ),
            callback=self.parse,
            dont_filter = True
        )
    
    async def parse(self, response):
        page = response.meta["playwright_page"]

        bottles = response.css('div.cardcontent')
        for bottle in bottles:
            whisky = WhiskyItemLoader(item=WhiskyItem(), selector=bottle)
            whisky.add_css('lot_title_1', 'div.cardcontent-title.cardcontent-description-title::text')
            whisky.add_css('lot_title_2', 'div.cardcontent-description-text')
            whisky.add_value('lot_title', whisky.get_output_value('lot_title_1') + ' ' + whisky.get_output_value('lot_title_2'))
            whisky.add_css('lot_url', 'a.card-link::attr(href)')
            whisky.add_css('auction_lot_id', 'a.card-link::attr(href)')
            whisky.add_css('end_date', 'div.cardcontent-title.cardcontent-title-auction::text')
            whisky.add_css('hammer_price', 'span[id^="card_current_high_bid"]::text')
            whisky.add_css('auction_name', 'div.cardcontent-title.cardcontent-title-auction::text')
            whisky.add_value('auction_url', 'https://whiskyauction.com/wac/whiskyBrowser')
            yield whisky.load_item()

        self.num_pages += 1

        if self.num_pages < self.start_page + 2:  # Adjust the number of pages to scrape here - (3 scrapes 2 pages)
            await page.locator("#dt_whiskybrowser_next > .fa-solid").first.click()
              
            await page.wait_for_selector('div.cardcontent-title')

            # Pass the updated playwright_page object to the next request
            yield scrapy.Request(
                url=page.url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', 'div.cardcontent-title'),
                    ],
                    playwright_page=page
                ),
                callback=self.parse,
                dont_filter=True
            )    
        else:
            await page.close()



# page.locator("#paginate_input_top").click()
# page.locator("#paginate_input_top").fill("500")


        # page.locator("#paginate_input_top").click()
        # page.locator("#paginate_input_top").fill("500")
        # page.wait_for_selector('div.cardcontent-title')





    # page.goto("https://whiskyauction.com/wac/whiskyBrowser")
    # page.get_by_role("button", name="Auction ").click()
    # page.get_by_role("button", name="Auction ").click()
    # page.get_by_role("button", name=" Show results").click()
    # page.goto("https://whiskyauction.com/wac/whiskyBrowser#card-item-null")
    # page.locator("div").filter(has_text=re.compile(r"^2023-06$")).first.click()


# page.get_by_role("button", name="Auction ").click()
# page.locator("div").filter(has_text=re.compile(r"^2023-06$")).first.click()
# page.get_by_role("button", name=" Show results").click()

