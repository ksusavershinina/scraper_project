import pandas as pd
import sqlite3
import re
import numpy as np
import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')

def clean_str(column_name):
    df[column_name] = df[column_name].map(lambda x: re.sub('[\n\t]', '', str(x)) if (type(x) != float and not(re.search(r'^\W{1}', x))) else np.nan)

def clean_numbers(column_name):
    df[column_name] = df[column_name].map(lambda x: re.sub(r'\D', '', str(x)) if (type(x) != float and not(re.search(r'^[а-я]*', x))) else np.nan)
    df[column_name] = df[column_name].map(lambda x: re.sub(r'\d*[-,;.+]', '', str(x)) if (type(x) != float) else np.nan)

def clean_isbn(column_name):
    df[column_name] = df[column_name].map(lambda x: re.sub('-', '', x) if (type(x) != float and not(re.search(r'^\W{1}', x))) else np.nan)

def сlean_date(column_name):
    df[column_name] = df[column_name].map(lambda x: x if re.search(r'\d{2} \w{3} \d{4}', x) else np.nan)
    df[column_name] = df[column_name].map(lambda x: dt.datetime.strptime(x, '%d %b %Y').strftime('%d-%m-%Y'))

def clean_cost(column_name):
    df[column_name] = df[column_name].map(
        lambda x: re.sub('₽', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)

def clean_wieght(column_name):
    df[column_name] = df[column_name].map(lambda x: re.sub(',', '.', x) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
    df[column_name] = df[column_name].map(lambda x: float(x) / 1000 if not (re.search('[.]', str(x))) else x)



df = pd.read_csv('./mk_price_21-07-2023.csv', sep=";")

df['Код_циф'] = pd.to_numeric(df['Код_циф'], errors='coerce')
clean_isbn('ISBN')

columns_with_str = ('Автор', 'Название', 'Издательство', 'Город', 'Код_бук', 'Формат', 'Размер', 'Тип_обл', 'Серия', 'Стандарт', 'тираж', 'на_складе', 'Аннотация', 'предоплата')
for i in columns_with_str:
    clean_str(i)

columns_with_numbers = ('Год', 'Колво_стр')
for i in columns_with_numbers:
    clean_numbers(i)

clean_wieght('Вес')
clean_cost('Цена')
сlean_date('Дата')

con = sqlite3.connect('database.db')

cur = con.cursor()

df.to_sql(
    name='slow_books_database',
    con=con,
    if_exists='replace',
    index=False,
    dtype={
        'Заказ': 'text',
        'Код_циф': 'integer',
        'ISBN': 'text',
        'Автор': 'text',
        'Название': 'text',
        'Издательство': 'text',
        'Город': 'text',
        'Год': 'integer',
        'Цена': 'real',
        'Код_бук': 'text',
        'Колво_стр': 'integer',
        'Формат': 'text',
        'Размер': 'text',
        'Вес': 'real',
        'Тип_обл': 'text',
        'Серия': 'text',
        'Стандарт': 'text',
        'Наличие': 'text',
        'тираж': 'text',
        'на_складе': 'text',
        'Дата': 'blob',
        'Аннотация': 'text',
        'предоплата': 'text'
    }
)

cur.execute("""
    CREATE TABLE IF NOT EXISTS book_description
    (ID INTEGER PRIMARY KEY,
    ISBN text,
    Author text,
    Name text,
    Publisher text,
    City text,
    Year integer,
    Serias text,
    Date blob,
    Annotation text)
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS book_characteristics
    (ID INTEGER PRIMARY KEY,
    Number_of_pages integer,
    Format text,
    Size text,
    Weight real,
    Wrapper_type text,
    Standart text)
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS business_info
    (ID INTEGER PRIMARY KEY,
    Booking text,
    Cost_rub real,
    Availability text,
    Circulation text,
    In_storage text,
    Prepayment text)
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS book_codes
    (ID INTEGER PRIMARY KEY,
    Code_num integer,
    Code_txt text)
""")

cur.execute("""
    INSERT INTO book_description
    SELECT NULL
    ID,
    ISBN,
    Автор,
    Название,
    Издательство,
    Город,
    Год,
    Серия,
    Дата,
    Аннотация
    FROM slow_books_database
""")

cur.execute("""
    INSERT INTO book_characteristics
    SELECT NULL
    ID,
    Колво_стр,
    Формат,
    Размер,
    Вес,
    Тип_обл,
    Стандарт
    FROM slow_books_database
""")

cur.execute("""
    INSERT INTO business_info
    SELECT NULL
    ID,
    Заказ,
    Цена,
    Наличие,
    тираж,
    на_складе,
    предоплата
    FROM slow_books_database
""")

cur.execute("""
    INSERT INTO book_codes
    SELECT NULL
    ID,
    Код_циф,
    Код_бук
    FROM slow_books_database
""")

cur.execute("DROP TABLE slow_books_database")

con.commit()

con.close()