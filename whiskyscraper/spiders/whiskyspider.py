import scrapy
from scrapy_playwright.page import PageMethod
from whiskyscraper.itemloaders import WhiskyItemLoader
from whiskyscraper.items import WhiskyItem
# from playwright.sync_api import sync_playwright

class WhiskyspiderSpider(scrapy.Spider):
    name = 'whiskyspider'

    def start_requests(self):
        yield scrapy.Request('https://whiskyauction.com/wac/whiskyBrowser/', 
        meta= dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'div.cardcontent-title'),
                ]
        )
        )

    async def parse(self, response):
      bottles = response.css('div.cardcontent')

      for bottle in bottles:
            whisky = WhiskyItemLoader(item=WhiskyItem(), selector=bottle)
            # whisky.add_css('lot_title', 'div.cardcontent-title.cardcontent-description-title::text').get().strip() + " " + item.css('div.cardcontent-description-text::text').get().strip(),
            whisky.add_css('lot_title_1', 'div.cardcontent-title.cardcontent-description-title::text'),
            whisky.add_css('lot_title_2', 'div.cardcontent-description-text::text'),
            whisky.add_value('lot_title', whisky.get_output_value('lot_title_1') + ' ' + whisky.get_output_value('lot_title_2')),
            whisky.add_css('lot_url', 'a.card-link::attr(href)'),
            whisky.add_css('auction_lot_id', 'a.card-link::attr(href)'),
            whisky.add_css('end_date', 'div.cardcontent-title.cardcontent-title-auction::text'),
            whisky.add_css('hammer_price', 'span[id^="card_current_high_bid"]::text'),
            yield whisky.load_item()

      # with sync_playwright() as pw:
      #   browser = pw.chromium.launch(headless=False)
      #   page = browser.new_page()
      #   page.set_content(response.body, wait_until="networkidle")
      #   next_page = page.locator(".next")