# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import re
import sqlite3


class ItemPipeline:
    def process_item(self, item, spider):
        if item['description'] != None:
            description = item['description']
            item['description'] = re.sub(r'\s+', ' ', description)
            item['description'] = description.strip()

        if item['book_genres'] != None:
            book_genres = item['book_genres']
            cleaned_genres = [
                re.search(r'[А-Я][а-яА-ЯёЁ\s]*', genre).group() if re.search(r'[А-Я][а-яА-ЯёЁ\s]*', genre) else None
                for genre in book_genres
            ]
            new_cleaned_genres = ', '.join(cleaned_genres)
            item['book_genres'] = new_cleaned_genres
        return item


class DatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect('books2.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS isbn_test(isbn TEXT PRIMARY KEY, description TEXT, book_cover TEXT, book_genres TEXT)""")

    def process_item(self, item, spider):
        # self.cur.execute("""INSERT INTO books_test VALUES (?, ?, ?, ?)""",(item['isbn'], item['description'], item['book_cover'], item['book_genres']))
        self.cur.execute(f"""UPDATE isbn_test SET description = '{item['description']}', book_cover = '{item['book_cover']}', book_genres = '{item['book_genres']}' WHERE isbn = '{item['isbn']}'""")
        self.con.commit()
        return item
