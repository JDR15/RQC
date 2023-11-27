import mysql.connector

database= mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='sistemaEducativo2',
    port='3306'
    )

print(database)

