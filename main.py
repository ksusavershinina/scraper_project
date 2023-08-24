
from parsing.parsing.spiders.book24 import Book24Spider
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging



def book24_parse(ROBOTSTXT_OBEY=False, DOWNLOAD_DELAY=0, LOG_LEVEL='INFO'):
    # logging.basicConfig(format='%(levelname)s: %(message)s')
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)  # Set the default log level to INFO

    process = CrawlerProcess({
        'ROBOTSTXT_OBEY': ROBOTSTXT_OBEY,
        'DOWNLOAD_DELAY': str(DOWNLOAD_DELAY),
        'LOG_LEVEL': LOG_LEVEL,
        'LOG_FILE': 'logs.txt',
        'LOG_FILE_APPEND': True,
        'LOG_SHORT_NAMES': True,
        # 'DOWNLOADER_CLIENTCONTEXTFACTORY': 'scrapy.core.downloader.contextfactory.BrowserLikeContextFactory',
        # 'ITEM_PIPELINES': {
        #     'scraper_project.parsing.parsing.pipelines.DescriptionPipeline': 300,
        #     'scraper_project.parsing.parsing.pipelines.GenresPipeline': 400,
        # },
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
    process.crawl(Book24Spider)
    process.start()


book24_parse()