import re
import scrapy
import logging
from scraper_project.bestseller.bestseller.items import BestsellerItem


class BookSpider(scrapy.Spider):
    name = 'livelib_test'
    allowed_domains = ['www.livelib.ru']

    headers_for_book = {
        'Host': 'www.livelib.ru',
        'Sec-Ch-Ua': '',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.5845.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    cookies_for_book = {'__llutmz': '-600', '__llutmf': '0', '__ll_fv': '1677902920', '_ym_uid': '1677902921278570168',
                        '_ym_d': '1677902921', 'tmr_lvid': 'c1da78ba680c9a04c8473880e908bcc6',
                        'tmr_lvidTS': '1677902922063',
                        '__ll_ab_mp': '1', '__popupmail_showed_uc': '2', '__ddg1_': 'qA2HNADSt7nh3TNDCbBr',
                        'LiveLibId': 'fbae66966e333521db96ad3027358196', '__ll_tum': '4182824734', '__ll_dvs': '4',
                        'll_asid': '1402019738', '_ym_isad': '2', '_gid': 'GA1.2.981752588.1693499713',
                        'promoLLid': '1mcjf4mtul1cqab76bq0ajkse0', 'showed_vkid_onetap': '1', '__ll_unreg_r': '60',
                        '__utnt': 'g0_y0_a15721_u0_c0', '__ll_unreg_session': 'fbae66966e333521db96ad3027358196',
                        '__ll_unreg_sessions_count': '11', '__ll_popup_count_pviews': 'regc1_mailc1_',
                        '__ll_popup_showed': 'challenge23unreg_', '__ll_popup_last_show': '1693499892',
                        '__ll_popup_count_shows': 'regc1_mailc1_challenge23unregc1_', '__popupmail_showed': '1000',
                        '__llaggbookbookstyle': 'middletiles', '__gr': 'g433c2_g1217c2_g706c1_g692c1_g1c6_',
                        '_ga_90RPM8SDHL': 'GS1.1.1693499711.1.1.1693502744.58.0.0', '__ll_cp': '17',
                        '_ga': 'GA1.2.1851051766.1677902921',
                        'tmr_detect': '0%7C1693502746687', '__ll_dv': '1693502805'}

    headers_for_desc = {
        'Host': 'www.livelib.ru',
        'Sec-Ch-Ua': 'Accept: */*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36',
        'Sec-Ch-Ua-Platform': "",
        'Origin': 'https://www.livelib.ru',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    cookies_for_desc = {'__ddg1_': 'XMke2VWMxlHK7ym9cJ5y', '__ll_tum': '2811089264', '__ll_ab_mp': '1',
                        'tmr_lvid': 'b64effb70d7d4eee3b73f6f8e1f1c5dd', 'tmr_lvidTS': '1693104841239',
                        '_ym_uid': '1693104842929034073', '_ym_d': '1693104842', '__ll_fv': '1693104847',
                        '__llutmz': '-600', '__llutmf': '0', '__ll_popup_count_shows': 'challenge23unregc1_',
                        '_ym_isad': '1', '_gid': 'GA1.2.218806420.1693659428',
                        'LiveLibId': '6bd6aa1f8a8adc77e2e8efc115e72077', '__ll_dvs': '5',
                        'll_asid': '1403330600', '__utnt': 'g0_y0_a15721_u0_c0',
                        '__ll_unreg_session': '6bd6aa1f8a8adc77e2e8efc115e72077',
                        '__ll_unreg_sessions_count': '4', 'promoLLid': 'uo03dh2nptucd8u4hacm514u70',
                        'showed_vkid_onetap': '1', '__ll_unreg_r': '60',
                        '__gr': 'g137c2_g1143c1_g1140c1_g533c1_g527c1_', '__gads': 'ID', '__gpi': 'UID',
                        '__ll_cp': '10', '_ga': 'GA1.2.466385732.1693104841',
                        'tmr_detect': '0%7C1693711595846',
                        '_ga_90RPM8SDHL': 'GS1.1.1693711592.3.1.1693711596.56.0.0',
                        '__ll_popup_count_pviews': 'mailc1_', '__ll_dv': '1693711657'}

    def __init__(self, isbn_arr):
        self.isbn_arr = isbn_arr

    def get_object_id(self, raw):
        id_pattern = r'/book/(\d+)-'

        match = re.search(id_pattern, raw)

        if match:
            id = match.group(1)
            return id
        else:
            pass

    def book_item(self, isbn, description, book_cover, book_genres, rate, read, plan_to_read):
        return BestsellerItem(
            isbn=isbn,
            description=description,
            book_cover=book_cover,
            book_genres=book_genres,
            rate=rate,
            read=read,
            plan_to_read=plan_to_read,
        )

    def start_requests(self):
        logging.debug('Spider is starting...')
        isbn_arr = self.isbn_arr
        for isbn in isbn_arr:
            link = f"https://www.livelib.ru/book/{isbn}"
            yield scrapy.Request(url=link, callback=self.parse_book, headers=self.headers_for_book, method="POST",
                                 cookies=self.cookies_for_book, meta={'isbn': isbn})

    def parse_book(self, response):
        logging.debug('Parsing book...', )

        book_cover = response.css('img.bc-menu__image::attr(src)').get()
        book_genres = response.css("p:contains('Жанры') a::text").getall()
        expand = response.css('a.read-more__link::text').get()
        if response.css('a.bc-rating-medium span::text').get() is not None:
            rate = response.css('a.bc-rating-medium span::text').get().strip()
        else:
            rate = None

        try:
            read = response.css("a.popup-load-data.bc-stat__link:contains('прочит')").get()
        except:
            read = None

        try:
            plan_to_read = response.css("a.popup-load-data.bc-stat__link:contains('планир')").get()
        except:
            plan_to_read = None

        if expand:
            object_id = self.get_object_id(response.url)
            params = f"object_alias=edition&object_id={object_id}&is_new_design=ll2019"
            yield scrapy.Request(url='https://www.livelib.ru/feed/getfullobjecttext',
                                 headers=self.headers_for_desc,
                                 cookies=self.cookies_for_desc,
                                 method='POST',
                                 body=params,
                                 callback=self.parse_description,
                                 meta={'isbn': response.meta.get('isbn'), 'book_cover': book_cover,
                                       'book_genres': book_genres, 'rate': rate, 'read': read, 'plan_to_read': plan_to_read})
        else:
            description = response.css('#lenta-card__text-edition-escaped::text').get()
            yield self.book_item(
                isbn=response.meta.get('isbn'),
                description=description,
                book_cover=book_cover,
                book_genres=book_genres,
                rate=rate,
                read=read,
                plan_to_read=plan_to_read,
            )
            logging.debug('Complete parsing book')

    def parse_description(self, response):
        logging.debug('Parsing full description...', )
        data = response.json()
        content = data.get('content')

        yield self.book_item(
            isbn=response.meta.get('isbn'),
            description=content,
            book_cover=response.meta.get('book_cover'),
            book_genres=response.meta.get('book_genres'),
            rate=response.meta.get('rate'),
            read=response.meta.get('read'),
            plan_to_read=response.meta.get('plan_to_read'),
        )

        logging.debug('Complete parsing book')

