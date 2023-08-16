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


def сlean_date(column_name):
    df[column_name] = df[column_name].map(lambda x: x if re.search(r'\d{2} \w{3} \d{4}', str(x)) else np.nan)
    #df[column_name] = df[column_name].map(lambda x: dt.datetime.strptime(str(x), '%d %b %Y').strftime('%d-%m-%Y'))


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
        сlean_date(column_name)
    else:
        pass


def create_table(table_name):
    query = f"CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT)"
    # for column, datatype in column_dic.items():
    #     query += f"{column} {datatype}, "
    #
    # query = query[:-2] + ")"
    cur.execute(query)

def add_column(table_name, column_name, datatype):
    query = f"AlTER TABLE {table_name} ADD COLUMN {column_name} {datatype}"
    cur.execute(query)

# def update_data(table_name, data_frame):
#     query = f"INSERT INTO {table_name} SELECT NULL ID, "
#     for column, values in data_frame.items():
#         query += f"{column}, "
#
#     query = query[:-2]
#
#     cur.execute(query)

con = sqlite3.connect('slow_books_database.db')

cur = con.cursor()

df = pd.read_csv('./mk_price_21-07-2023.csv', sep=";")

columns_with_str = (
    'Booking', 'Author', 'Name', 'Publisher', 'City', 'Code_txt', 'Format', 'Size', 'Wrapper_type', 'Serias',
    'Standart', 'Circulation',
    'Availiablitility', 'In_storage', 'Annotation', 'Prepaytion')
columns_with_numbers = ('Code_num', 'Year', 'Number_of_pages')

tables_names = ('book_description', 'book_characteristics', 'business_info', 'book_codes')

book_description_dic = {
    'ISBN': 'text',
    'Author': 'text',
    'Name': 'text',
    'Publisher': 'text',
    'City': 'text',
    'Year': 'integer',
    'Serias': 'text',
    'Date': 'blob',
    'Annotation': 'text'
}

book_characteristics_dic = {
    'Number_of_pages': 'integer',
    'Format': 'text',
    'Size': 'text',
    'Weight': 'real',
    'Wrapper_type': 'text',
    'Standart': 'text'
}

business_info_dic = {
    'Booking': 'text',
    'Cost_rub': 'real',
    'Availiablitility': 'text',
    'Circulation': 'text',
    'In_storage': 'text',
    'Prepaytion': 'text'
}

book_codes_dic = {
    'Code_num': 'integer',
    'Code_txt': 'text'
}

book_description_lst = ('ID', 'ISBN', 'Author', 'Name', 'Publisher', 'City', 'Year', 'Serias', 'Date', 'Annotation')
# book_characteristics_lst = ('Колво_стр', 'Формат', 'Размер', 'Вес', 'Тип_обл', 'Стандарт')
# business_info_lst = ('Заказ', 'Цена', 'Наличие', 'тираж', 'на_складе', 'предоплата')
# book_codes_lst = ('Код_циф', 'Код_бук')
#
tables = {'book_description': book_description_dic,
          'book_characteristics': book_characteristics_dic,
          'business_info': business_info_dic,
          'book_codes': book_codes_dic}

for tables_name in tables_names:
    create_table(tables_name)

# for column in df:
#     clean(column)
#     for tables_name, table_column_dic in tables.items():
#         if column in table_column_dic.keys():
#             df[column].to_sql(tables_name, con, if_exists='append', index=False)

# for table_name, table_column_dic in tables.items():
#     query = f"INSERT INTO {table_name} {table_column_dic.keys()} VALUES (NULL, "
#     params = []
#     for column in df:
#         if column in table_column_dic.keys():
#             clean(column)
#             query += f"?, "
#             params.append(column)
#     query = query[:-2] + ")"
#     cur.executemany(query, params)

for column in df:
    clean(column)
    values = df[column].tolist()
    for tables_name, table_column_dic in tables.items():
        if column in table_column_dic.keys():
            add_column(tables_name, column, table_column_dic[column])
            for value in values:
                cur.execute(f"INSERT INTO {tables_name} ({column}) VALUES(?)", (value,))

con.commit()

con.close()
