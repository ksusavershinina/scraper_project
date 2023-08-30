import scrapy
import logging
from scraper_project.bestseller.bestseller.items import BestsellerItem


class BookSpider(scrapy.Spider):
    name = 'livelib_test'
    allowed_domains = ['livelib.ru/find', 'www.livelib.ru', 'livelib.ru/book']

    custom_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Dnt': '1',
        'Pragma': 'no-cache',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.203',
    }

    custom_cookies = {'__ddg1_': '9g9qjI29przbCEfqoItH', 'LiveLibId': '037d3556fd79b1ada16317a62166152d',
                      '__ll_tum': '1811981767', '__ll_ab_mp': '1', '__utnt': 'g0_y0_a15721_u0_c0',
                      '__ll_unreg_session': '037d3556fd79b1ada16317a62166152d', '__ll_unreg_sessions_count': '1',
                      '__ll_fv': '1693096357', '__ll_dvs': '5', 'll_asid': '1397335144',
                      'tmr_lvid': '7514c47c5bb16a64e27e3f85b4bf7594', 'tmr_lvidTS': '1693096358038',
                      '_ym_uid': '1693096358208679050', '_ym_d': '1693096358', '_ym_isad': '2',
                      'promoLLid': 'ha3nk1lplc9i5o5vstqpthtv80', '__llutmz': '-600', '__llutmf': '0',
                      '_gid': 'GA1.2.958445525.1693096359', '__ll_popup_count_pviews': 'mailc1_',
                      'showed_vkid_onetap': '1', 'closed_vkid_onetap': '1', '__popupmail_showed': '1000',
                      '__popupmail_showed_uc': '1', '__popupmail_showed_t': '1000',
                      '__ll_popup_showed': 'challenge23unreg_mail_', '__ll_popup_last_show': '1693096885',
                      '__ll_popup_count_shows': 'challenge23unregc1_mailc1_', '__r': 'pc3804c1_',
                      'iwatchyou': 'c30be2019cb6bc105691d58cb7cb7906', 'pushsetnew': '1', 'pushsub': '1',
                      '__ll_dv': '1693097021', '__ll_cp': '7', '_ga': 'GA1.2.754249114.1693096358',
                      '_gat_gtag_UA_929334_1': '1', 'tmr_detect': '0%7C1693097024645',
                      '_ga_90RPM8SDHL': 'GS1.1.1693096358.1.1.1693097024.58.0.0'}

    def __int__(self, isbn_arr):
        # в таком случае в методе ниже нужно будет чуть чуть поменять логику
        self.isbn_arr = isbn_arr

    def add_headers(self, row, dictionary):
        refactor_row = row.split(': ')
        dictionary[refactor_row[0]] = refactor_row[1]
        return dictionary

    def start_requests(self):
        logging.debug('Spider is starting...')
        logging.debug('Starting requests...')
        isbn_arr = self.isbn_arr
        for isbn in isbn_arr:
            link = f"https://www.livelib.ru/find/{isbn}"
            yield scrapy.Request(url=link, callback=self.parse_page, headers=self.custom_headers, method="GET",
                                 cookies=self.custom_cookies, meta={'isbn': isbn})

    def parse_page(self, response):
        logging.debug('Parsing page...')
        book_link = response.css('.find-book-block a::attr(href)').get()
        if not (book_link):
            book_item = BestsellerItem(
                isbn=response.meta.get('isbn'),
                description=None,
                book_cover=None,
                book_genres=None,
            )
            yield book_item
        else:
            # надо прописать условия на 0 и больше 1 ссылки
            yield response.follow(url=book_link, callback=self.parse_book, meta={'isbn': response.meta.get('isbn')},
                                  method='POST',
                                  # headers=self.custom_headers)
            headers=self.add_headers('X-Requested-With: XMLHttpRequest', self.custom_headers))

    def parse_book(self, response):

        # работа с json

        # logging.debug('Parsing book...', )
        # description = response.css('#lenta-card__text-edition-escaped::text').get()
        # book_cover = response.css('img.bc-menu__image::attr(src)').get()
        # book_genres = response.css("p:contains('Жанры') a::text").getall()
        #
        # book_item = BestsellerItem(
        #     isbn=response.meta.get('isbn'),
        #     description=description,
        #     book_cover=book_cover,
        #     book_genres=book_genres,
        # )
        # yield book_item
        # logging.debug('Complete parsing book')
        print(response.text)
