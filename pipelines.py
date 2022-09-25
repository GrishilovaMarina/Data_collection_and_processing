# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import hashlib
from os.path import splitext
import os
from urllib.parse import urlparse


class GoodsScraperPipeline:
    def process_item(self, item, spider):
      item['specifications'] = dict(zip(item['specifications_key'], item['specifications_value']))
      return item

class CastoramaPhotosPipeline(ImagesPipeline):
  def get_media_requests(self, item, info):
    if item['photos']:
      for img in item['photos']:
        try:
          yield Request(img)
        except Exception as e:
          print(e)

  def item_completed(self, results, item, info):
    item['photos'] = [itm[1] for itm in results if itm[0]]
    return item

  def file_path(self, request, response=None, info=None, *, item=None):
    image_filename = ''.join(request.url.split('_')[1])
    return str(image_filename + '/' + os.path.basename(urlparse(request.url).path))
