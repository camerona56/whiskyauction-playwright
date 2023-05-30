from datetime import datetime
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class WhiskyItemLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    lot_title_1_in = MapCompose(lambda x : x.strip())
    lot_title_2_in = MapCompose(lambda x : x.replace('<div class=\"cardcontent-description-text\">', '').replace('<br>', ' ').replace('</div>', '').strip())
    lot_title_in = MapCompose(lambda x : x.strip())
    lot_url_in = MapCompose(lambda x : 'https://whiskyauction.com' + x)
    auction_lot_id_in = MapCompose(lambda x : x.replace('/item/', ''))
    auction_name_in = MapCompose(lambda x : x.strip())
    hammer_price_in = MapCompose(lambda x : int(x))
    end_date_in = MapCompose(lambda x : datetime.strptime(x.replace('2023-06', '27.05.23').replace('2023-05', '30.04.23').replace('2023-04', '01.04.23').replace('2022-11', '12.11.22').strip(), '%d.%m.%y'))