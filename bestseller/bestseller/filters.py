import logging


class DumpingStatsFilter(logging.Filter):
    def filter(self, record):
        return "Dumping Scrapy stats" in record.getMessage()
