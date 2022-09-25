import scrapy
from scrapy.http import HtmlResponse
from goods_scraper.items import GoodsScraperItem
from scrapy.loader import ItemLoader
from pprint import pprint


class CastoramaRuSpider(scrapy.Spider):
    name = 'castorama_ru'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/heating-water-supply-and-ventilation/fireplaces/fireplace-sets']

    def parse(self, response:HtmlResponse):
      links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
      for link in links:
        yield response.follow(link, callback=self.parse_good)
    def parse_good(self, response:HtmlResponse):
      loader = ItemLoader(item=GoodsScraperItem(), response=response)
      loader.add_xpath('name_goods', "//h1/text()")
      loader.add_value('url', response.url)
      loader.add_xpath('price', "//div[@class='add-to-cart__price js-fixed-panel-trigger']//span[@class='price']/span/span/text()")
      loader.add_xpath('photos', "//img[@class='top-slide__img swiper-lazy']/@data-src")
      loader.add_xpath('specifications_key', "//div[@class='product-block product-specifications']//span/text()")
      loader.add_xpath('specifications_value', "//div[@class='product-block product-specifications']//dd/text()")
      yield loader.load_item()
      #specifications_key= response.xpath("//div[@class='product-block product-specifications']//span/text()").getall()
      #specifications_value= response.xpath("//div[@class='product-block product-specifications']//dd/text()").getall()
      #print(specifications_key)
      #print(specifications_value)
     



