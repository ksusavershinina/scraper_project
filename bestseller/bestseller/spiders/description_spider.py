import scrapy
import logging
from scraper_project.bestseller.bestseller.items import DescriptionItem


class DescriptionSpider(scrapy.Spider):
    name = 'description_spider'
    allowed_domains = ['www.livelib.ru/feed', ]
    custom_settings = {
        'LOG_FILE': 'logs.txt',
        'LOG_FILE_APPEND': True,
        'LOG_SHORT_NAMES': True,
        'ITEM_PIPELINES': {
            'scraper_project.bestseller.bestseller.pipelines.DescriptionPipeline': 300,
            'scraper_project.bestseller.bestseller.pipelines.DescriptionDatabasePipeline': 400,
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
    }

    headers_for_desc = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Dnt': '1', 'Origin': 'https://www.livelib.ru', 'Pragma': 'no-cache',
                        'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                        'Sec-Ch-Ua-Mobile': '?1', 'Sec-Ch-Ua-Platform': '"Android"', 'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36 Edg/117.0.2045.36',
                        'X-Requested-With': 'XMLHttpRequest'}

    cookies_for_desc = {'__ddg1_': 'XR1IzhP6AW7V7Gfjjata', 'LiveLibId': '4cfcc567dda02071eee09dca94ff232d',
                        '__llutmz': '-600', 'll_asid': '1371254432', 'SL_GWPT_Show_Hide_tmp': '1',
                        'SL_wptGlobTipTmp': '1', '__ll_fv': '1690682303', '__ll_dvs': '5', 'closed_vkid_onetap': '1',
                        '__ll_ab_mp': '1', '__ll_unreg_session': '4cfcc567dda02071eee09dca94ff232d',
                        '__ll_unreg_sessions_count': '1', 'pushsub': '1', '__ll_tum': '826029989', '__ll_cp': '2',
                        '__ddgid_': 'v2x57OEhW0hhj58a', '__ddg2_': 'hj9U1HhbyVRJjBmG',
                        '__gr': 'g1143c1_g1140c1_g601c1_g537c5_g611c2_g519c1_g510c5_g146c1_g137c1_g551c1_g547c1_g764c1_g535c1_g516c1_g602c8_g1121c1_g600c1_g412c1_g434c1_g525c3_g1170c1_g1165c1_g12c1_g8c1_g464c1_g459c1_g609c7_g426c5_g1240c5_g1249c5_g1360c1_g1226c1_',
                        '__ll_vkontakte_oauth': '', '__ll_vkontakte_code': '', 'undefined': '', '__utrx': '1',
                        'llsid': 'a00f07744fb9306ed2bfa2e1248f6345', '__utnx': '13048187221', '__llutmf': '1',
                        '__utnt': 'g2_y51421_a15721_u13048187221_c0', '__ll_dv': '1695380571'}

    def __init__(self, id_arr):
        super(DescriptionSpider, self).__init__()
        self.id_arr = id_arr

    def start_requests(self):
        logging.debug('Spider is starting...')
        id_arr = self.id_arr
        for book_id in id_arr:
            id = book_id[0]
            parametrs = f"object_alias=edition&object_id={id}&is_new_design=ll2019"
            yield scrapy.Request(
                url='https://www.livelib.ru/feed/getfullobjecttext',
                headers=self.headers_for_desc,
                cookies=self.cookies_for_desc,
                method='POST',
                body=parametrs,
                callback=self.parse_description,
                meta={'id': id}
            )

    def parse_description(self, response):
        if response.status == 404:
            logging.error(f"Received 404 for URL: {response.url}")
            return

        logging.debug('Parsing full description...', )
        data = response.json()
        content = data.get('content')

        yield DescriptionItem(
            livelib_id=response.meta.get('id'),
            description=content,
        )

        logging.debug('Complete parsing description')
