import sqlite3
import csv

con = sqlite3.connect('database/slow_books_database.db')

cur = con.cursor()

cur.execute("SELECT ISBN, Publisher, COUNT(*) FROM book_description GROUP BY ISBN HAVING COUNT(*) > 1")

result = cur.fetchall()

number_of_books = 12833

with open('database/statistic.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["ISBN", "Number", "%", "Publisher"])
    for row in result:
        isbn = row[0],
        publisher = row[1]
        count = row[2]
        writer.writerow([isbn, count, count * 100 / number_of_books, publisher])

con.close()
