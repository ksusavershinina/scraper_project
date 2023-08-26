from parsing.parsing.spiders.book24 import Book24Spider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

configure_logging()
parserConfig = CrawlerRunner(settings={'ROBOTSTXT_OBEY': False,
                                       'DOWNLOAD_DELAY': 0,
                                       # 'LOG_FILE': 'logs.txt',
                                       # 'LOG_FILE_APPEND': True,
                                       # 'LOG_SHORT_NAMES': True,
                                       # 'FEEDS':
                                       #     {'%(name)s/%(name)s_%(time)s.json': {
                                       #         'format': 'json',
                                       #         'encoding': 'utf8',
                                       #         'store_empty': False,
                                       #         'fields': None,
                                       #         'indent': 4,
                                       #         'ensure_ascii': False,
                                       #         'item_export_kwargs': {
                                       #             'export_empty_fields': True,
                                       #         },
                                       #     }}
                                       })


@defer.inlineCallbacks
def book24_parse():
    isbn_lst = ['9785950034107', '9785600017153']

    yield parserConfig.crawl(Book24Spider, isbn_lst)


book24_parse()
reactor.run()
