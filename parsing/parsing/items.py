# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsingItem(scrapy.Item):
    id = scrapy.Field()
    isbn = scrapy.Field()
    book24_score = scrapy.Field()
    book24_feedback = scrapy.Field()
    number_of_buyers = scrapy.Field()
    description = scrapy.Field()
    book_cover = scrapy.Field()

