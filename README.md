# scraper_project
проект парсера

Описание проекта есть существующая база данных "Медленных книг"(около 13000 книг), которую мы очищаем, далее для каждой книги по isbn (международный стандартный книжный номер) находим соответсвующее описание, жанр, обложку, оценку и количество отзывов с livelib; оценку, колчество отзывов, описание, количество покупок и обложку с book24, записываем данные в бд (slow_books_database).

Описание стэка: проект реализован на python, с использованием следующих библиотек:

scrapy (создание паука)
pandas (работа с csv файлами)
re (очистка бд и полученных данных от парсера) 
испольванная бд - sqlite3

Описание классов и методов: 

ksusa_branch
  class BestsellerItem - класс создаёт scrapy item
  class BookSpider - паук для парсинга книг с livelib
    def parse_book возвращает основные характеристики книги
    def parse_description возвращает полное описание
    def parse_rate возвращает словарь с оценками
  
  class ItemPipeline - класс  получает scrapy item и очищает его
    def process_item  с помощью регулярок очищает поля item
  class DatabasePipeline - класс для записи в отдельную таблицу в бд
    def __init__ 
    def create_table если таблицы не существует, то данный метод метод создаёт её
    def process_item записывает очищенный item  в бд
    
galbranch
  class ParsingItem - класс создаёт scrapy item
    ID - id для записи в бд и связки таблицей book_description в бд
    isbn - уникальный идентификационный номер книги, с помощью него ищем книги на сайте
    book24_score - оценка книги на book24 
    book24_feedback - количество оценок пользователей на book24
    number_of_buyers - количество покупок книги
    description - описание книги
    book_cover - ссылка на обложку книги
  class Book24Spider - паук для парсинга с book24
    def __init__ - конструктор класса
    def start_requests - отправлет запрос на book24
    def parse_link - возращает ссылку на страницу книги
    def parse_book - собирает информацию со страницы книги и заполняет поля в item
  class ItemPipeline - класс  получает scrapy item и очищает его
    def process_item  с помощью регулярок очищает поля item
  class DatabasePipeline - класс для записи в отдельную таблицу в бд
    def __init__ - конструктор класса 
    def create_table если таблицы не существует, то данный метод метод создаёт её
    def process_item записывает очищенный item  в бд

База данных:
Таблицы:
  book_description:
    ID,
    ISBN - международный стандартный книжный номер,
    Author,
    Name,
    Publisher - издательство,
    City,
    Year,
    Serias - серия,
    Date,
    Annotation,
  book_characteristics
    ID,
    Number_of_pages - количество страниц,
    Format - формат?,
    Size,
    Weight,
    Wrapper_type - тип обложки,
    Standart - стандарт?,
  business_info
    ID,
    Booking - заказ,
    Cost_rub- цена в рублях,
    Availiablitility - наличие,
    Circulation - тираж,
    In_storage - на складе,
    Prepaytion - предоплата,                  
  book_codes
  ID,
  Code_num - код_цифр,
  Code_txt - код_букв
    
История обновлений: 
upd 10.08: переделала импорт базы данных медленных книг, теперь данные отчищены (нет пробелов, знаков пунктуации и тд), пофиксила типы данных. upd 11.08: реструктурировала бд, изменила формат даты, проверяю работу регулярок upd 12.08: отладила работу регулярок, привела колонку вес к единой единице измерения, проверила валидацию

Паук находится parsing/parsing/spiders/book24 База данных и связанные с ней файлы находятся в папке database Вызов паука происходит из файла main.py
