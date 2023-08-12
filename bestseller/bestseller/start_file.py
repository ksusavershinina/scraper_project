from spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess
import logging


if __name__ == '__main__':
    logging.basicConfig(
        filename='logs.txt',
        level=logging.DEBUG,  # Set the desired log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create a logger object for Scrapy
    scrapy_logger = logging.getLogger('scrapy')
    scrapy_logger.setLevel(logging.DEBUG)  # Set the desired log level for Scrapy

    process = CrawlerProcess()
    process.crawl(BookSpider)
    process.start()