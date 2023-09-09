import pandas as pd
import sqlite3
import re
import numpy as np
import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')


def clean_str(column_name):
    df[column_name] = df[column_name].map(
        lambda x: re.sub('[\n\t]', '', str(x)) if (type(x) != float and not (re.search(r'^[.,\s-]$', x))) else np.nan)


def clean_numbers(column_name):
    df[column_name] = df[column_name].map(
        lambda x: re.sub(r'\D', '', str(x)) if (
                type(x) != float and not (re.search(r'^[.,\w\s-]$', str(x)))) else np.nan)
    df[column_name] = df[column_name].map(lambda x: re.sub(r'\d*[-,;.+]', '', str(x)) if (type(x) != float) else np.nan)


def clean_isbn(column_name):
    df[column_name] = df[column_name].map(
        lambda x: re.sub('-', '', x) if (type(x) != float and not (re.search(r'^\W{1}', str(x)))) else np.nan)


def clean_date(column_name):
    df[column_name] = df[column_name].map(lambda x: x if re.search(r'\d{2} \w{3} \d{4}', str(x)) else np.nan)
    df[column_name] = df[column_name].map(lambda x: dt.datetime.strptime(str(x), '%d %b %Y').strftime('%d-%m-%Y'))


def clean_cost(column_name):
    df[column_name] = df[column_name].map(
        lambda x: re.sub('₽', '', str(x)) if (type(x) != float and re.search(r'\W+', x)) else np.nan)


def clean_weight(column_name):
    df[column_name] = df[column_name].map(
        lambda x: re.sub(',', '.', x) if (type(x) != float and re.search(r'\W+', x)) else np.nan)
    df[column_name] = df[column_name].map(lambda x: float(x) / 1000 if not (re.search('[.]', str(x))) else x)


def clean(column_name):
    if column_name in columns_with_numbers:
        clean_numbers(column_name)
    elif column_name in columns_with_str:
        clean_str(column_name)
    elif column_name == 'ISBN':
        clean_isbn(column_name)
    elif column_name == 'Weight':
        clean_weight(column_name)
    elif column_name == 'Cost_rub':
        clean_cost(column_name)
    elif column_name == 'Date':
        clean_date(column_name)
    else:
        pass


def create_table(table_name, column_dic):
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column, datatype in column_dic.items():
        query += f"{column} {datatype}, "

    query = query[:-2] + ")"
    cur.execute(query)


con = sqlite3.connect('slow_books_database.db')

cur = con.cursor()

df = pd.read_csv('mk_price_21-07-2023.csv', sep=";")

columns_with_str = (
    'Booking', 'Author', 'Name', 'Publisher', 'City', 'Code_txt', 'Format', 'Size', 'Wrapper_type', 'Serias',
    'Standart', 'Circulation',
    'Availiablitility', 'In_storage', 'Annotation', 'Prepaytion')
columns_with_numbers = ('Code_num', 'Year', 'Number_of_pages')

tables = {
    'book_description': {'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                         'ISBN': 'text',
                         'Author': 'text',
                         'Name': 'text NOT NULL',
                         'Publisher': 'text',
                         'City': 'text',
                         'Year': 'integer',
                         'Serias': 'text',
                         'Date': 'blob',
                         'Annotation': 'text'},
    'book_characteristics': {'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                             'Number_of_pages': 'integer',
                             'Format': 'text',
                             'Size': 'text',
                             'Weight': 'real',
                             'Wrapper_type': 'text',
                             'Standart': 'text'},
    'business_info': {'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                      'Booking': 'text',
                      'Cost_rub': 'real NOT NULL',
                      'Availiablitility': 'text',
                      'Circulation': 'text',
                      'In_storage': 'text',
                      'Prepaytion': 'text'},
    'book_codes': {'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                   'Code_num': 'integer NOT NULL ',
                   'Code_txt': 'text'}}

for tables_name, columns_dic in tables.items():
    create_table(tables_name, columns_dic)

for tables_name, table_column_dic in tables.items():
    data = pd.DataFrame()
    for column in df:
        if column in table_column_dic.keys():
            clean(column)
            data.insert(len(data.columns), column, df[column])
    data.to_sql(tables_name, con, if_exists='append', index=False)

con.commit()

con.close()
