import scrapy
import logging
from scraper_project.bestseller.bestseller.items import BestsellerItem


class BookSpider(scrapy.Spider):
    name = 'livelib_test'
    allowed_domains = ['livelib.ru/find', 'www.livelib.ru', 'livelib.ru/book']
    start_urls = ['https://www.livelib.ru/find']

    custom_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Dnt': '1',
        'Pragma': 'no-cache',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.188',
    }

    custom_cookies = {'__ddg1_': 'XR1IzhP6AW7V7Gfjjata', 'LiveLibId': '4cfcc567dda02071eee09dca94ff232d',
                      '__ll_tum': '579836457', '__llutmz': '-600', '__llutmf': '0', 'll_asid': '1371254432',
                      'SL_GWPT_Show_Hide_tmp': '1', 'SL_wptGlobTipTmp': '1', '__ll_fv': '1690682303', '__ll_dvs': '5',
                      'closed_vkid_onetap': '1', '__ll_ab_mp': '1', '__utnt': 'g0_y0_a15721_u0_c0',
                      '__ll_unreg_session': '4cfcc567dda02071eee09dca94ff232d', '__ll_unreg_sessions_count': '1',
                      '__ll_cp': '1', 'pushsub': '1', '__ll_dv': '1692595522',
                      '__gr': 'g102c40_g1c14_g1243c1_g1240c5_g533c4_g527c6_g433c7_g1217c7_g1360c2_g1226c2_g430c2_g1143c3_g1140c4_g137c3_g144c2_g146c1_g426c1_g143c2_g394c1_g387c1_g510c3_g520c2_g601c4_g537c43_g549c1_g547c1_g670c1_g641c1_g76c2_g535c2_g518c1_g611c37_g107c2_g150c1_g1319c1_g1318c1_g148c1_g141c1_g149c1_g142c1_g1142c1_g1321c1_g1163c2_g1150c2_g1247c3_g1276c3_'}

    # def __int__(self, isbn_arr):
    #  в таком случае в методе ниже нужно будет чуть чуть поменять логику
    #     self.isbn_arr = isbn_arr

    def start_requests(self):
        logging.debug('Spider is starting...')
        logging.debug('Starting requests...')
        # получать данные из бд
        isbn_arr = ['5-87444-255-3', '5-87444-178-6', '5-87444-338-3', '978-5-87444-415-0', '5-93332-213-X',
                    '978-966-8324-20-X', '965-293-058-X', '5-902291-02-X', '978-5-6044767-4-1', '978-5-6044767-7-2',
                    '978-5-6044767-2-7', '978-5-6044767-3-4', '978-5-6044767-5-8']
        for isbn in isbn_arr:
            link = f"https://www.livelib.ru/find/{isbn}"
            yield scrapy.Request(url=link, callback=self.parse_page, headers=self.custom_headers, method="GET",
                                 cookies=self.custom_cookies)

    def parse_page(self, response):
        logging.debug('Parsing page...')
        book_link = response.css('.find-book-block a::attr(href)').get()
        if not (book_link):
            book_item = BestsellerItem(
                description=None,
                book_cover=None,
                book_genres=None,
            )
            yield book_item
        else:
            # надо прописать условия на 0 и больше 1 ссылки
            yield response.follow(url=book_link, callback=self.parse_book)

    def parse_book(self, response):
        logging.debug('Parsing book...', )
        description = response.css('#lenta-card__text-edition-escaped::text').get()
        book_cover = response.css('img.bc-menu__image::attr(src)').get()
        book_genres = response.css("p:contains('Жанры') a::text").getall()

        book_item = BestsellerItem(
            description=description,
            book_cover=book_cover,
            book_genres=book_genres,
        )
        yield book_item
        logging.debug('Complete parsing book')
