# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import re
import sqlite3
import json


class ItemPipeline:
    def process_item(self, item, spider):
        if item['description'] is not None:
            description = item['description']
            item['description'] = re.sub(r'\s+', ' ', description)
            item['description'] = description.strip()
            item['description'] = re.sub(r'<br />|\r|\n', '', item['description'])
            item['description'] = re.sub(r'&quot;', '"', item['description'])
            item['description'] = re.sub('&amp;|&#039;', '\'', item['description'])

        if item['book_genres'] is not None:
            book_genres = item['book_genres']
            cleaned_genres = [
                re.search(r'[А-Я][а-яА-ЯёЁ\s]*', genre).group() if re.search(r'[А-Я][а-яА-ЯёЁ\s]*', genre) else None
                for genre in book_genres
            ]
            item['book_genres'] = cleaned_genres

        if item['read'] is not None:
            match = re.search(r'<b>(\d+)</b>', item['read'])
            if match:
                item['read'] = match.group(1)

        if item['plan_to_read'] is not None:
            match = re.search(r'<b>(\d+)</b>', item['plan_to_read'])
            if match:
                item['plan_to_read'] = match.group(1)

        return item


class DatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect('slow_books_database.db')
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        self.cur.execute("""UPDATE isbn_test SET
            description = ?,
            book_cover = ?,
            book_genres = ?,
            rate = ?,
            read = ?,
            plan_to_read = ?
            WHERE isbn = ?""",
                         (
                             item['description'],
                             item['book_cover'],
                             json.dumps(item['book_genres'], ensure_ascii=False),
                             item['rate'],
                             item['read'],
                             item['plan_to_read'],
                             item['isbn']
                         ))

        self.con.commit()
        return item
