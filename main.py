import pandas as pd
import csv
import sqlite3
import re

df = pd.read_csv("D:\OneDrive\Рабочий стол\mk_price_21-07-2023.csv", sep=";")

con = sqlite3.connect('database.db')

cur = con.cursor()

df.to_sql(
    name='table1',
    con=con,
    if_exists='replace',
    index=False,
    dtype={
        'Заказ': 'text',
        'Код_циф': 'integer',
        'ISBN': 'REAL',
        'Автор': 'text',
        'Название': 'text',
        'Издательство': 'text',
        'Город': 'text',
        'Год': 'real',
        'Цена': 'real',
        'Код_бук': 'real',
        'Кол-во стр.': 'real',
        'Формат': 'text',
        'Размер': 'text',
        'Вес': 'real',
        'Тип обл.': 'text',
        'Серия': 'text',
        'Стандарт': 'real',
        'Наличие': 'text',
        'тираж': 'text',
        'на складе': 'text',
        'Дата': 'blob',
        'Аннотация': 'text',
        'предоплата': 'text'
    }
)


cur.execute("""
    SELECT ISBN, Название  
    FROM table1 
    WHERE ISBN NOT IN ('-')
""")

result = cur.fetchall()

for i in result:
    #print(re.sub(r'\W', '', i[1]))
    print(re.sub(r'-', '', i[0]))
    #print(i)

con.close()
