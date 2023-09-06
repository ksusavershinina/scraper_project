# from spiders.book_spider import BookSpider
from spiders.js_test_spider import BookSpider
from scrapy.crawler import CrawlerProcess
import logging
import sqlite3

# import pandas as pd
# load data file
# df = pd.read_csv('mk_price_21-07-2023.csv')
#
# # data clean up
# df.columns = df.columns.str.strip()
#
# # creating db
# connection = sqlite3.connect('demo.db')
# df.to_sql('books_table', connection, if_exists="replace")
# cursor = connection.cursor()
# query = "SELECT ISBN FROM books_table WHERE ISBN != '-' AND ISBN IS NOT NULL"
# cursor.execute(query)
# isbn_array = [row[0] for row in cursor.fetchall()]
#
# # close connection
# connection.close()

# get book genres
# query = "SELECT book_genres FROM isbn_test"
# cursor.execute(query)
# genres_from_db = [json.loads(row[0]) if row[0] is not None else [] for row in cur.fetchall()]
#
# for genre_list in genres_from_db:
#     print(genre_list)

"""clean isbn_array and store it like this:"""

isbn_arr = ['978-601-338-560-0', '978-601-338-832-8', '978-601-338-617-1', '978-601-338-618-8', '978-601-338-831-1',
     '978-601-302-395-3', '978-601-302-287-1', '978-601-338-768-0', '978-601-302-657-2', '978-601-271-326-8',
     '978-601-271-338-1', '978-601-302-968-9', '978-601-302-945-0', '978-601-338-073-5', '978-601-338-168-8',
     '978-601-302-534-6', '978-601-338-622-5', '978-601-338-625-6', '978-601-302-748-7', '978-601-338-202-9',
     '978-601-302-148-5', '978-601-302-895-8', '978-601-302-952-8', '978-601-338-181-7', '978-601-302-379-3',
     '978-601-338-741-3', '978-601-338-340-8', '978-601-338-833-5', '978-601-338-599-0', '978-601-292-834-1',
     '978-601-338-532-7', '978-601-338-528-0', '978-601-338-324-8', '978-601-338-187-9', '978-601-271-273-5',
     '978-601-338-458-0', '978-601-302-105-8', '978-601-302-626-8', '978-601-302-909-2', '978-601-271-234-6',
     '978-601-302-602-2', '978-601-302-629-9', '978-601-302-642-8', '978-601-338-182-4', '978-601-338-045-2',
     '978-601-338-939-4', '978-601-338-940-0', '978-601-338-941-7', '978-601-338-018-6', '978-601-338-212-8',
     '978-601-338-062-9', '978-601-271-257-5', '978-601-338-663-8', '978-601-271-368-8', '978-601-302-802-6',
     '978-601-338-316-3', '978-601-302-423-3', '978-601-338-218-0', '978-601-338-076-6', '978-601-338-077-3',
     '978-601-338-134-3', '978-601-338-183-1', '978-601-338-781-9', '978-601-338-701-7', '978-601-338-978-3',
     '978-601-271-300-8', '978-601-338-778-9', '978-601-302-498-1', '978-601-302-292-5', '978-601-302-565-0',
     '979-080-385-476-4', '978-601-338-104-6', '978-601-271-297-1', '978-601-292-973-7', '978-601-338-377-4',
     '978-601-338-401-6', '978-601-302-576-6', '978-601-338-398-9', '978-601-338-649-2', '978-601-338-534-1',
     '978-601-756-883-2', '978-601-271-296-4', '978-601-338-383-5', '978-601-338-327-9', '978-601-338-360-6',
     '978-601-338-341-5', '978-601-338-325-5', '978-601-338-361-3', '978-601-338-362-0', '978-601-338-326-2',
     '978-601-338-339-2', '978-601-338-359-0', '978-601-338-323-1', '978-601-271-306-0', '978-601-338-148-0',
     '978-601-302-724-1', '978-601-302-121-8', '978-601-302-490-5', '978-601-271-370-1', '978-601-271-399-2',]

con = sqlite3.connect('books2.db')
cur = con.cursor()
cur.execute("DROP TABLE isbn_test")
cur.execute(
    """CREATE TABLE IF NOT EXISTS isbn_test(isbn TEXT, description TEXT, book_cover TEXT, book_genres TEXT, rate REAL, read INTEGER, plan_to_read INTEGER)""")
for isbn in isbn_arr:
    cur.execute("""INSERT INTO isbn_test VALUES (?, ?, ?, ?, ?, ?, ?)""", (isbn, None, None, None, None, None, None))
    con.commit()

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
    process.crawl(BookSpider, isbn_arr=isbn_arr)
    process.start()


start_livelib_spider()
