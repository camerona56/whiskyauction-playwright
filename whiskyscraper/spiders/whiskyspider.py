# import scrapy
# from scrapy_playwright.page import PageMethod
# from whiskyscraper.itemloaders import WhiskyItemLoader
# from whiskyscraper.items import WhiskyItem
# from playwright.sync_api import Playwright, sync_playwright, expect

# class WhiskyspiderSpider(scrapy.Spider):
#     name = 'whiskyspider'

#     def start_requests(self):
#         yield scrapy.Request(
#             url = 'https://whiskyauction.com/wac/whiskyBrowser/',
#             meta=dict(
#                 playwright=True,
#                 playwright_include_page=True,
#                 playwright_page_methods=[
#                     PageMethod('wait_for_selector', 'div.cardcontent-title'),
#                 ],
#                 current_page=1
#             ),
#             callback=self.parse
#         )

#     def parse(self, response):
#         bottles = response.css('div.cardcontent')

#         for bottle in bottles:
#             whisky = WhiskyItemLoader(item=WhiskyItem(), selector=bottle)
#             whisky.add_css('lot_title_1', 'div.cardcontent-title.cardcontent-description-title::text')
#             whisky.add_css('lot_title_2', 'div.cardcontent-description-text::text')
#             whisky.add_value('lot_title', whisky.get_output_value('lot_title_1') + ' ' + whisky.get_output_value('lot_title_2'))
#             whisky.add_css('lot_url', 'a.card-link::attr(href)')
#             whisky.add_css('auction_lot_id', 'a.card-link::attr(href)')
#             whisky.add_css('end_date', 'div.cardcontent-title.cardcontent-title-auction::text')
#             whisky.add_css('hammer_price', 'span[id^="card_current_high_bid"]::text')
#             yield whisky.load_item()










# import scrapy
# from scrapy_playwright.page import PageMethod
# from whiskyscraper.itemloaders import WhiskyItemLoader
# from whiskyscraper.items import WhiskyItem

# class WhiskyspiderSpider(scrapy.Spider):
#     name = 'whiskyspider'

#     def start_requests(self):
#         url = 'https://whiskyauction.com/wac/whiskyBrowser/'
#         yield scrapy.Request(url, meta=dict(
#             playwright=True,
#             playwright_include_page=True,
#             playwright_page_methods=[
#                 PageMethod('wait_for_selector', 'div.cardcontent-title'),
#             ],
#         ), callback=self.parse)

#     async def parse(self, response):
#         page = response.meta["playwright_page"]
#         # await page.close()

#         bottles = response.css('div.cardcontent')
#         for bottle in bottles:
#             whisky = WhiskyItemLoader(item=WhiskyItem(), selector=bottle)
#             whisky.add_css('lot_title_1', 'div.cardcontent-title.cardcontent-description-title::text')
#             whisky.add_css('lot_title_2', 'div.cardcontent-description-text::text')
#             whisky.add_value('lot_title', whisky.get_output_value('lot_title_1') + ' ' + whisky.get_output_value('lot_title_2'))
#             whisky.add_css('lot_url', 'a.card-link::attr(href)')
#             whisky.add_css('auction_lot_id', 'a.card-link::attr(href)')
#             whisky.add_css('end_date', 'div.cardcontent-title.cardcontent-title-auction::text')
#             whisky.add_css('hammer_price', 'span[id^="card_current_high_bid"]::text')
#             yield whisky.load_item()

#         await page.locator("#dt_whiskybrowser_next > .fa-solid").first.click()

#         await page.wait_for_selector('div.cardcontent-title')

#         yield scrapy.Request(
#             url=response.url,
#             meta=dict(
#                 playwright=True,
#                 playwright_include_page=True,
#                 playwright_page_methods=[
#                     PageMethod('wait_for_selector', 'div.cardcontent-title'),
#                 ],
#                 playwright_page=page  # Pass the page object to the next request
#             ),
#             callback=self.parse
        # )



import scrapy
from scrapy_playwright.page import PageMethod
from whiskyscraper.itemloaders import WhiskyItemLoader
from whiskyscraper.items import WhiskyItem

class WhiskyspiderSpider(scrapy.Spider):
    name = 'whiskyspider'
    start_urls = ['https://whiskyauction.com/wac/whiskyBrowser/']
    num_pages = 0

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div.cardcontent-title'),
                ],
            ),
            callback=self.parse
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        bottles = response.css('div.cardcontent')
        for bottle in bottles:
            whisky = WhiskyItemLoader(item=WhiskyItem(), selector=bottle)
            whisky.add_css('lot_title_1', 'div.cardcontent-title.cardcontent-description-title::text')
            whisky.add_css('lot_title_2', 'div.cardcontent-description-text::text')
            whisky.add_value('lot_title', whisky.get_output_value('lot_title_1') + ' ' + whisky.get_output_value('lot_title_2'))
            whisky.add_css('lot_url', 'a.card-link::attr(href)')
            whisky.add_css('auction_lot_id', 'a.card-link::attr(href)')
            whisky.add_css('end_date', 'div.cardcontent-title.cardcontent-title-auction::text')
            whisky.add_css('hammer_price', 'span[id^="card_current_high_bid"]::text')
            yield whisky.load_item()

        await page.locator("#dt_whiskybrowser_next > .fa-solid").first.click()

        if self.num_pages < 5:  # Adjust the number of pages to scrape here
            self.num_pages += 1
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
                callback=self.parse
            )
        # else:
        #     await page.close()



