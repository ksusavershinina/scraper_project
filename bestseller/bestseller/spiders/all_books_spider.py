import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BookSpider(CrawlSpider):
    name = 'all_books'
    start_urls = ['https://www.livelib.ru/']

    rules = (
        Rule(LinkExtractor(allow='books')),
        Rule(LinkExtractor(allow='book'), callback='parse_items'),
    )

    def parse_items(self, response):
        yield {
            'title': response.css('h1.bc__book-title::text').get(),
            'isbn': response.css('div.bc-info__wrapper p span::text').getall()[0],
        }