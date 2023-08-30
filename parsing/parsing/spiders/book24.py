import scrapy
from scraper_project.parsing.parsing.items import ParsingItem


class Book24Spider(scrapy.Spider):
    name = "book24"
    allowed_domains = ["book24.ru", "book24.ru/search"]

    headers = {
        'host': 'book24.ru',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Cache-Control': 'max-age=0',
        'If-Modified-Since': 'Sunday, 20-Aug-2023 10:25:58 GMT',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': "navigate",
        "Sec-Fetch-Site": "same-origin",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
    }

    cookie = {
        'g4c_x': '1', 'gdeslon.ru.__arc_aid': '91052',
        'gdeslon.ru.__arc_token': '0738e1159429026c1a03ee720bff78333a46959c', 'gdeslon.ru.__arc_domain': 'gdeslon.ru',
        '_ym_d': '1692319734', '_ym_uid': '1692319734716127214', '_gid': 'GA1.2.629691625.1692319734',
        '_ga_T9TF1ZMWX4': 'GS1.1.1692319734.1.0.1692319734.0',
        'BITRIX_SM_book24_visitor_id': 'c5871259-212e-43df-a299-504b2d195da3',
        'b24DiscountUrlRequest': 'utm_source%3Dgdeslon',
        'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
        'gdeslon.ru.user_id': 'b8242c4c-fe2f-4aee-af01-9684653093c9', 'analytic_id': '1692319737759745',
        'adid': '169231973823187', 'tmr_lvid': 'a0571016a34eb8b4d364c8261681821d', 'tmr_lvidTS': '1692319944644',
        'BITRIX_SM_location_name': '%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%B2%D0%BE%D1%81%D1%82%D0%BE%D0%BA',
        'BITRIX_SM_location_code': '7b6de6a5-86d0-4735-b11a-499081111af8', 'BITRIX_SM_location_country': 'RU',
        'BITRIX_SM_location_region_code': '3909681-d6e1-432d-b61f-ddac393cb5da',
        'ssaid': 'f90eb70-3d61-11ee-9cae-e1163324d6f9',
        '_tt_enable_cookie': '1', '_ttp': 'OUBb9Ye25hhQ5I-DgrpgbBFctyL',
        'BITRIX_SM_location_coords': '%5B%2243.116391%22%2C%22131.882421%22%5D',
        'flocktory-uuid': 'b1acca01-d45e-4503-87f5-36625abfba41-5', 'g4c_x': '1',
        '_ym_isad': '2', 'PHPSESSID': 'ZgkeemUib2tE08jPW3J054Hxl9SAxTBj',
        'mindboxDeviceUUID': '1026951b-32c4-4053-8dc6-5e2b3b335173',
        'directCrm - session': '7B%22deviceGuid%22%3A%221026951b-32c4-4053-8dc6-5e2b3b335173%22%7D',
        'directCrm-session': '%7B%22deviceGuid%22%3A%221026951b-32c4-4053-8dc6-5e2b3b335173%22%7D', 'ym_visorc': 'b',
        '_ga': 'GA1.2.418833563.1692319734', 'tmr_detect': '0%7C1692527170651', '__tld__': 'null',
        'COOKIES_ACCEPTED': 'Y',
        '_ga_L57STKDPVC': 'GS1.1.1692527166.17.1.1692527376.58.0.0'
    }

    def __init__(self, isbn_list):
        super(Book24Spider, self).__init__()
        self.isbn_list = isbn_list

    def start_requests(self):
        for isbn in self.isbn_list:
            yield scrapy.Request(
                url='https://book24.ru/search/?q={}'.format(isbn), callback=self.parse_link,
                headers=self.headers, method='GET', cookies=self.cookie)

    def parse_link(self, response, **kwargs):
        book_link = response.css('.product-card__content a::attr(href)').get()
        if not book_link:

            book_item = ParsingItem(
                book24_score=None,
                book24_feedback=None,
                number_of_buyers=None,
                description=None,
                book_cover=None
            )

            yield book_item

        else:
            yield scrapy.Request(
                url='https://book24.ru{}'.format(book_link),
                headers=self.headers, callback=self.parse_book)

    def parse_book(self, response, **kwargs):
        book24_score = response.css('.rating-widget__main-text::text').getall()[0]
        book24_feedback = response.css('.rating-widget__other-text::text').getall()[0]
        number_of_buyers = response.css('.product-detail-page__purchased-text::text').get()
        description = response.css('.product-about__text p::text').getall()
        book_cover = response.css('img.product-poster__main-image::attr(src)').get()

        book_item = ParsingItem(
            book24_score=book24_score,
            book24_feedback=book24_feedback,
            number_of_buyers=number_of_buyers,
            description=description,
            book_cover=book_cover
        )

        yield book_item
