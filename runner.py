from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from project_parser_hh.spiders.hh_ru import HhRuSpider
from project_parser_hh.spiders.rabota_by import RabotaBySpider


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()

    runner = CrawlerRunner(settings)
    runner.crawl(HhRuSpider)
    runner.crawl(RabotaBySpider)
    
    reactor.run()