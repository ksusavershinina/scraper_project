import  sqlite3
import csv

con = sqlite3.connect('slow_books_database.db')

cur = con.cursor()

cur.execute("SELECT COUNT(*) FROM parsed_books WHERE description IS NULL")
result = cur.fetchall()


print(result)

con.close()