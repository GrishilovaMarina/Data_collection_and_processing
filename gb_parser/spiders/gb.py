import scrapy
from scrapy.http import HtmlResponse
from lxml import html
from gb_parser.items import GbItem


class GbSpider(scrapy.Spider):
    allowed_domains = ['gb.ru']
    start_urls = ['https://gb.ru/']
    login_link = 'https://gb.ru/login'
    login_ = 'mabemi6344@oncebar.com'
    pwd = 'test1234'
    name = 'gb'
    post_hashe = 'js.dbde4izh76hch97qwyhhxa.hr7tvwb1ckqaiehvjoiunc'

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            'https://gb.ru/login/',
            method='POST',
            callback=self.login,
            formdata={
                'utf8': '✓',
                'authenticity_token': self.post_hashe,
                'user_email': self.login_,
                'user_password': self.pwd})

    def login(self, response: HtmlResponse):
        if response.text.find('Моё обучение'):
            print('АВТОРИЗАЦИЯ ПРОШЛА УСПЕШНО!!!')
            yield response.follow('https://gb.ru/courses/all', callback=self.parse_programms)

    def parse_programms(self, response: HtmlResponse):
        info_programm = response.xpath("//div[@class='uni-card new-d w-dyn-item']").getall()
        print(f'ВСЕГО СЧИТАНО - {len(info_programm)} ПОГРАММ ОБУЧЕНИЯ')

        for prog in info_programm:
            dom = html.fromstring(prog)
            url_programm = dom.xpath("..//a[@class='product_card_link w-inline-block']/@href")[0]
            name_programm = dom.xpath("..//div[@class='product_title new-d']/text()")[0]
            termin_programm = dom.xpath("..//div[@class='product_detail new-d']/text()")[0]

            yield GbItem(
                name=name_programm,
                termin=termin_programm,
                url=url_programm
            )
