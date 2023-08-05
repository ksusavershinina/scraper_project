import scrapy


class NewspiderSpider(scrapy.Spider):
    name = "newspider"
    allowed_domains = ["www.livelib.ru"]
    start_urls = ["https://www.livelib.ru/books/bestsellers"]

    def parse(self, response):
        products = response.css('div.book-item__inner ')

        for product in products:
            yield {
                'isbn' : product.css('table.book-item-edition tbody tr td::text')[1].get(),
                'description' : product.css('div.book-item__text div p::text').get()
            }

