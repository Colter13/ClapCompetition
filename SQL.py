import sqlite3

try:
    sqliteConnection = sqlite3.connect('ClapCompetition.db')
    cursor = sqliteConnection.cursor()
    print('DB Init')

    query = '''
    create table Person(
        PersonID int Primary Key not null,
        FirstName varchar(15),
        LastName varchar(15)
    )

    '''
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)

    cursor.close()

# handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)

# close connection
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')