import scrapy

class BookSpider(scrapy.Spider):
    name = 'livelib'
    start_urls = ['https://www.livelib.ru/genre/%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/best/listview/biglist']

    def parse(self, response):
        for link in response.css('a.brow-book-name.with-cycle::attr(href)'):
            yield response.follow(link, callback=self.parse_book)

        for i in range (1, 11):
            next_page = f'https://www.livelib.ru/genre/%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/best/listview/biglist/~{i}'
            yield response.follow(next_page, callback=self.parse)


    def parse_book(self, response):
        yield {
            'title': response.css('h1.bc__book-title::text').get(),
            'year': response.css('div.bc-info__wrapper p::text').getall()[1][13:],
            'isbn': response.css('span[itemprop="isbn"]::text').get()
        }

