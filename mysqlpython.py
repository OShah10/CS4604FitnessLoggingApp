import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'YouWontPass',
    port = '3306',
    database = 'health_tracker'
)

mycursor = mydb.cursor()

mycursor.execute('show tables;')

tables = mycursor.fetchall()
for (i) in tables:
    print(i)