from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'YouWontPass',
    'host': 'localhost',
    'port' : '3306',
    'database': 'health_tracker'
}
app.secret_key = 'secretKey'

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
        
@app.route('/user_sign',  methods=['GET','POST'])
def user_sign():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        userid = request.form['user_id']
              
        conn = mysql.connector.connect(**config)
        cursed = conn.cursor()
        params = ()
        query = ""
        used_email = False
        used_uid = False
        if email != '':

        #find a user with that specific email address
            params = (email,)
            query = "SELECT UserID, Fname, Privilege FROM users WHERE Email = %s"
            used_email = True
        elif userid != '':
            params = (int(userid),)
            query = "SELECT UserID, Fname, Privilege FROM users WHERE UserID = %s"
            used_uid = True
        else:
            flash("No user ID or Email provided")
            return render_template('user_sign.html')
            
        cursed.execute(query, params)
        #get results
        results = cursed.fetchall()
        cursed.close()
        conn.close()
        if len(results) == 0:
            print("User not found")
            if used_email:
                flash("Incorrect Email")
            if used_uid:
                flash("Incorrect User ID")
        else:
            uid, fname, user_privilege = results[0]

            if user_privilege == 'a':
                return redirect(url_for('admin',userid=uid))
            
            return redirect(url_for('user',userid = uid))
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
    
    mycursor.execute("INSERT INTO users (Fname, Lname, Email, Birthdate, Height, Weight, Privilege)"
    "VALUES (%s,%s,%s,%s,%s,%s,%s)",insert_params)
    #check that the addition was successful
    conn.commit()
    #get user ID
    uid = mycursor.lastrowid
    print("User created. ID: ", uid)
    mycursor.close()
    conn.close()
    return redirect(url_for('user',userid = uid)) #placeholder for now, redirects to user page



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

@app.route('/admin/<userid>')
def admin(userid):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    # get user info
    cursor.execute("SELECT * FROM Users WHERE UserID = %s", (userid,))
    user_info = cursor.fetchone()
    user_privilege = user_info["Privilege"]
    # get meal logs for this user
    cursor.execute("SELECT * FROM Meals WHERE UserID = %s ORDER BY Timestamp DESC", (userid,))
    meals = cursor.fetchall()
    # get exercise logs for this user
    cursor.execute("SELECT * FROM Exercises WHERE UserID = %s ORDER BY Timestamp DESC", (userid,))
    exercises = cursor.fetchall()
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users")
    num_users = cursor.fetchone() #get the total number of users
    cursor.close()
    conn.close()
    return render_template('user_admin.html', uid=userid, user_info=user_info, meals=meals, 
                           exercises=exercises, usercnt = num_users,
                           user_search_result = None,
                           searched_uid = None)


@app.route('/get_user', methods=['POST'])
def get_user():
    target_uid = request.form['uid']
    admin_uid = request.form['admin_uid']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Users WHERE UserID = %s", (admin_uid,))
    user_info = cursor.fetchone()

    cursor.execute("SELECT * FROM Meals WHERE UserID = %s ORDER BY Timestamp DESC", (admin_uid,))
    meals = cursor.fetchall()

    cursor.execute("SELECT * FROM Exercises WHERE UserID = %s ORDER BY Timestamp DESC", (admin_uid,))
    exercises = cursor.fetchall()

    cursor.execute("SELECT * FROM Users WHERE UserID = %s", (target_uid,))
    search_result = cursor.fetchone()
    cursor.close()
    conn.close()
    newconn = mysql.connector.connect(**config)
    newcursor = newconn.cursor()
    newcursor.execute("SELECT COUNT(*) FROM Users")
    num_users = newcursor.fetchone()
    newcursor.close()
    newconn.close()

    return render_template('user_admin.html',
                           uid=admin_uid,
                           user_info=user_info,
                           meals=meals,
                           exercises=exercises,
                           usercnt=num_users,
                           user_search_result=search_result,
                           searched_uid=target_uid)


@app.route('/user/<userid>')
def user(userid):
    print("At user route")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    # get user info
    cursor.execute("SELECT * FROM Users WHERE UserID = %s", (userid,))
    user_info = cursor.fetchone()
    user_privilege = user_info["Privilege"]

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