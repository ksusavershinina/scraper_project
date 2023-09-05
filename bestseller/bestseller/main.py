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

isbn_arr = ['978-5-907584-31-0', '978-5-907015-29-6', '978-5-907447-67-7', '978-5-906892-53-9', '978-5-907173-30-9',
            '978-5-907015-17-3', '978-5-907015-71-5', '978-5-907015-27-2', '978-5-906892-84-3', '978-5-906892-86-7',
            '978-5-907173-02-6', '978-5-906892-22-5', '978-5-907015-84-5', '978-5-907447-79-0', '978-5-907277-65-6',
            '978-5-907173-94-1', '978-5-907015-79-1', '978-5-907277-73-1', '978-5-907646-40-7', '978-5-907015-33-3',
            '978-5-907173-53-8', '978-5-907173-03-3', '978-5-907277-94-6', '978-5-907277-21-2', '978-5-907015-04-3',
            '978-5-907015-56-2', '978-5-907015-74-6', '978-5-907015-76-0', '978-5-906892-24-9', '978-5-907277-96-0',
            '978-5-907015-75-3', '978-5-906892-52-2', '978-5-906892-87-4', '978-5-907277-92-2', '978-5-907015-68-5',
            '978-5-907277-19-9', '978-5-907584-61-7', '978-5-906892-49-2', '978-5-907015-63-0', '978-5-906892-57-7',
            '978-5-907447-25-7', '978-5-906892-60-7', '978-5-907173-11-8', '978-5-906892-74-4', '978-5-907584-08-2',
            '978-5-907646-13-1', '978-5-906892-42-3', '978-5-907277-07-6', '978-5-907173-09-5', '978-5-907447-82-0',
            '978-5-907646-31-5', '978-5-907015-54-8', '978-5-907584-65-5', '978-5-907584-64-8', '978-5-907015-59-3',
            '978-5-906892-70-6', '978-5-906892-82-9', '978-5-906892-77-5', '978-5-907277-58-8', '978-5-907447-07-3',
            '978-5-907447-49-3', '978-5-907015-82-1', '978-5-907015-81-4', '978-5-907277-08-3', '978-5-907173-64-4', ]

con = sqlite3.connect('books2.db')
cur = con.cursor()
cur.execute("DROP TABLE isbn_test")
cur.execute("""CREATE TABLE IF NOT EXISTS isbn_test(isbn TEXT, description TEXT, book_cover TEXT, book_genres TEXT)""")
for isbn in isbn_arr:
    cur.execute("""INSERT INTO isbn_test VALUES (?, ?, ?, ?)""", (isbn, None, None, None))
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
