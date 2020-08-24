# import mysql.connector
import MySQLdb


db = MySQLdb.connect(host="localhost", user="root", password="Myp@sswordis123")

# print(db)

mycursor = db.cursor()

mycursor.execute("Show databases")

for db in mycursor:
    print(db)
