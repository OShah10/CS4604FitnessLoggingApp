import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='muid1111',
    port='3306',
    database='Project'
)

mycursor = mydb.cursor()
mycursor.execute('insert into Persons(id,name) values(6,"Bob")')
mycursor.execute("select * from Persons")
data = mycursor.fetchall()
for i in data:
    print("name:", i[1])