from spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess

# метод, из которого вызывается работа парсера
# передавать отсюда в паук базу данных


process = CrawlerProcess({
    'ROBOTSTXT_OBEY': 'False',
    'LOG_LEVEL': 'ERROR',
    'LOG_FILE': 'logs.txt',
    'DOWNLOAD_DELAY': '0',
    'FEEDS': {
        'data.json': {
            'format': 'json',
            'encoding': 'utf8',
        }
    }
})
process.crawl(BookSpider)
process.start()
