from flask import Flask, redirect, render_template, request, session
import sqlite3
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "shahzaibofficial"
app.permanent_session_lifetime = timedelta(days=30)

Genders = ["Male","Female","Custom"]

@app.route("/")
def index():
    if "userName" not in session or "password" not in session:
        return redirect("/login")
    userName = session["userName"]
    password = session["password"]

    #SQLite3 Queries starts
    connection = sqlite3.connect("./Databases/database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT userName,fullName,gender FROM users WHERE userName = ? AND password = ?",(userName,password))
    verify = cursor.fetchone()
    connection.commit()
    connection.close()
    #SQLite3 Queries ended
    if verify:
        return render_template("index.html",fullName=verify[1])
    else:
        return redirect("/login")

@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        userName = request.form.get("userName")
        password = request.form.get("password")

        #SQLite3 Queries starts
        connection = sqlite3.connect("./Databases/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT userName,fullName,gender FROM users WHERE userName = ? AND password = ?",(userName,password))
        verify = cursor.fetchone()
        connection.commit()
        connection.close()
        #SQLite3 Queries ended
        if verify:
            session["userName"] = userName
            session["password"] = password
            return redirect('/')
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html",genders = Genders)

@app.route('/logout')
def logout():
    session["userName"] = None
    session["password"] = None
    return redirect('/login')

@app.route('/recorded',methods = ["POST"])
def record():
    userName = request.form.get("userName")
    name = request.form.get("name")
    gender = request.form.get("gender")
    password = request.form.get("password")
    #SQLite3 Queries starts
    connection = sqlite3.connect("./Databases/database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT userName FROM users WHERE userName = ?",(userName,))
    userNameVerify = cursor.fetchall()
    connection.commit()
    connection.close()
    #SQLite3 Queries ended

    if gender not in Genders or not userName or not name or not password:
        return render_template("signup.html",genders=Genders,failure = "Some Error Occurs")
    if len(password) < 8:
        return render_template("signup.html",genders = Genders,passwordIssue = "This Password is not enough!")
    if userNameVerify:
        return render_template("signup.html",genders = Genders,userNameIssue = "This name is already Taken!")
    #SQLite3 Queries starts
    connection = sqlite3.connect("./Databases/database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?,?,?,?)",(userName,name,gender,password))
    connection.commit()
    connection.close()
    #SQLite3 Queries ended
    return redirect('/login')

@app.route('/records')
def records():
    #SQLite3 Queries starts
    connection = sqlite3.connect("./Databases/database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT userName,fullName,gender FROM users")
    usersData = cursor.fetchall()
    connection.commit()
    connection.close()
    #SQLite3 Queries ended
    return render_template("records.html",usersData = usersData)

if __name__ == "__main__":
    app.run(debug=True)