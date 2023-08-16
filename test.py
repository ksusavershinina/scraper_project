import sqlite3

con = sqlite3.connect('database.db')

cur = con.cursor()

cur.execute("""
    SELECT Code_num, Code_txt
    FROM book_codes
""")
type_massive = [int, str]
result = cur.fetchall()
errors = 0
for i in result:
    for j in range(len(i)):
        if type(i[j]) != type_massive[j] and i[j] != None:
            errors += 1
            print(j, i[j])
print('errors', errors)

con.close()