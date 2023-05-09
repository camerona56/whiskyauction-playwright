import scrapy
from scrapy_playwright.page import PageMethod

class WhiskyspiderSpider(scrapy.Spider):
    name = 'whiskyspider'

    def start_requests(self):
        yield scrapy.Request('https://whiskyauction.com/wac/whiskyBrowser/', 
        meta= dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'div.cardcontent-title')
                ]
        )
        )

    async def parse(self, response):
        products = response.css('div.cardcontent')
        for item in products:
            yield {
            'lot_title': item.css('div.cardcontent-title.cardcontent-description-title::text').get().strip() + " " + item.css('div.cardcontent-description-text::text').get().strip(),
            'lot_url': item.css('a.card-link::attr(href)').get(),
            # 'auction_lot_id': response.css('').get(),
            'end_date': item.css('div.cardcontent-title.cardcontent-title-auction::text').get().replace('\n', '').strip(),
            'hammer_price': item.css('span[id^="card_current_high_bid"]::text').get()
            }

# import scrapy

# class WhiskyspiderSpider(scrapy.Spider):
#     name = 'whiskyspider'

#     def start_requests(self):
#         url = "https://quotes.toscrape.com/js/"
#         yield scrapy.Request(url, meta={'playwright': True})

#     async def parse(self, response):
#         yield {
#             'text': response.text
#         }