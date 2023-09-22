from parsing.parsing.spiders.book24 import Book24Spider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
import sqlite3

configure_logging()
parserConfig = CrawlerRunner(settings={'ROBOTSTXT_OBEY': False,
                                       'DOWNLOAD_DELAY': 0,
                                       'LOG_FILE': 'logs.txt',
                                       'LOG_FILE_APPEND': False,
                                       'LOG_SHORT_NAMES': True,
                                       'IMAGES_STORE': 'images',
                                       'ITEM_PIPELINES': {
                                           'scrapy.pipelines.images.ImagesPipeline': 1,
                                           'scraper_project.parsing.parsing.pipelines.ItemPipeline': 200,
                                            'scraper_project.parsing.parsing.pipelines.DatabasePipeline': 300
                                       },
                                       'FEEDS': {
                                           '%(name)s/%(name)s_%(time)s.json': {
                                               'format': 'json',
                                               'encoding': 'utf8',
                                               'indent': 4,
                                               'item_export_kwargs': {
                                                   'export_empty_fields': True,
                                               },
                                           }
                                       }})

con = sqlite3.connect('database/slow_books_database.db')
cur = con.cursor()
cur.execute("SELECT ID, ISBN FROM book_description")
id_isbn_lst = cur.fetchall()
con.close()

@defer.inlineCallbacks
def book24_parse():
    yield parserConfig.crawl(Book24Spider, id_isbn_lst)


book24_parse()
reactor.run()
