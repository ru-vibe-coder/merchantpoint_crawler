import scrapy


class MerchantpointCrawlerItem(scrapy.Item):
    merchant_name = scrapy.Field()      # Название точки
    mcc = scrapy.Field()                # MCC код
    address = scrapy.Field()            # Адрес (необязательный)
    geo_coordinates = scrapy.Field()    # Координаты (необязательные)
    org_name = scrapy.Field()           # Название организации
    org_description = scrapy.Field()    # Описание организации
    source_url = scrapy.Field()         # Ссылка на источник