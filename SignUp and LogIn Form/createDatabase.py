import sqlite3

connection = sqlite3.connect('./Databases/database.db')

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(userName text,fullName text,gender text,password text)")

connection.commit()

connection.close()