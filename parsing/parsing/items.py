# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsingItem(scrapy.Item):
    # define the fields for your item here like:
    book24_score = scrapy.Field()
    number_of_buyers = scrapy.Field()
    description = scrapy.Field()
    book_cover = scrapy.Field()

