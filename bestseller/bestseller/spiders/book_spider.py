import scrapy
import re

class BookSpider(scrapy.Spider):
    name = 'livelib'
    start_urls = ['https://www.livelib.ru/find']
    def parse(self, response):
        a = ['978-5-6044767-4-1',
             '978-5-6044767-7-2',
             '978-5-9500341-0-7',
             '978-9934-8753-1-1',
             '978-5-600-01715-3']
        for isbn in a:
            link = f"https://www.livelib.ru/find/{isbn}"
            yield response.follow(link, callback=self.parse_book)


    def parse_book(self, response):
        description = response.css('div#lenta-card__text-edition-escaped::text').get()
        description = description.strip()
        description = re.sub(r'\s+', ' ', description)

        yield {
            'description': description
        }


# response.css("a.slide-book__link::attr(href)").get()

 # response.css('div#lenta-card__text-edition-escaped::text').get()