import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Arman1111',
    port = '3306',
    database = 'CandyStore'
)

mycursor = mydb.cursor()

mycursor.execute('show tables;')

tables = mycursor.fetchall()

for i in tables:
    print(i)


mycursor.execute('select * from Customer;')

Customers = mycursor.fetchall()

for j in Customers:
    print(j)
    print('customer name: ', j[1])
    print('customer last name: ', j[2])