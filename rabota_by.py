import scrapy
from scrapy.http import HtmlResponse
from project_parser_hh.items import ProjectParserHhItem
import re
from unicodedata import normalize


class RabotaBySpider(scrapy.Spider):
    name = 'rabota_by'
    allowed_domains = ['rabota.by']
    start_urls = ['https://rabota.by/search/vacancy?text=python&salary=&clusters=true&area=1002&no_magic=true&ored_clusters=true&items_on_page=20&enable_snippets=true']
    
    def parse(self, response:HtmlResponse):
      next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
      if next_page:
        yield response.follow(next_page, callback=self.parse)
      urls_vacancies = response.xpath("//a[@class='serp-item__title']/@href").getall()
      for url_vacancy in urls_vacancies:
        yield response.follow(url_vacancy, callback=self.vacancy_parse)
       
    
    def vacancy_parse(self, response: HtmlResponse):
      vacancy_name = response.css("h1::text").get()
      vacancy_url = response.url
      vacancy_salary =  response.xpath("//span[@data-qa='vacancy-salary-compensation-type-net']//text()").getall()
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
          salary_upto=vacancy_salary_upto,            
          salary_from=vacancy_salary_from,
          url=vacancy_url
        )
