# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class BestsellerPipeline:
#     def process_item(self, item, spider):
#         return item

import re

class DescriptionPipeline:
    def process_item(self, item, spider):
        if 'description' in item:
            description = item['description']
            item['description'] = re.sub(r'\s+', ' ', description)
            item['description'] = description.strip()
        return item

class GenresPipeline:
    def process_item(self, item, spider):
        if 'book_genres' in item:
            book_genres = item['book_genres']
            cleaned_genres = [
                re.search(r'[А-Я][а-яА-ЯёЁ\s]*', genre).group() if re.search(r'[А-Я][а-яА-ЯёЁ\s]*', genre) else None
                for genre in book_genres
            ]
            item['book_genres'] = cleaned_genres
        return item
