import scrapy
import re

class BookSpider(scrapy.Spider):
    name = 'livelib'
    start_urls = ['https://www.livelib.ru/find']

    headers = {
        'Host': 'www.livelib.ru',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64; rv: 109.0) Gecko / 20100101 Firefox / 116.0',
        'Accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, * / *;q = 0.8',
        'Accept - Language': 'ru - RU, ru; q = 0.8, en - US; q = 0.5, en; q = 0.3',
        'Accept - Encoding': 'gzip, deflate',
        'Upgrade - Insecure - Requests': '1',
        'Sec - Fetch - Dest': 'document',
        'Sec - Fetch - Mode': 'navigate',
        'Sec - Fetch - Site': 'none',
        'Sec - Fetch - User': '?1'
    }

    cookieString = '__ddg1_=VDh13kXeUwVWhy8DxvHu; __ll_tum=1877629280; _ga_90RPM8SDHL=GS1.1.1691221633.3.1.1691221743.20.0.0; _ga=GA1.2.360621380.1691146407; __llutmz=-600; __llutmf=0; __ll_fv=1691146409; __ll_dv=1691221741; __ll_cp=6; __ll_popup_count_pviews=mailc1_; _gid=GA1.2.1227887881.1691146424; tmr_lvid=cee4b20ebf3c74fe45044991249f2bf3; tmr_lvidTS=1691146424800; tmr_detect=0%7C1691221748055; __r=pc4340c1_; __ll_ab_mp=1; __ll_unreg_session=dfed4f2ab4423f6fde59ba810f74b88e; __ll_unreg_sessions_count=2; pushsub=1; __gr=g144c1_g137c1_g1240c1_; LiveLibId=dfed4f2ab4423f6fde59ba810f74b88e; __ll_dvs=5; ll_asid=1377305511; promoLLid=tbqammr3dqoe4sk6apue7054b7; showed_vkid_onetap=1; __utnt=g0_y0_a15721_u0_c0'

    cookies = {}

    for i in cookieString.split(';'):
        key = i.split('=')[0]
        value = i.split('=')[1]
        cookies[key] = value

    handle_httpstatus_list = [400]

    def parse(self, response):

        a = ['978-5-907532-14-4',
             '978-5-6046148-1-5',
             '978-5-6044208-9-8',
              '978-5-6045105-4-4',
              '978-5-6044244-5-2',
              '978-5-91103-591-4',
              '978-5-91103-214-2',
              '978-5-91103-515-0',
              '978-5-91103-603-4',
              '978-5-91103-588-4']
        for isbn in a:
            link = f"https://www.livelib.ru/find/{isbn}"
            yield response.follow(link, callback=self.parse_book, cookies=self.cookies, headers=self.headers)


    def parse_book(self, response):
        #description = response.css('div#lenta-card__text-edition-escaped::text').get()
        #description = description.strip()
        #description = re.sub(r'\s+', ' ', description)
        pass

        #yield {
        #    'description': description
        #}


# response.css("a.slide-book__link::attr(href)").get()

 # response.css('div#lenta-card__text-edition-escaped::text').get()