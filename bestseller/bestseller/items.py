# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BestsellerItem(scrapy.Item):
    isbn = scrapy.Field()
    description = scrapy.Field()
    book_cover = scrapy.Field()
    book_genres = scrapy.Field()
    rate = scrapy.Field()
    read = scrapy.Field()
    plan_to_read = scrapy.Field()



