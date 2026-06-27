from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
app = Flask(__name__)

config = {
    'user': 'root',
    'password': '<insert your password here>',
    'host': 'localhost',
    'port' : '3306',
    'database': 'health_tracker'
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

@app.route('/create_account')
def acct_create():
    return render_template('create_acct.html')
        
@app.route('/user_sign')
def usign():
    return render_template('user_sign.html')

@app.route('/add_acct', methods=['POST'])
def add_acct():
    fname = request.form['fname']
    lname = request.form['lname']
    sx = request.form['sex']
    height = request.form['height']
    weight = request.form['weight']
    email = request.form['email']
    dob = request.form['birthday']
    conn = mysql.connector.connect(**config)
    mycursor = conn.cursor()
#create a user with privilege level 'u' as default
    insert_params = (fname,lname,email,dob,height,weight,'u')
    
    mycursor.execute("INSERT INTO Users (Fname, Lname, Email, Birthdate, Height, Weight, Privilege)"
    "VALUES (%s,%s,%s,%s,%s,%s,%s)",insert_params)
    #check that the addition was successful
    conn.commit()
    #get user ID
    uid = mycursor.lastrowid
    print("User created. ID: ", uid)
    mycursor.close()
    conn.close()
    return redirect(url_for('user',userid = uid)) #placeholder for now, redirects to user page

@app.route('/user_signin')
def signin():
    print("arguments:", request.args)
    data = request.args['email']
    print("email:", data)
    conn = mysql.connector.connect(**config)
    cursed = conn.cursor()
    #find a user with that specific email address
    params = (data,)
    query = "SELECT UserID, Fname FROM USERS WHERE Email = %s"
    cursed.execute(query, params)
    #get results
    results = cursed.fetchall()
    cursed.close()
    conn.close()
    if len(results) == 0:
        print("User not found")
        return render_template('user_sign.html')
    else:
        uid, fname = results[0]
        print("Found user")
        return redirect(url_for('user',userid = uid))


@app.route('/log_meal/<userid>')
def log_meal(userid):
    return render_template('log_meal.html', uid=userid)


@app.route('/add_meal/<userid>', methods=['POST'])
def add_meal(userid):
    name = request.form['name']
    calories = request.form['calories']
    notes = request.form['notes']
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Meals (UserID, Name, Calories, Notes) VALUES (%s, %s, %s, %s)",
        (userid, name, calories, notes)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('user', userid=userid))


@app.route('/log_exercise/<userid>')
def log_exercise(userid):
    return render_template('log_exercise.html', uid=userid)


@app.route('/add_exercise/<userid>', methods=['POST'])
def add_exercise(userid):
    name = request.form['name']
    calories_burned = request.form['calories_burned']
    duration = request.form['duration']
    effort_rating = request.form['effort_rating']
    done = request.form['done']
    notes = request.form['notes']
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Exercises (UserID, Name, Calories_Burned, Duration, Effort_Rating, Done, Notes) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (userid, name, calories_burned, duration, effort_rating, done, notes)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('user', userid=userid))


@app.route('/user/<userid>')
def user(userid):
    print("At user route")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    # get user info
    cursor.execute("SELECT * FROM Users WHERE UserID = %s", (userid,))
    user_info = cursor.fetchone()

    # get meal logs for this user
    cursor.execute("SELECT * FROM Meals WHERE UserID = %s ORDER BY Timestamp DESC", (userid,))
    meals = cursor.fetchall()

    # get exercise logs for this user
    cursor.execute("SELECT * FROM Exercises WHERE UserID = %s ORDER BY Timestamp DESC", (userid,))
    exercises = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('user.html', uid=userid, user_info=user_info, meals=meals, exercises=exercises)

if __name__ == '__main__':
    app.run(debug=True)