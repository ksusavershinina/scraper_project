# from spiders.js_test_spider import BookSpider
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

from spiders.book_spider import BookSpider
from spiders.description_spider import DescriptionSpider
from scrapy.utils.project import get_project_settings

from scrapy.crawler import CrawlerProcess, CrawlerRunner
import logging
import sqlite3

con = sqlite3.connect('slow_books_database.db')
cur = con.cursor()
cur.execute("SELECT ISBN FROM book_description WHERE ISBN IS NOT NULL AND Annotation IS NULL ORDER BY random() LIMIT 10")
isbn_lst = cur.fetchall()
con.close()


def start_livelib_spider(ROBOTSTXT_OBEY=False, DOWNLOAD_DELAY=0.01, LOG_LEVEL='DEBUG'):
    logging.basicConfig(format='%(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    settings = get_project_settings()
    extra_settings = {
        'ROBOTSTXT_OBEY': ROBOTSTXT_OBEY,
        'DOWNLOAD_DELAY': str(DOWNLOAD_DELAY),
        'LOG_LEVEL': LOG_LEVEL,
    }
    merged_settings = settings.copy()
    merged_settings.update(extra_settings)

    configure_logging(merged_settings)
    runner = CrawlerRunner(merged_settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(BookSpider, isbn_arr=isbn_lst)

        con = sqlite3.connect('slow_books_database.db')
        cur = con.cursor()
        cur.execute("SELECT livelib_id FROM parsed_books")
        id_lst = cur.fetchall()
        con.close()

        yield runner.crawl(DescriptionSpider, id_arr=id_lst)
        reactor.stop()

    crawl()
    reactor.run()


start_livelib_spider()
