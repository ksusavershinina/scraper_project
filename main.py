import pandas as pd
<<<<<<< HEAD
import sqlite3
import re
import numpy as np

df = pd.read_csv('./mk_price_21-07-2023.csv', sep=";")
df['Код_циф'] = pd.to_numeric(df['Код_циф'], errors='coerce')
df['ISBN'] = df['ISBN'].map(lambda x: re.sub('-', '', x))
df['Автор'] = df['Автор'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['Название'] = df['Название'].map(lambda x: re.sub('\W', '', x))
df['Издательство'] = df['Издательство'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float or x == '-' else np.nan)
df['Город'] = df['Город'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['Год'] = df['Год'].map(lambda x: x if re.search(r'\d{4}', str(x)) else np.nan)
# df['Цена'] = df['Цена'].map(lambda x: x if re.search(r'\d{3}', str(x)) else np.nan)
df['Код_бук'] = df['Код_бук'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['Кол-во стр.'] = df['Кол-во стр.'].map(lambda x: x if re.search(r'\d', str(x)) else np.nan)
#df['Формат'] = df['Формат'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
#df['Размер'] = df['Размер'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['Вес'] = df['Вес'].map(lambda x: x if re.search(r'\d', str(x)) else np.nan)
df['Тип обл.'] = df['Тип обл.'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['Серия'] = df['Серия'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['Стандарт'] = df['Стандарт'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['тираж'] = df['тираж'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['на складе'] = df['на складе'].map(lambda x: re.sub('\W', '', str(x)) if type(x) != float else np.nan)
df['Дата'] = df['Дата'].map(lambda x: x if re.search(r'\d{2} \w{3} \d{4}', x) else np.nan)
df['Аннотация'] = df['Аннотация'].map(lambda x: re.sub('\W', '', x) if type(x) != float else np.nan)
df['предоплата'] = df['предоплата'].map(lambda x: re.sub('\W', '', x) if type(x) != float else np.nan)


=======
import csv
import sqlite3
import re

df = pd.read_csv("D:\OneDrive\Рабочий стол\mk_price_21-07-2023.csv", sep=";")
>>>>>>> 8877408 (add database)

con = sqlite3.connect('database.db')

cur = con.cursor()

df.to_sql(
<<<<<<< HEAD
    name='slow_books_database',
=======
    name='table1',
>>>>>>> 8877408 (add database)
    con=con,
    if_exists='replace',
    index=False,
    dtype={
        'Заказ': 'text',
        'Код_циф': 'integer',
<<<<<<< HEAD
        'ISBN': 'real',
=======
        'ISBN': 'REAL',
>>>>>>> 8877408 (add database)
        'Автор': 'text',
        'Название': 'text',
        'Издательство': 'text',
        'Город': 'text',
<<<<<<< HEAD
        'Год': 'integer',
        'Цена': 'real',
        'Код_бук': 'text',
=======
        'Год': 'real',
        'Цена': 'real',
        'Код_бук': 'real',
>>>>>>> 8877408 (add database)
        'Кол-во стр.': 'real',
        'Формат': 'text',
        'Размер': 'text',
        'Вес': 'real',
        'Тип обл.': 'text',
        'Серия': 'text',
<<<<<<< HEAD
        'Стандарт': 'text',
=======
        'Стандарт': 'real',
>>>>>>> 8877408 (add database)
        'Наличие': 'text',
        'тираж': 'text',
        'на складе': 'text',
        'Дата': 'blob',
        'Аннотация': 'text',
        'предоплата': 'text'
    }
)

<<<<<<< HEAD
cur.execute("""
    SELECT ISBN, Название
    FROM slow_books_database
=======

cur.execute("""
    SELECT ISBN, Название  
    FROM table1 
>>>>>>> 8877408 (add database)
    WHERE ISBN NOT IN ('-')
""")

result = cur.fetchall()

<<<<<<< HEAD
# for i in result:
    # print(i)
=======
for i in result:
    print(i)
>>>>>>> 8877408 (add database)

con.close()
