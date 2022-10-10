# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    termin = scrapy.Field()
    url = scrapy.Field()
