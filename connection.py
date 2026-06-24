from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
app = Flask(__name__)

config = {
    'user': 'root',
    'password': '<insert your password here>',
    'host': 'localhost',
    'database': 'healthtracker',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    data = request.form['data']
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (Name) VALUES (%s)", (data,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)