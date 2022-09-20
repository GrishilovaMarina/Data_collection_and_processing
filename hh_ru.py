from operator import index
import scrapy
from scrapy.http import HtmlResponse
from project_parser_hh.items import ProjectParserHhItem
from unicodedata import normalize


class HhRuSpider(scrapy.Spider):

    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://spb.hh.ru/search/vacancy?area=76&search_field=name&search_field=company_name&search_field=description&text=python&no_magic=true&L_save_area=true&items_on_page=20',
        'https://spb.hh.ru/search/vacancy?area=88&search_field=name&search_field=company_name&search_field=description&text=python&no_magic=true&L_save_area=true&items_on_page=20'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
          yield response.follow(next_page, callback=self.parse)
        urls_vacancies = response.xpath("//div[@class='serp-item']//a[@data-qa='serp-item__title']/@href").getall()
        for url_vacancy in urls_vacancies:
          yield response.follow(url_vacancy, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//h1/text()").get()
        vacancy_salary =  response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        if 'от ' in vacancy_salary and ' до ' in vacancy_salary:
          vacancy_salary_from = normalize('NFKD', (vacancy_salary[vacancy_salary.index('от ') + 1]))
          vacancy_salary_upto = normalize('NFKD', (vacancy_salary[vacancy_salary.index(' до ') + 1]))
        elif 'от ' in vacancy_salary and not ' до ' in vacancy_salary:
          vacancy_salary_from = normalize('NFKD', (vacancy_salary[vacancy_salary.index('от ') + 1]))
          vacancy_salary_upto = 'не указана'
        elif 'до ' in vacancy_salary and not 'от ' in vacancy_salary:
          vacancy_salary_upto = normalize('NFKD', (vacancy_salary[vacancy_salary.index('до ') + 1]))
          vacancy_salary_from = 'не указана'
        else:
          vacancy_salary_upto, vacancy_salary_from = 'не указана', 'не указана'
        vacancy_url = response.url

        yield ProjectParserHhItem(
            name=vacancy_name,
            salary_from=vacancy_salary_from,
            salary_upto=vacancy_salary_upto,
            url=vacancy_url
          )
