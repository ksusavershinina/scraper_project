import pandas as pd
import sqlite3
import re
import numpy as np
import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')

df = pd.read_csv('./mk_price_21-07-2023.csv', sep=";")
df['Код_циф'] = pd.to_numeric(df['Код_циф'], errors='coerce')
df['ISBN'] = df['ISBN'].map(lambda x: re.sub('-', '', x))
df['Автор'] = df['Автор'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Название'] = df['Название'].map(lambda x: re.sub('\W', '', x))
df['Издательство'] = df['Издательство'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Город'] = df['Город'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Год'] = df['Год'].map(lambda x: re.sub('\D', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Цена'] = df['Цена'].map(lambda x: re.sub('[\s₽]', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Цена'] = df['Цена'].map(lambda x: re.sub(',', '.', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Код_бук'] = df['Код_бук'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Колво_стр'] = df['Колво_стр'].map(lambda x: re.sub('\D', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Формат'] = df['Формат'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Размер'] = df['Размер'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Вес'] = df['Вес'].map(lambda x: re.sub(',', '.', x) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Вес'] = df['Вес'].map(lambda x: float(x) / 1000 if not(re.search('[.]', str(x))) else x)
df['Тип_обл'] = df['Тип_обл'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Серия'] = df['Серия'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Стандарт'] = df['Стандарт'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['тираж'] = df['тираж'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['на_складе'] = df['на_складе'].map(lambda x: re.sub('\W', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['Дата'] = df['Дата'].map(lambda x: x if re.search(r'\d{2} \w{3} \d{4}', x) else np.nan)
df['Дата'] = df['Дата'].map(lambda x: dt.datetime.strptime(x, '%d %b %Y').strftime('%d-%m-%Y'))
df['Аннотация'] = df['Аннотация'].map(lambda x: re.sub('\W', '', x) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
df['предоплата'] = df['предоплата'].map(lambda x: re.sub('\W', '', x) if (type(x) != float and re.search(r'\W+', x)) else np.nan)

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
        'Год': 'text',
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
    CREATE TABLE book_description
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
    CREATE TABLE book_characteristics
    (ID INTEGER PRIMARY KEY,
    Number_of_pages integer,
    Format text,
    Size text,
    Weight real,
    Wrapper_type text,
    Standart text)
""")

cur.execute("""
    CREATE TABLE business_info
    (ID INTEGER PRIMARY KEY,
    Booking text,
    Cost_rub real,
    Availability text,
    Circulation text,
    In_storage text,
    Prepayment text)
""")

cur.execute("""
    CREATE TABLE book_codes
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


# cur.execute("""
#     SELECT ISBN, Название
#     FROM slow_books_database
#     WHERE ISBN NOT IN ('-')
# """)
#
# result = cur.fetchall()
#
# for i in result:
#     if i != np.nan:
#         print(i)

con.commit()

con.close()