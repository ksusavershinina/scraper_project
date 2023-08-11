from spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BookSpider)
    process.start()
