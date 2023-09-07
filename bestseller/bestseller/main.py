from spiders.book_spider import BookSpider
# from spiders.js_test_spider import BookSpider
from scrapy.crawler import CrawlerProcess
import logging
import sqlite3

con = sqlite3.connect('slow_books_database.db')
cur = con.cursor()
cur.execute("SELECT ISBN FROM book_description WHERE Annotation IS NULL ORDER BY random() LIMIT 50")
isbn_lst = cur.fetchall()
con.close()


def start_livelib_spider(ROBOTSTXT_OBEY=False, DOWNLOAD_DELAY=0.01, LOG_LEVEL='DEBUG', filter_stats=False):
    logging.basicConfig(format='%(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    process = CrawlerProcess({
        'ROBOTSTXT_OBEY': ROBOTSTXT_OBEY,
        'DOWNLOAD_DELAY': str(DOWNLOAD_DELAY),
        'LOG_LEVEL': LOG_LEVEL,
        'LOG_FILE': 'logs.txt',
        'LOG_FILE_APPEND': True,
        'LOG_SHORT_NAMES': True,
        'ITEM_PIPELINES': {
            'scraper_project.bestseller.bestseller.pipelines.ItemPipeline': 300,
            'scraper_project.bestseller.bestseller.pipelines.DatabasePipeline': 400,
        },
        'FEEDS': {
            '%(name)s/%(name)s_%(time)s.json': {
                'format': 'json',
                'encoding': 'utf8',
                'fields': None,  # какие поля нужны для экпорта
                'indent': 4,
                'ensure_ascii': False,  # вроде как позволяет видеть ascii символы
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            }
        }
    })
    process.crawl(BookSpider, isbn_arr=isbn_lst)
    process.start()


start_livelib_spider()
