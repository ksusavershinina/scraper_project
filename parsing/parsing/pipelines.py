# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import sqlite3
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FileException
from scrapy.utils.request import referer_str

logger = logging.getLogger(__name__)


class ItemPipeline:
    def process_item(self, item, spider):
        if item['isbn'] is not None:
            item['isbn'] = re.sub(r'\D', '', item['isbn'])
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
        self.con = sqlite3.connect('database/slow_books_database.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS parsed_books (ID INTEGER PRIMARY KEY, ISBN TEXT, book24_score REAL, 
            book24_feedback INTEGER, number_of_buyers INTEGER, description TEXT, book_cover TEXT)""")

    def process_item(self, item, spider):
        self.cur.execute(
            """INSERT INTO parsed_books (ID, ISBN, book24_score, book24_feedback, number_of_buyers, description, 
            book_cover) VALUES (?, ?, ?, ?, ?, ?, ?)""", (item['id'], item['isbn'], item['book24_score'],
                                                          item['book24_feedback'], item['number_of_buyers'],
                                                          item['description'], item['images']))
        self.con.commit()
        return item


class CustomImagePipeline(ImagesPipeline):
    def media_downloaded(self, response, request, info, *, item=None):
        referer = referer_str(request)

        if response.status != 200:
            logger.warning(
                "File (code: %(status)s): Error downloading file from "
                "%(request)s referred in <%(referer)s>",
                {"status": response.status, "request": request, "referer": referer},
                extra={"spider": info.spider},
            )
            raise FileException("download-error")

        if not response.body:
            logger.warning(
                "File (empty-content): Empty file from %(request)s referred "
                "in <%(referer)s>: no-content",
                {"request": request, "referer": referer},
                extra={"spider": info.spider},
            )
            raise FileException("empty-content")

        status = "cached" if "cached" in response.flags else "downloaded"
        logger.debug(
            "File (%(status)s): Downloaded file from %(request)s referred in "
            "<%(referer)s>",
            {"status": status, "request": request, "referer": referer},
            extra={"spider": info.spider},
        )
        self.inc_stats(info.spider, status)

        try:
            path = self.file_path(request, response=response, info=info, item=item)
            checksum = self.file_downloaded(response, request, info, item=item)
        except FileException as exc:
            logger.warning(
                "File (error): Error processing file from %(request)s "
                "referred in <%(referer)s>: %(errormsg)s",
                {"request": request, "referer": referer, "errormsg": str(exc)},
                extra={"spider": info.spider},
                exc_info=True,
            )
            raise
        except Exception as exc:
            logger.error(
                "File (unknown-error): Error processing file from %(request)s "
                "referred in <%(referer)s>",
                {"request": request, "referer": referer},
                exc_info=True,
                extra={"spider": info.spider},
            )
            raise FileException(str(exc))

        return path
