import sqlite3

sqliteConnection = sqlite3.connect('sql.db')

cursor = sqliteConnection.cursor()
print('DB Init')

query = 'SQL query;'
cursor.execute(query)
result = cursor.fetchall()
print('SQLiteVersion is {}'.format(result))