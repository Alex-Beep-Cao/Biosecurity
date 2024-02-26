from flask import render_template
from flask import Flask
from flask import request
import mysql.connector
import connect

app = Flask(__name__)


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
def home():
    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")
