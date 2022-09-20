# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectParserHhItem(scrapy.Item):
    name = scrapy.Field()
    salary_from = scrapy.Field()
    salary_upto = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
