import scrapy
from merchantpoint_crawler.items import MerchantpointCrawlerItem


class BrandsSpider(scrapy.Spider):
    name = 'brands_by_id'
    allowed_domains = ['merchantpoint.ru']

    def start_requests(self):
        for brand_id in range(1, 500):  # тестовый диапазон
            url = f'https://merchantpoint.ru/brand/{brand_id}'
            yield scrapy.Request(url, callback=self.parse_org)

    def parse_org(self, response):
        if response.status == 404:
            return

        org_name = response.xpath('//h1[@class="text-3xl md:text-4xl font-bold mb-3"]/text()').get()
        org_description = response.xpath(
            '//div[@class="company-info"]/h1/text()'
        ).get()

        if not org_description:
            org_description = response.xpath(
                '//section[@id="description"]//div[contains(@class, "description_brand")]//text()[normalize-space()][1]'
            ).get()

        if org_description:
            org_description = org_description.strip()

        # Теперь обрабатываем таблицу точек прямо на этой странице
        rows = response.xpath('//table[@class="finance-table"]/tbody/tr')
        for row in rows:
            point_item = MerchantpointCrawlerItem()
            point_item['mcc'] = row.xpath('./td[1]/text()').get()
            point_item['merchant_name'] = row.xpath('./td[2]/a/text()').get()
            address = row.xpath('./td[3]/text()').get()
            point_item['address'] = address.strip() if address else None
            point_item['geo_coordinates'] = None
            point_item['org_name'] = org_name
            point_item['org_description'] = org_description
            point_item['source_url'] = response.url
            yield point_item
