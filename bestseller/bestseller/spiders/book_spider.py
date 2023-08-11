import scrapy
import re

class BookSpider(scrapy.Spider):
    name = 'livelib_test'
    allowed_domains = ['livelib.ru', 'www.livelib.ru']
    start_urls = ['https://www.livelib.ru/find']

    custom_headers = {
        ':authority:': 'www.livelib.ru',
        ':method:': 'GET',
        ':scheme:': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cahce',
        'Dnt': '1',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?1',
        'Sec-Ch-Ua-Platform': '"Android"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.livelib.ru/book/1000835130-rossiya-v-evrope-po-materialam-mezhdunarodnogo-proekta-evropejskoe-sotsialnoe-issledovanie',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Content-Length': '268',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.188',
        'X-Requested-With': 'XMLHttpRequest'
    }

    custom_cookies = {
        '__ddg1_': 'XR1IzhP6AW7V7Gfjjata',
        'LiveLibId': '4cfcc567dda02071eee09dca94ff232d',
        '__ll_tum': '579836457',
        '__llutmz': '-600',
        '__llutmf': '0',
        'll_asid': '1371254432',
        'SL_GWPT_Show_Hide_tmp': '1',
        'SL_wptGlobTipTmp': '1',
        '__ll_fv': '1690682303',
        '__ll_dvs': '5',
        'closed_vkid_onetap': '1',
        '__ll_ab_mp': '1',
        '__utnt': 'g0_y0_a15721_u0_c0',
        '__ll_unreg_session': '4cfcc567dda02071eee09dca94ff232d',
        '__ll_unreg_sessions_count': '1',
        '__ll_cp': '1', 'pushsub': '1',
        '__ll_dv': '1691669611',
        '__gr': 'g102c39_g1c12_g1243c1_g1240c2_g533c4_g527c6_g433c4_g1217c4_g1360c2_g1226c2_g430c2_g1143c3_g1140c3_g137c2_g144c1_g146c1_g426c1_g143c1_g394c1_g387c1_g510c2_g520c1_g601c3_g537c34_g549c1_g547c1_g670c1_g641c1_g76c1_g535c1_g518c1_g611c30_g107c1_'
    }


    def start_requests(self):
        # isbn_massiv = ['978-5-6044767-4-1']
        isbn_massiv = ['978-5-6044767-4-1',
             '978-5-6044767-7-2',
             '978-5-9500341-0-7',
             '978-9934-8753-1-1',
             '978-5-600-01715-3']
        for isbn in isbn_massiv:
            link = f"https://www.livelib.ru/find/{isbn}"
            yield scrapy.Request(url=link, callback=self.parse_page, headers=self.custom_headers, method="GET", cookies=self.custom_cookies)

    def parse_page(self, response):
        book_links = response.css('.find-book-block a::attr(href)').getall()
        # надо прописать условия на 0 и больше 1 ссылки
        for book_link in book_links:
            yield response.follow(url=book_link, callback=self.parse_book)

    def parse_book(self, response):
        description = response.css('#lenta-card__text-edition-escaped::text').get()
        if description:
            description = description.strip()
            description = re.sub(r'\s+', ' ', description)
            yield {
                'description': description.strip()
            }
        else:
            yield {
                'description': '-'
            }
