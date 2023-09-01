# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import sqlite3


class ItemPipeline:
    def process_item(self, item, spider):
        if item['isbn'] is not None:
            item['isbn'] = re.sub(r'-', '', item['isbn'])

        if item['number_of_buyers'] is not None:
            item['number_of_buyers'] = re.sub(r'\D', '', item['number_of_buyers'])

        if item['book24_score'] is not None:
            item['book24_score'] = re.sub(r'\s', '', item['book24_score'])
            item['book24_score'] = re.sub(r',', '.', item['book24_score'])

        if item['book24_feedback'] is not None:
            item['book24_feedback'] = re.sub(r'[()\s]', '', item['book24_feedback'])

        if item['description'] is not None:
            description = item['description']
            item['description'] = ' '.join(description)
            item['description'] = re.sub(r'\r', '', item['description'])

        return item


class DatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect()
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS isbn_test(id INTEGER PRIMARY KEY, isbn TEXT, book24_score REAL, book24_feedback INTEGER, number_of_buyers INTEGER, description TEXT, book_cover TEXT, )""")

    def process_item(self, item, spider):
        self.cur.execute(
            f"""UPDATE isbn_test SET book24_score='{item['book24_score']}', book24_feedback='{item['book24_feedback']}', number_of_buyers='{item['number_of_buyers']}',description = '{item['description']}', book_cover = '{item['book_cover']}}' WHERE isbn = '{item['isbn']}'""")
        self.con.commit()
        return item
