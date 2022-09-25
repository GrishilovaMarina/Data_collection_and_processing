# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst

def format_price(value):
  try:
    value = float(value[0].replace(' ', ''))
  except:
    return value
  return value

def format_data(value):
  value = value.replace('\n', '').strip()
  return value

class GoodsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name_goods = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field()
    price = scrapy.Field(input_processor=Compose(format_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    specifications_key = scrapy.Field(input_processor=MapCompose(format_data))
    specifications_value = scrapy.Field(input_processor=MapCompose(format_data))
    specifications = scrapy.Field()

    _id = scrapy.Field()
