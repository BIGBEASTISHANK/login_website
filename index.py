from flask import Flask, render_template, redirect, request, session, url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "321121123"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] ="@Pranjal12"
app.config["MYSQL_DB"] = "login"

db = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            global username, password
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM logininfo WHERE email=%s AND password=%s", (username, password))
            info = cursor.fetchone()
            print(info)
            if info is not None:
                if info['email'] == username and info['password'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        if "name" in request.form and "email" in request.form and "password" in request.form:
            
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO login.logininfo (name, email, password) VALUES (%s, %s, %s);",(name, email, password))
            db.connection.commit()
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile')
def profile():
    if session['loginsuccess'] == True:
        return render_template('profile.html', email = username, password = password)
    else:
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    session['loginsuccess'] = False
    return redirect(url_for('index'))

app.run(debug=True)