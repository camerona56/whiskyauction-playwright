from datetime import datetime
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class WhiskyItemLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    lot_title_1_in = MapCompose(lambda x : x.strip())
    lot_title_2_in = MapCompose(lambda x : x.strip())
    lot_title_in = MapCompose(lambda x : x.strip())
    lot_url_in = MapCompose(lambda x : 'https://whiskyauction.com' + x)
    auction_lot_id_in = MapCompose(lambda x : x.replace('/item/', ''))
    end_date_in = MapCompose(lambda x : x.strip())
    hammer_price_in = MapCompose(lambda x : int(x))
    # end_date_in = MapCompose(lambda x : datetime.strptime(x.replace('133rd-auction', '10.07.22').split('/', 1)[0], '%d.%m.%y'))