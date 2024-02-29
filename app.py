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
                if account[4] == 1:
                    return redirect(url_for('apiaristdisplay'))
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
                'INSERT INTO apiarist VALUES (NULL, %s, %s, %s,%s, %s,%s ,%s, %s,%s ,%s)', (username, firstname, lastname, password, address, email, phone, date.today(), True, 1))

            # Add register infromation into users table
            cursor.execute(
                'SELECT apiarist_id FROM apiarist WHERE username = %s', (username,))
            apiarist_id = cursor.fetchone()
            cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s)',
                           (apiarist_id[0], username, hashed, email, 1,))

            connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))

    return render_template("register.html", msg=msg)


@app.route('/apiaristdisplay', methods=['GET', 'POST'])
def apiaristdisplay():
    msg = ''
    if request.method == 'POST':
        user_id = session['id']
        cursor = getCursor()
        cursor.execute(
            'SELECT * FROM apiarist WHERE apiarist_id = %s', (user_id,))
        account = cursor.fetchone()

        firstname = request.form['firstname'] if request.form['firstname'] != '' else account[2]
        lastname = request.form['lastname'] if request.form['lastname'] != '' else account[3]
        password = request.form['password'] if request.form['password'] != '' else account[4]
        address = request.form['address'] if request.form['address'] != '' else account[5]
        email = request.form['email'] if request.form['email'] != '' else account[6]
        phone = request.form['phone'] if request.form['phone'] != '' else account[7]

        # If account exists show error and validation checks
        if not account:
            msg = 'Account not exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
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
        else:
            hashed = hashing.hash_value(password, salt='alex')
            cursor.execute(
                'UPDATE apiarist SET first_name = %s, last_name = %s, plain_password = %s, address = %s, email = %s, phone_number = %s WHERE apiarist_id = %s', (firstname, lastname, password, address, email, phone, user_id))
            cursor.execute(
                'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s', (
                    hashed, email, user_id)
            )
            personal_details = [account[1], firstname,
                                lastname, address, email, phone]
            msg = " Updated"

        return render_template("apiaristdisplay.html", personal_details=personal_details, msg=msg)
    else:
        msg = ''
        user_id = session['id']
        position_type_id = session['position_type_id']
        personal_details = ''
        cursor = getCursor()
        if position_type_id == 1:
            cursor.execute(
                'SELECT * FROM apiarist WHERE apiarist_id = %s', (user_id,))
            personal_details = cursor.fetchone()
        else:
            cursor.execute(
                'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
            personal_details = cursor.fetchone()
        connection.commit()
        return render_template("apiaristdisplay.html", personal_details=personal_details msg=msg)


@app.route('/logout')
def logout():
    session.pop('Username', None)
    return redirect(url_for('home'))
