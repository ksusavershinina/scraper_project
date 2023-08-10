import scrapy
import re

class BookSpider(scrapy.Spider):
    name = 'livelib_test'
    allowed_domains = ['livelib.ru']
    start_urls = ['https://www.livelib.ru/find']

    custom_headers = {
        'Accept': '/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.livelib.ru/book/1000835130-rossiya-v-evrope-po-materialam-mezhdunarodnogo-proekta-evropejskoe-sotsialnoe-issledovanie',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'no-cahce',
        'Content-Length': '268',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.188',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        isbn_massiv = ['978-5-6044767-4-1']
        for isbn in isbn_massiv:
            link = f"https://www.livelib.ru/find/{isbn}"
            yield scrapy.Request(url=link, callback=self.parse_page, headers=self.custom_headers)

    def parse_page(self, response):
        book_links = response.css('.find-book-block a::attr(href)').getall()
        # надо приписать условия на 0 и больше 1 книги
        for book_link in book_links:
            yield response.follow(url=book_link, callback=self.parse_book)

    def parse_book(self, response):
        description = response.css('#lenta-card__text-edition-escaped::text').get()
        if description:
            description = description.strip()
            description = re.sub(r'\s+', ' ', description)
            yield {
                'description': description.strip()
            }
        else:
            yield {
                'description': '-'
            }
