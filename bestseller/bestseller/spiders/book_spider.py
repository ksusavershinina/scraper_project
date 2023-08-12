import scrapy
import re
import logging
from scrapy.utils.log import configure_logging


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
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.188',
    }

    custom_cookies = {'pushsetnew': '1', '__ddg1_': 'XR1IzhP6AW7V7Gfjjata',
                      'LiveLibId': '4cfcc567dda02071eee09dca94ff232d', '__ll_tum': '579836457', '__llutmz': '-600',
                      '__llutmf': '0', 'll_asid': '1371254432', 'SL_GWPT_Show_Hide_tmp': '1', 'SL_wptGlobTipTmp': '1',
                      '__ll_fv': '1690682303', '__ll_dvs': '5', 'closed_vkid_onetap': '1', '__ll_ab_mp': '1',
                      '__utnt': 'g0_y0_a15721_u0_c0', '__ll_unreg_session': '4cfcc567dda02071eee09dca94ff232d',
                      '__ll_unreg_sessions_count': '1', '__ll_cp': '1', 'pushsub': '1', '__ll_dv': '1691759015',
                      '__gr': 'g102c39_g1c12_g1243c1_g1240c2_g533c4_g527c6_g433c4_g1217c4_g1360c2_g1226c2_g430c2_g1143c3_g1140c4_g137c3_g144c2_g146c1_g426c1_g143c2_g394c1_g387c1_g510c2_g520c1_g601c3_g537c36_g549c1_g547c1_g670c1_g641c1_g76c1_g535c1_g518c1_g611c32_g107c1_g150c1_g1319c1_g1318c1_g148c1_g141c1_g149c1_g142c1_g1142c1_g1321c1_g1163c1_g1150c1_',
                      'iwatchyou': '3d1fa16abc8455f326c604587166bca3'}

    def start_requests(self):
        logging.debug('Spider is starting...')
        # получать данные из бд
        isbn_arr = ['5-87444-255-3', '5-87444-178-6', '5-87444-338-3', '978-5-87444-415-0', '5-93332-213-X',
                    '978-966-8324-20-X', '965-293-058-X', '5-902291-02-X', '978-5-6044767-4-1', '978-5-6044767-7-2',
                    '978-5-6044767-2-7', '978-5-6044767-3-4', '978-5-6044767-5-8']
        for isbn in isbn_arr:
            logging.debug('Starting requests...')
            link = f"https://www.livelib.ru/find/{isbn}"
            yield scrapy.Request(url=link, callback=self.parse_page, headers=self.custom_headers, method="GET",
                                 cookies=self.custom_cookies)

    def parse_page(self, response):
        logging.debug('Parsing page...')
        book_link = response.css('.find-book-block a::attr(href)').get()
        # if not(book_link):
        #     book_link = response.css('.brow-title a::attr(href)').get()
        if not (book_link):
            yield {
                'description': '-',
                'book_cover': '-',
            }
        else:
            # надо прописать условия на 0 и больше 1 ссылки
            yield response.follow(url=book_link, callback=self.parse_book)

    def parse_book(self, response):
        logging.debug('Parsing book...', )
        description = response.css('#lenta-card__text-edition-escaped::text').get()
        book_cover = response.css('img.bc-menu__image::attr(src)').get()
        if description:
            description = description.strip()
            description = re.sub(r'\s+', ' ', description)
            yield {
                'description': description.strip(),
                'book_cover': book_cover,
            }
        else:
            yield {
                'description': '-',
                'book_cover': '-',
            }
