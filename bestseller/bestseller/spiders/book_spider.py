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

    cookies_for_book = {'__ddg1_': 'XR1IzhP6AW7V7Gfjjata', 'LiveLibId': '4cfcc567dda02071eee09dca94ff232d', '__llutmz': '-600', '__llutmf': '0', 'll_asid': '1371254432', 'SL_GWPT_Show_Hide_tmp': '1', 'SL_wptGlobTipTmp': '1', '__ll_fv': '1690682303', '__ll_dvs': '5', 'closed_vkid_onetap': '1', '__ll_ab_mp': '1', '__utnt': 'g0_y0_a15721_u0_c0', '__ll_unreg_session': '4cfcc567dda02071eee09dca94ff232d', '__ll_unreg_sessions_count': '1', 'pushsub': '1', '__ll_tum': '826029989', '__ll_cp': '2', '__ddgid_': 'v2x57OEhW0hhj58a', '__ddg2_': 'hj9U1HhbyVRJjBmG', '__ll_dv': '1693971817', '__gr': 'g102c40_g1c14_g1243c1_g1240c5_g533c5_g527c7_g433c7_g1217c7_g1360c2_g1226c2_g430c3_g1143c6_g1140c12_g137c4_g144c2_g146c1_g426c1_g143c2_g394c3_g387c3_g510c6_g520c2_g601c6_g537c49_g549c1_g547c4_g670c1_g641c1_g76c2_g535c2_g518c1_g611c40_g107c2_g150c1_g1319c1_g1318c1_g148c1_g141c1_g149c2_g142c1_g1142c5_g1321c1_g1163c2_g1150c2_g1247c3_g1276c3_g511c1_g516c1_g140c1_g525c1_g600c1_g1147c1_g1098c2_g1095c2_g551c3_g1323c1_g416c1_g1128c1_', 'iwatchyou': '9dfaead2695764c012c07556a76f65c9'}

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

    cookies_for_desc = {'__ddg1_': 'XR1IzhP6AW7V7Gfjjata', 'LiveLibId': '4cfcc567dda02071eee09dca94ff232d', '__llutmz': '-600', '__llutmf': '0', 'll_asid': '1371254432', 'SL_GWPT_Show_Hide_tmp': '1', 'SL_wptGlobTipTmp': '1', '__ll_fv': '1690682303', '__ll_dvs': '5', 'closed_vkid_onetap': '1', '__ll_ab_mp': '1', '__utnt': 'g0_y0_a15721_u0_c0', '__ll_unreg_session': '4cfcc567dda02071eee09dca94ff232d', '__ll_unreg_sessions_count': '1', 'pushsub': '1', '__ll_tum': '826029989', '__ll_cp': '2', '__ddgid_': 'v2x57OEhW0hhj58a', '__ddg2_': 'hj9U1HhbyVRJjBmG', '__ll_dv': '1693971817', '__gr': 'g102c40_g1c14_g1243c1_g1240c5_g533c5_g527c7_g433c7_g1217c7_g1360c2_g1226c2_g430c3_g1143c6_g1140c12_g137c4_g144c2_g146c1_g426c1_g143c2_g394c3_g387c3_g510c6_g520c2_g601c6_g537c49_g549c1_g547c4_g670c1_g641c1_g76c2_g535c2_g518c1_g611c40_g107c2_g150c1_g1319c1_g1318c1_g148c1_g141c1_g149c2_g142c1_g1142c5_g1321c1_g1163c2_g1150c2_g1247c3_g1276c3_g511c1_g516c1_g140c1_g525c1_g600c1_g1147c1_g1098c2_g1095c2_g551c3_g1323c1_g416c1_g1128c1_', 'iwatchyou': '9dfaead2695764c012c07556a76f65c9'}

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

