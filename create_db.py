import mysql.connector

my =mysql.connector.connect(
    host="localhost",
    user="root",
    passwd='123',
    )
my_cursor =my.cusor()

my_cursor.execute("CREATE DATABASE our_users")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
