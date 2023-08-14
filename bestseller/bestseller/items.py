# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BestsellerItem(scrapy.Item):
    description = scrapy.Field()
    book_cover = scrapy.Field()
    book_genres = scrapy.Field()

