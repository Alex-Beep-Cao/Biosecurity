from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import date

app = Flask(__name__)
hashing = Hashing(app)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'alexbeeproject'

dbconn = None
connection = None


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser,
                                         password=connect.dbpass, host=connect.dbhost,
                                         database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


@app.route('/')
@app.route('/home')
def home():
    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login(): \
        # alex
    # alex1
    # alex2
    # p1 = "alex2"
    # hashed = hashing.hash_value(p1, salt='alex')
    # print(hashed)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = getCursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,))

        hashed = hashing.hash_value('alex', salt='alex')
        print(hashed)
        account = cursor.fetchone()
        print(account)
        if account is not None:
            user_password = account[2]
            if hashing.check_value(user_password, password, salt='alex'):
                # If account exists in accounts table
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['position_type_id'] = account[4]
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'

    return render_template("login.html", msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        repeartpassword = request.form['repeartpassword']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        cursor = getCursor()
        cursor.execute(
            'SELECT * FROM apiarist WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        # elif not len(password) > 8:
        #     msg = 'Password must be at least 8 characters long!'
        # elif not re.search(r'[A-Z]', password):
        #     msg = 'Password must contain at least one uppercase letter!'
        # elif not re.search(r'[a-z]', password):
        #     msg = 'Password must contain at least one lowercase letter!'
        # elif not re.search(r'[0-9]', password):
        #     msg = 'Password must contain at least one digit!'
        # elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        #     msg = 'Password must contain at least one special character!'
        elif repeartpassword != password:
            msg = 'Password not match!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='alex')
            cursor.execute(
                'INSERT INTO apiarist VALUES (NULL, %s, %s, %s,%s, %s,%s ,%s, %s,%s ,%s)', (username, firstname, lastname, hashed, address, email, phone, date.today(), True, 1))

            # Add register infromation into users table
            cursor.execute(
                'SELECT apiarist_id FROM apiarist WHERE username = %s', (username,))
            apiarist_id = cursor.fetchone()
            cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s)',
                           (apiarist_id, username, hashed, email, 1,))

            connection.commit()
            msg = 'You have successfully registered!'

    return render_template("register.html", msg=msg)
