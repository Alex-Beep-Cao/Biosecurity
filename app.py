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
import base64

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
@app.route('/login', methods=['GET', 'POST'])
def login():
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
        elif not len(password) > 8:
            msg = 'Password must be at least 8 characters long!'
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
        elif not re.search(r'[0-9]', password):
            msg = 'Password must contain at least one digit!'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
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
        elif not len(password) > 8:
            msg = 'Password must be at least 8 characters long!'
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
        elif not re.search(r'[0-9]', password):
            msg = 'Password must contain at least one digit!'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
        else:
            hashed = hashing.hash_value(password, salt='alex')
            cursor.execute(
                'UPDATE apiarist SET first_name = %s, last_name = %s, plain_password = %s, address = %s, email = %s, phone_number = %s WHERE apiarist_id = %s', (firstname, lastname, password, address, email, phone, user_id))
            cursor.execute(
                'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s and position_type_id = 1', (
                    hashed, email, user_id)
            )

            msg = " Updated successfully !"

        cursor.execute(
            'SELECT * FROM apiarist WHERE apiarist_id = %s', (user_id,))
        personal_details = cursor.fetchone()

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

        firstname = request.form['firstname_u'] if request.form['firstname_u'] != '' else account[2]
        lastname = request.form['lastname_u'] if request.form['lastname_u'] != '' else account[3]
        password = request.form['password_u'] if request.form['password_u'] != '' else account[4]
        email = request.form['email_u'] if request.form['email_u'] != '' else account[5]
        phone = request.form['phone_u'] if request.form['phone_u'] != '' else account[6]
        department = request.form['department_u'] if request.form['department_u'] != '' else account[8]

        # If account exists show error and validation checks
        if not account:
            msg = 'Account not exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not len(password) > 8:
            msg = 'Password must be at least 8 characters long!'
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
        elif not re.search(r'[0-9]', password):
            msg = 'Password must contain at least one digit!'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
        else:
            hashed = hashing.hash_value(password, salt='alex')

            cursor.execute(
                'UPDATE employee SET first_name = %s, last_name = %s, plain_password = %s, email = %s, phone_number = %s , department= %s WHERE employee_id = %s and position_type_id= 2', (firstname, lastname, password, email, phone, department, user_id))
            cursor.execute(
                'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s and position_type_id = 2', (
                    hashed, email, user_id)
            )

            msg = 'You have successfully updated your details!'

        cursor.execute(
            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = 2', (user_id,))

        personal_details = cursor.fetchone()

        cursor.execute(
            'SELECT apiarist_id, username, first_name, last_name, plain_password,address, email, phone_number, date_joined, employee_status FROM apiarist'
        )
        apiarist_detail = cursor.fetchall()

        return render_template("staffdisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, msg=msg)
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

        firstname = request.form['firstname_u'] if request.form['firstname_u'] != '' else account[2]
        lastname = request.form['lastname_u'] if request.form['lastname_u'] != '' else account[3]
        password = request.form['password_u'] if request.form['password_u'] != '' else account[4]
        email = request.form['email_u'] if request.form['email_u'] != '' else account[5]
        phone = request.form['phone_u'] if request.form['phone_u'] != '' else account[6]
        department = request.form['department_u'] if request.form['department_u'] != '' else account[8]

        # If account exists show error and validation checks
        if not account:
            msg = 'Account not exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not len(password) > 8:
            msg = 'Password must be at least 8 characters long!'
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
        elif not re.search(r'[0-9]', password):
            msg = 'Password must contain at least one digit!'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
        else:
            hashed = hashing.hash_value(password, salt='alex')

            cursor.execute(
                'UPDATE employee SET first_name = %s, last_name = %s, plain_password = %s, email = %s, phone_number = %s , department= %s WHERE employee_id = %s and position_type_id= 3', (firstname, lastname, password, email, phone, department, user_id))
            cursor.execute(
                'UPDATE users SET hashed_password= %s, email=%s WHERE user_id = %s and position_type_id = 3', (
                    hashed, email, user_id)
            )
            msg = " Updated"

        cursor.execute(
            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = 3', (user_id,))

        personal_details = cursor.fetchone()

        cursor.execute(
            'SELECT * FROM employee WHERE  position_type_id = 2')

        staff_detail = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM apiarist'
        )
        apiarist_detail = cursor.fetchall()

        return render_template("admindisplay.html", personal_details=personal_details,  apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)
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
                    'DELETE FROM employee WHERE employee_id = %s and position_type_id = 2', (id,))
                msg = "Successfully Deleted."
            except:
                msg = "Something wrong within the deletion in employee Table."

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
        elif not len(password) > 8:
            msg = 'Password must be at least 8 characters long!'
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
        elif not re.search(r'[0-9]', password):
            msg = 'Password must contain at least one digit!'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
        elif int(status) != 0 and int(status) != 1:
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

    return render_template("admindisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)

# admin update staff


@app.route('/admin/update/staff/<id>', methods=['GET', 'POST'])
def adminupdatestaff(id):
    user_id = session['id']
    position_type_id = session['position_type_id']

    if id:
        cursor = getCursor()
        cursor.execute(

            'SELECT * FROM employee WHERE employee_id = %s and position_type_id = 2', (id,))
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
        elif int(status) != 0 and int(status) != 1:
            msg = 'Status must be 0 or 1!'
        else:
            hashed = hashing.hash_value(password, salt='alex')
            try:
                cursor.execute(
                    'UPDATE employee SET first_name = %s, last_name = %s, plain_password = %s, email = %s, phone_number = %s, hire_date = %s, department = %s, employee_status = %s WHERE employee_id = %s', (firstname, lastname, password,  email, phone, hiredate, department, status, employee_id))
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

    return render_template("admindisplay.html", personal_details=personal_details, apiarist_detail=apiarist_detail, staff_detail=staff_detail, msg=msg)

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
        elif not len(password) > 8:
            msg = 'Password must be at least 8 characters long!'
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
        elif not re.search(r'[0-9]', password):
            msg = 'Password must contain at least one digit!'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
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
    if request.method == 'POST':
        username = request.form['username-add-staff']
        firstname = request.form['firstname-add-staff']
        lastname = request.form['lastname-add-staff']
        password = request.form['password-add-staff']
        email = request.form['email-add-staff']
        phone = request.form['phone-add-staff']
        hiredate = request.form['hiredate-add-staff']
        department = request.form['department-add-staff']
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
        elif not len(password) > 8:
            msg = 'Password must be at least 8 characters long!'
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
        elif not re.search(r'[0-9]', password):
            msg = 'Password must contain at least one digit!'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
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


@app.route('/guide', methods=['GET', 'POST'])
@app.route('/guide/<photoId>', methods=['GET', 'POST'])
def viewguide(photoId=None):

    position_type_id = session['position_type_id']

    cursor = getCursor()

    bees = []
    processedImages = []

    msg = ''

    if request.method == 'POST':
        beetype = request.form['beetype']
        present = request.form['present']
        if present == 1:
            presentvalue = True
        else:
            presentvalue = False
        commonname = request.form['commonname']
        scientificname = request.form['scientificname']
        keycharacteristics = request.form['keycharacteristics']
        biology = request.form['biology']
        symptoms = request.form['symptoms']
        file = request.files['image']

        if file:
            image_data = file.read()
            try:
                cursor.execute(
                    'INSERT INTO image VALUES (NULL, %s, True)', (image_data,))

                cursor.execute(
                    'SELECT max(image_id) FROM image where primary_image = true')

                image_id = cursor.fetchone()
                try:
                    cursor.execute(
                        'INSERT INTO bee VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (beetype, presentvalue, commonname, scientificname, keycharacteristics, biology, symptoms, image_id[0]))

                    msg = "Bee added successfully!"
                except:
                    msg = 'Error duirng bee table.'
            except:
                msg = 'Error duirng image table.'

        cursor.execute('SELECT * FROM bee')
        bees = cursor.fetchall()
        cursor.execute('SELECT * FROM image where primary_image = true')
        images = cursor.fetchall()
        for image in images:
            image_data_base64 = base64.b64encode(image[1]).decode('utf-8')
            processedImages.append([image[0], image_data_base64])

        return render_template("guide.html",  bees=bees, processedImages=processedImages, position_type_id=position_type_id, msg=msg)

    else:
        cursor.execute('SELECT * FROM bee')
        bees = cursor.fetchall()
        cursor.execute('SELECT * FROM image where primary_image = true')
        images = cursor.fetchall()
        for image in images:
            image_data_base64 = base64.b64encode(image[1]).decode('utf-8')
            processedImages.append([image[0], image_data_base64])

        return render_template("guide.html",  bees=bees, processedImages=processedImages, position_type_id=position_type_id)

# if request.form['firstname-update-staff'] != '' else account[2]


@ app.route('/update/bee/<id>', methods=['POST'])
def updatebee(id=None):
    cursor = getCursor()
    position_type_id = session['position_type_id']
    processedImages = []

    if id != None and request.method == 'POST':
        cursor.execute('SELECT * FROM bee WHERE bee_id = %s', (id,))
        bee = list(cursor.fetchone())

        cursor.execute(
            'SELECT * FROM image where primary_image = true and image_id = %s', (bee[8],))
        images = list(cursor.fetchone())

        beetype = request.form['beetype-update'] if request.form['beetype-update'] != '' else bee[1]
        present = request.form['present-update'] if request.form['present-update'] != '' else bee[2]
        if present == 1:
            presentvalue = True
        else:
            presentvalue = False
        commonname = request.form['commonname-update'] if request.form['commonname-update'] != '' else bee[3]
        scientificname = request.form['scientificname-update'] if request.form['scientificname-update'] != '' else bee[4]
        keycharacteristics = request.form['keycharacteristics-update'] if request.form['keycharacteristics-update'] != '' else bee[5]
        biology = request.form['biology-update'] if request.form['biology-update'] != '' else bee[6]
        symptoms = request.form['symptoms-update'] if request.form['symptoms-update'] != '' else bee[7]
        try:
            cursor.execute(
                'UPDATE bee SET item_type_id = %s, present_in_NZ= %s, common_name= %s, scientific_name= %s, key_characteristics = %s,biology = %s,symptoms= %s, image_id = %s WHERE bee_id = %s',
                (beetype, presentvalue, commonname, scientificname, keycharacteristics, biology, symptoms, images[0], bee[0],))
            msg = 'Table bee and image updated successfully!'
        except:
            msg = " Error occure Updating bee table!"

    cursor.execute('SELECT * FROM bee')
    bees = cursor.fetchall()
    cursor.execute('SELECT * FROM image where primary_image = true')
    images = cursor.fetchall()
    for image in images:
        image_data_base64 = base64.b64encode(image[1]).decode('utf-8')
        processedImages.append([image[0], image_data_base64])

    return render_template("guide.html",  bees=bees, processedImages=processedImages, position_type_id=position_type_id, msg=msg)


@ app.route('/delete/bee/<id>', methods=['POST'])
def deletebee(id=None):
    position_type_id = session['position_type_id']
    processedImages = []
    if id != None and request.method == 'POST':
        cursor = getCursor()
        cursor.execute('SELECT image_id FROM bee WHERE bee_id = %s', (id,))
        imageid = cursor.fetchone()
        try:
            cursor.execute(
                'DELETE FROM image WHERE image_id = %s', (imageid[0],))
            msg = "Successfully Deleted."
        except:
            msg = "Something wrong within the deletion in Image Table."

    cursor.execute('SELECT * FROM bee')
    bees = cursor.fetchall()
    cursor.execute('SELECT * FROM image where primary_image = true')
    images = cursor.fetchall()
    for image in images:
        image_data_base64 = base64.b64encode(image[1]).decode('utf-8')
        processedImages.append([image[0], image_data_base64])

    return render_template("guide.html",  bees=bees, processedImages=processedImages, position_type_id=position_type_id, msg=msg)


@ app.route('/logout')
def logout():
    session.pop('Username', None)
    session.pop('loggedin', False)
    session.pop('id', None)
    session.pop('position_type_id', None)

    return redirect(url_for('login'))
