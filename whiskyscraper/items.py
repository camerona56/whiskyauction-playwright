from scrapy import Item, Field

class WhiskyItem(Item):
    lot_title_1 = Field()
    lot_title_2 = Field()
    lot_title = Field()
    lot_url = Field()
    auction_lot_id = Field()
    end_date = Field()
    hammer_price = Field()