from spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
    'ROBOTSTXT_OBEY': 'False',
    'LOG_LEVEL': 'DEBUG',
    'LOG_FILE': 'logs.txt',
    'DOWNLOAD_DELAY': '0',
    'LOG_FILE_APPEND': True,
    'LOG_SHORT_NAMES': True,  # If True, the logs will just contain the root path.
    'date-fmt': '%Y-%m-%d %H:%M:%S',
    'FEEDS': {
        f'%(name)s/%(name)s_%(time)s.json': {
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
