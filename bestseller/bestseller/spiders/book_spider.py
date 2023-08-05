import scrapy
import re

# TODO: пристроить куда то запись в бд/файл???


class BookSpider(scrapy.Spider):
    name = 'livelib'
    start_urls = ['https://www.livelib.ru/find']
    def parse(self, response):
        a = ['978-5-6044767-4-1',
             '978-5-6044767-7-2',
             '978-5-9500341-0-7',
             '978-9934-8753-1-1',
             '978-5-600-01715-3']
        #TODO: как сделать так, чтобы мы шли по исбн и названиям? надо ыпихнуть так, чтобы везде шло. стоит ли исполь-оавть meta?
        for isbn, title in a:
            link = f"https://www.livelib.ru/find/{isbn}"
            yield response.follow(link, callback=self.parse_page, meta={'title': title})


    def parse_page(self, response):
        book_link = response.css('div.find-book-block a::attr(href)').getall()

        if len(book_link) == 1:
            yield response.follow(book_link[0], callback=self.parse_book)
        elif len(book_link) == 0:
            pass
        elif len(book_link) > 1:
            book_title = response.css('div.find-book-block a.find-book-name::text').getall()
            for title, i in book_title:
                #TODO: форматирование/валидация названия???
                if title in response.meta['title']:
                    yield response.follow(book_link[i], callback=self.parse_book)
                else:
                    pass



    def parse_book(self, response):
        # description = response.css('div#lenta-card__text-edition-full').get()

        description = response.css('div#lenta-card__text-edition-escaped::text').get()
        #TODO: как получить полное описание???
        if description:
            description = description.strip()
            description = re.sub(r'\s+', ' ', description)

            yield {
                'description': description
            }
        else:
            yield {
                'description' : '-'
            }


# response.css("a.slide-book__link::attr(href)").get()

 # response.css('div#lenta-card__text-edition-escaped::text').get()