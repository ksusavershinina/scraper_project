import scrapy

class BookSpider(scrapy.Spider):
    name = 'livelib'
    start_urls = ['https://www.livelib.ru/']

    def parse(self, response):
        for link in response.css('a.slide-book__link::attr(href)'):
            yield response.follow(link, callback=self.parse_book)


    def parse_book(self, response):
        yield {
            'title': response.css('h1.bc__book-title::text').get(),
            'year': response.css('div.bc-info__wrapper p::text').getall()[1][13:],
            'isbn': response.css('span[itemprop="isbn"]::text').get()
        }


# response.css("a.slide-book__link::attr(href)").get()