from spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess
import logging
from filters import DumpingStatsFilter  # Import the custom filter


def start_livelib_spider(ROBOTSTXT_OBEY=False, DOWNLOAD_DELAY=0, LOG_LEVEL='INFO', filter_stats=False):

    logging.basicConfig(format='%(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the default log level to INFO
    if filter_stats:
        logger.addFilter(DumpingStatsFilter())

    process = CrawlerProcess({
        'ROBOTSTXT_OBEY': ROBOTSTXT_OBEY,
        'DOWNLOAD_DELAY': str(DOWNLOAD_DELAY),
        'LOG_LEVEL': LOG_LEVEL,
        'LOG_FILE': 'logs.txt',
        'LOG_FILE_APPEND': True,
        'LOG_SHORT_NAMES': True,
        'FEEDS': {
            '%(name)s/%(name)s_%(time)s.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'ensure_ascii': False,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            }
        }
    })
    process.crawl(BookSpider)
    process.start()


start_livelib_spider()
