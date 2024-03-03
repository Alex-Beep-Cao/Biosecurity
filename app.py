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


# @app.route('/')
# @app.route('/home')
# def home():
#     hashed = hashing.hash_value('123', salt='alex')
#     print(hashed)
#     return render_template("base.html")

@app.route('/')
@app.route('/home')
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
                # if position_type_id = 1 -> apiarist
                # if position_type_id = 2 -> staff
                # if position_type_id = 3 -> admin

                if account[4] == 1:
                    return redirect(url_for('apiaristdisplay'))
                elif account[4] == 2:
                    return redirect(url_for('staffdisplay'))
                else:
                    return redirect(url_for('admindisplay'))
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
                'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s position_type_id = 1', (
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
        return render_template("apiaristdisplay.html", personal_details=personal_details, msg=msg)

# staff display


@app.route('/staffdisplay', methods=['GET', 'POST'])
def staffdisplay():
    msg = ''
    # Staff update their own information
    if request.method == 'POST':
        user_id = session['id']
        cursor = getCursor()
        cursor.execute(
            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = 2', (user_id,))
        account = cursor.fetchone()

        firstname = request.form['firstname'] if request.form['firstname'] != '' else account[2]
        lastname = request.form['lastname'] if request.form['lastname'] != '' else account[3]
        password = request.form['password'] if request.form['password'] != '' else account[4]
        email = request.form['email'] if request.form['email'] != '' else account[5]
        phone = request.form['phone'] if request.form['phone'] != '' else account[6]
        department = request.form['department'] if request.form['department'] != '' else account[8]

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
                'UPDATE employee SET first_name = %s, last_name = %s, plain_password = %s, email = %s, phone_number = %s , department= %s WHERE employee_id = %s and position_type_id= 2', (firstname, lastname, password, email, phone, department, user_id))
            cursor.execute(
                'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s and position_type_id = 2', (
                    hashed, email, user_id)
            )
            personal_details = [account[1], firstname,
                                lastname, email, phone, department]
            msg = " Updated"

        return render_template("staffdisplay.html", personal_details=personal_details, msg=msg)
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

        cursor.execute(
            'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
        )
        apiarist_detail = cursor.fetchall()

        connection.commit()
        return render_template("staffdisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, msg=msg)

# staff delete apiarist
# @app.route('/staff/delete/<id>', methods=['GET', 'POST'])
# def staffdelete(id):
#     user_id = session['id']
#     position_type_id = session['position_type_id']

#     if id:
#         cursor = getCursor()
#         try:
#             cursor.execute(
#                 'DELETE FROM users WHERE user_id = %s and position_type_id = 1', (id,))
#             try:
#                 cursor.execute(
#                     'DELETE FROM apiarist WHERE apiarist_id = %s', (id,))
#             except:
#                 msg = "Something wrong within the deletion in apiarist Table."
#             msg = "Successfully Deleted."
#         except:
#             msg = "Something wrong within the deletion in User Table."

#         cursor.execute(
#             'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
#         personal_details = cursor.fetchone()

#         cursor.execute(
#             'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
#         )
#         apiarist_detail = cursor.fetchall()

#     return render_template("staffdisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, msg=msg)

# staff udpate apiarist
# @app.route('/staff/update/<id>', methods=['GET', 'POST'])
# def staffupdate(id):
#     user_id = session['id']
#     position_type_id = session['position_type_id']

#     # Staff level update apiarist
#     if id:
#         cursor = getCursor()
#         cursor.execute('SELECT * FROM apiarist WHERE apiarist_id = %s', (id,))
#         account = cursor.fetchone()
#         apiarist_id = account[0]

#         firstname = request.form['firstname-update'] if request.form['firstname-update'] != '' else account[2]
#         lastname = request.form['lastname-update'] if request.form['lastname-update'] != '' else account[3]
#         password = request.form['password-update'] if request.form['password-update'] != '' else account[4]
#         address = request.form['address-update'] if request.form['address-update'] != '' else account[5]
#         email = request.form['email-update'] if request.form['email-update'] != '' else account[6]
#         phone = request.form['phone-update'] if request.form['phone-update'] != '' else account[7]
#         status = request.form['status-update'] if request.form['status-update'] != '' else account[9]

#         # If account exists show error and validation checks
#         if not account:
#             msg = 'Account not exists!'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address!'
#         # elif not len(password) > 8:
#         #     msg = 'Password must be at least 8 characters long!'
#         # elif not re.search(r'[A-Z]', password):
#         #     msg = 'Password must contain at least one uppercase letter!'
#         # elif not re.search(r'[a-z]', password):
#         #     msg = 'Password must contain at least one lowercase letter!'
#         # elif not re.search(r'[0-9]', password):
#         #     msg = 'Password must contain at least one digit!'
#         # elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
#         #     msg = 'Password must contain at least one special character!'
#         elif status not in (0, 1):
#             msg = 'Status must be 0 or 1!'
#         else:
#             hashed = hashing.hash_value(password, salt='alex')
#             try:
#                 cursor.execute(
#                     'UPDATE apiarist SET first_name = %s, last_name = %s, plain_password = %s, address = %s, email = %s, phone_number = %s, employee_status = %s WHERE apiarist_id = %s', (firstname, lastname, password, address, email, phone, status, apiarist_id))
#                 try:
#                     cursor.execute(
#                         'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s position_type_id = 1', (hashed, email, apiarist_id))
#                 except:
#                     msg = " Update User table error!"
#             except:
#                 msg = " Update Apiarist table error!"

#             msg = " Updated"
#             cursor.execute(
#                 'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
#             personal_details = cursor.fetchone()

#             cursor.execute(
#                 'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
#             )
#             apiarist_detail = cursor.fetchall()

#     return render_template("staffdisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, msg=msg)

# staff add apiarist
# @app.route('/staff/add', methods=['GET', 'POST'])
# def staffadd():
#     user_id = session['id']
#     position_type_id = session['position_type_id']
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         username = request.form['username']
#         firstname = request.form['firstname']
#         lastname = request.form['lastname']
#         password = request.form['password']
#         address = request.form['address']
#         email = request.form['email']
#         phone = request.form['phone']
#         status = request.form['status']

#         cursor = getCursor()
#         cursor.execute(
#             'SELECT * FROM apiarist WHERE username = %s', (username,))
#         account = cursor.fetchone()
#         # If account exists show error and validation checks
#         if account:
#             msg = 'Account already exists!'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address!'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers!'
#         # elif not len(password) > 8:
#         #     msg = 'Password must be at least 8 characters long!'
#         # elif not re.search(r'[A-Z]', password):
#         #     msg = 'Password must contain at least one uppercase letter!'
#         # elif not re.search(r'[a-z]', password):
#         #     msg = 'Password must contain at least one lowercase letter!'
#         # elif not re.search(r'[0-9]', password):
#         #     msg = 'Password must contain at least one digit!'
#         # elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
#         #     msg = 'Password must contain at least one special character!'
#         else:
#             # Account doesnt exists and the form data is valid, now insert new account into accounts table
#             hashed = hashing.hash_value(password, salt='alex')
#             try:
#                 cursor.execute(
#                     'INSERT INTO apiarist VALUES (NULL, %s, %s, %s,%s, %s,%s ,%s, %s,%s ,%s)', (username, firstname, lastname, password, address, email, phone, date.today(), status, 1))
#                 try:
#                     cursor.execute(
#                         'SELECT apiarist_id FROM apiarist WHERE username = %s', (username,))
#                     apiarist_id = cursor.fetchone()
#                     cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s)',
#                                    (apiarist_id[0], username, hashed, email, 1,))
#                 except:
#                     msg = 'Error occur duing insert data in Apiarist table!'
#             except:
#                 msg = 'Error occur duing insert data in User table!'

#             msg = 'Apiarist successfully created!'
#             cursor.execute(
#                 'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
#             personal_details = cursor.fetchone()

#             cursor.execute(
#                 'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
#             )
#             apiarist_detail = cursor.fetchall()
#             connection.commit()

#         return render_template("staffdisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, msg=msg)

# admin display


@app.route('/admindisplay', methods=['GET', 'POST'])
def admindisplay():
    msg = ''
    # Admin update their own information
    if request.method == 'POST':
        user_id = session['id']
        cursor = getCursor()
        cursor.execute(
            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = 3', (user_id,))
        account = cursor.fetchone()

        firstname = request.form['firstname'] if request.form['firstname'] != '' else account[2]
        lastname = request.form['lastname'] if request.form['lastname'] != '' else account[3]
        password = request.form['password'] if request.form['password'] != '' else account[4]
        email = request.form['email'] if request.form['email'] != '' else account[5]
        phone = request.form['phone'] if request.form['phone'] != '' else account[6]
        department = request.form['department'] if request.form['department'] != '' else account[8]

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
                'UPDATE employee SET first_name = %s, last_name = %s, plain_password = %s, email = %s, phone_number = %s , department= %s WHERE employee_id = %s and position_type_id= 3', (firstname, lastname, password, email, phone, department, user_id))
            cursor.execute(
                'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s and position_type_id = 3', (
                    hashed, email, user_id)
            )
            personal_details = [account[1], firstname,
                                lastname, email, phone, department]
            msg = " Updated"

        return render_template("staffdisplay.html", personal_details=personal_details, msg=msg)
    else:
        # Admin can see apiarists and staffs
        msg = ''
        user_id = session['id']
        position_type_id = session['position_type_id']
        personal_details = ''
        cursor = getCursor()
        cursor.execute(
            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
        personal_details = cursor.fetchone()

        cursor.execute(
            'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
        )
        apiarist_detail = cursor.fetchall()

        cursor.execute(
            'SELECT employee_id, username, first_name, last_name, plain_password, email, phone_number, hire_date, department, employee_status FROM employee where position_type_id = 2'
        )
        staff_detail = cursor.fetchall()

        connection.commit()
        return render_template("admindisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)

# admin delete apiarist


@app.route('/admin/delete/<id>', methods=['GET', 'POST'])
def admindelete(id):
    user_id = session['id']
    position_type_id = session['position_type_id']

    if id:
        cursor = getCursor()
        try:
            cursor.execute(
                'DELETE FROM users WHERE user_id = %s and position_type_id = 1', (id,))
            try:
                cursor.execute(
                    'DELETE FROM apiarist WHERE apiarist_id = %s', (id,))
            except:
                msg = "Something wrong within the deletion in apiarist Table."
            msg = "Successfully Deleted."
        except:
            msg = "Something wrong within the deletion in User Table."

        cursor.execute(
            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
        personal_details = cursor.fetchone()

        cursor.execute(
            'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
        )
        apiarist_detail = cursor.fetchall()

        cursor.execute(
            'SELECT employee_id, username, first_name, last_name, plain_password, email, phone_number, hire_date, department, employee_status FROM employee where position_type_id = 2'
        )
        staff_detail = cursor.fetchall()

    return render_template("admindisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)

# admin delete staff


@app.route('/admin/delete/staff/<id>', methods=['GET', 'POST'])
def admindeletestaff(id):
    user_id = session['id']
    position_type_id = session['position_type_id']

    if id:
        cursor = getCursor()
        try:
            cursor.execute(
                'DELETE FROM users WHERE user_id = %s and position_type_id = 2', (id,))
            try:
                cursor.execute(
                    'DELETE FROM employee WHERE empolyee_id = %s and position_type_id = 2', (id,))
            except:
                msg = "Something wrong within the deletion in employee Table."
            msg = "Successfully Deleted."
        except:
            msg = "Something wrong within the deletion in User Table."

        cursor.execute(
            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
        personal_details = cursor.fetchone()

        cursor.execute(
            'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
        )
        apiarist_detail = cursor.fetchall()

        cursor.execute(
            'SELECT employee_id, username, first_name, last_name, plain_password, email, phone_number, hire_date, department, employee_status FROM employee where position_type_id = 2'
        )
        staff_detail = cursor.fetchall()

    return render_template("admindisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)

# admin update apiarist


@app.route('/admin/update/<id>', methods=['GET', 'POST'])
def adminupdate(id):
    user_id = session['id']
    position_type_id = session['position_type_id']

    # Admin level update apiarist
    if id:
        cursor = getCursor()
        cursor.execute('SELECT * FROM apiarist WHERE apiarist_id = %s', (id,))
        account = cursor.fetchone()
        apiarist_id = account[0]

        firstname = request.form['firstname-update'] if request.form['firstname-update'] != '' else account[2]
        lastname = request.form['lastname-update'] if request.form['lastname-update'] != '' else account[3]
        password = request.form['password-update'] if request.form['password-update'] != '' else account[4]
        address = request.form['address-update'] if request.form['address-update'] != '' else account[5]
        email = request.form['email-update'] if request.form['email-update'] != '' else account[6]
        phone = request.form['phone-update'] if request.form['phone-update'] != '' else account[7]
        status = request.form['status-update'] if request.form['status-update'] != '' else account[9]

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
        elif status not in (0, 1):
            msg = 'Status must be 0 or 1!'
        else:
            hashed = hashing.hash_value(password, salt='alex')
            try:
                cursor.execute(
                    'UPDATE apiarist SET first_name = %s, last_name = %s, plain_password = %s, address = %s, email = %s, phone_number = %s, employee_status = %s WHERE apiarist_id = %s', (firstname, lastname, password, address, email, phone, status, apiarist_id))
                try:
                    cursor.execute(
                        'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s position_type_id = 1', (hashed, email, apiarist_id))
                except:
                    msg = " Update User table error!"
            except:
                msg = " Update Apiarist table error!"

            msg = " Updated"
            cursor.execute(
                'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
            personal_details = cursor.fetchone()

            cursor.execute(
                'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
            )
            apiarist_detail = cursor.fetchall()

            cursor.execute(
                'SELECT employee_id, username, first_name, last_name, plain_password, email, phone_number, hire_date, department, employee_status FROM employee where position_type_id = 2'
            )
            staff_detail = cursor.fetchall()

    return render_template("staffdisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)

# admin update staff


@app.route('/admin/update/staff/<id>', methods=['GET', 'POST'])
def adminupdatestaff(id):
    user_id = session['id']
    position_type_id = session['position_type_id']

    # Admin level update apiarist
    if id:
        cursor = getCursor()
        cursor.execute('SELECT * FROM apiarist WHERE apiarist_id = %s', (id,))
        account = cursor.fetchone()
        employee_id = account[0]

        firstname = request.form['firstname-update-staff'] if request.form['firstname-update-staff'] != '' else account[2]
        lastname = request.form['lastname-update-staff'] if request.form['lastname-update-staff'] != '' else account[3]
        password = request.form['password-update-staff'] if request.form['password-update-staff'] != '' else account[4]
        email = request.form['email-update-staff'] if request.form['email-update-staff'] != '' else account[5]
        phone = request.form['phone-update-staff'] if request.form['phone-update-staff'] != '' else account[6]
        hiredate = request.form['hiredate-update-staff'] if request.form['hiredate-update-staff'] != '' else account[7]
        department = request.form['department-update-staff'] if request.form['department-update-staff'] != '' else account[8]
        status = request.form['status-update-staff'] if request.form['status-update-staff'] != '' else account[9]

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
        elif status not in (0, 1):
            msg = 'Status must be 0 or 1!'
        else:
            hashed = hashing.hash_value(password, salt='alex')
            try:
                cursor.execute(
                    'UPDATE employee SET first_name = %s, last_name = %s, plain_password = %s, email = %s, phone_number = %s, hire_date = %s, department = %s, employee_status = %s WHERE apiarist_id = %s', (firstname, lastname, password,  email, phone, hiredate, department, status, employee_id))
                try:
                    cursor.execute(
                        'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s position_type_id = 2', (hashed, email, employee_id))
                except:
                    msg = " Update User table error!"
            except:
                msg = " Update Apiarist table error!"

            msg = " Updated"
            cursor.execute(
                'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
            personal_details = cursor.fetchone()

            cursor.execute(
                'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
            )
            apiarist_detail = cursor.fetchall()

            cursor.execute(
                'SELECT employee_id, username, first_name, last_name, plain_password, email, phone_number, hire_date, department, employee_status FROM employee where position_type_id = 2'
            )
            staff_detail = cursor.fetchall()

    return render_template("staffdisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)

# admin add apiarist


@app.route('/admin/add', methods=['GET', 'POST'])
def adminadd():
    user_id = session['id']
    position_type_id = session['position_type_id']
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        status = request.form['status']

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
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='alex')
            try:
                cursor.execute(
                    'INSERT INTO apiarist VALUES (NULL, %s, %s, %s,%s, %s,%s ,%s, %s,%s ,%s)', (username, firstname, lastname, password, address, email, phone, date.today(), status, 1))
                try:
                    cursor.execute(
                        'SELECT apiarist_id FROM apiarist WHERE username = %s', (username,))
                    apiarist_id = cursor.fetchone()
                    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s)',
                                   (apiarist_id[0], username, hashed, email, 1,))
                except:
                    msg = 'Error occur duing insert data in Apiarist table!'
            except:
                msg = 'Error occur duing insert data in User table!'

            msg = 'Apiarist successfully created!'
            cursor.execute(
                'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
            personal_details = cursor.fetchone()

            cursor.execute(
                'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
            )
            apiarist_detail = cursor.fetchall()
            cursor.execute(
                'SELECT employee_id, username, first_name, last_name, plain_password, email, phone_number, hire_date, department, employee_status FROM employee where position_type_id = 2'
            )
            staff_detail = cursor.fetchall()
            connection.commit()
    return render_template("admindisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)


@app.route('/admin/add/staff', methods=['GET', 'POST'])
def adminaddstaff():
    user_id = session['id']
    position_type_id = session['position_type_id']
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username-add-staff']
        firstname = request.form['firstname-add-staff']
        lastname = request.form['lastname-add-staff']
        password = request.form['password-add-staff']
        email = request.form['email-add-staff']
        phone = request.form['phone-add-staff']
        hiredate = request.form['hiredate-add-staff']
        department = request.form['department-add-stafff']
        status = request.form['status-add-staff']

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
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='alex')
            try:
                cursor.execute(
                    'INSERT INTO employee VALUES (NULL, %s, %s, %s,%s, %s,%s ,%s, %s,%s ,%s)', (username, firstname, lastname, password, email, phone, hiredate, department, status, 2))
                try:
                    cursor.execute(
                        'SELECT employee_id FROM employee WHERE username = %s', (username,))
                    employee_id = cursor.fetchone()
                    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s)',
                                   (employee_id[0], username, hashed, email, 2,))
                except:
                    msg = 'Error occur duing insert data in Employee table!'
            except:
                msg = 'Error occur duing insert data in User table!'

            msg = 'Employee successfully created!'
            cursor.execute(
                'SELECT * FROM employee WHERE employee_id = %s and position_type_id = %s', (user_id, position_type_id,))
            personal_details = cursor.fetchone()

            cursor.execute(
                'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
            )
            apiarist_detail = cursor.fetchall()
            cursor.execute(
                'SELECT employee_id, username, first_name, last_name, plain_password, email, phone_number, hire_date, department, employee_status FROM employee where position_type_id = 2'
            )
            staff_detail = cursor.fetchall()
            connection.commit()
    return render_template("admindisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)


@app.route('/logout')
def logout():
    session.pop('Username', None)
    session.pop('loggedin', False)
    session.pop('id', None)
    session.pop('position_type_id', None)

    return redirect(url_for('login'))
