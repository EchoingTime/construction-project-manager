from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'April152004#'
app.config['MYSQL_DB'] = 'test'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM MyGuests WHERE usrname = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['usrname'] = account['usrname']
            # Redirect to home page

            #profile()
            return redirect(url_for("profiles"))
            #return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


# http://localhost:5000/Falsk/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM MyGuests WHERE usrname = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO MyGuests (usrname, password, email) VALUES ( %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
@app.route('/profiles')
def profiles():
    #with assitance from Git Copilot
    if 'loggedin' in session: 
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * FROM MyGuests where id=%s', (session['id'],))
        account=cursor.fetchone()
        return render_template("profiles.html", account=account)
    return redirect(url_for('login'))

@app.route('/inbox')
def inbox():
    user_id = session['id']
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""select messages.id, messages.message_text, messages.time, myguests.usrname as sender_name from messages join myguests on messages.sender_id=myguests.id where messages.receiver_id=%s order by messages.time desc""", (user_id,))
    messages=cursor.fetchall()
    cursor.close()
    print(messages)
    return render_template("inbox.html", messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
        sender_id=session['id']
        receiver_name=request.form['receiver_username']
        content=request.form['content']
        cursor=mysql.connection.cursor()
        cursor.execute('select id from myguests where usrname=%s', (receiver_name,))
        receiver=cursor.fetchone()
        if receiver:
            receiver_id=receiver[0]    
            cursor.execute('insert into messages (sender_id, receiver_id, message_text) values (%s, %s, %s)', (sender_id, receiver_id, content))
            flash("message send")
            mysql.connection.commit()
        else:
            flash("User not found!","error")

        cursor.close()
        return redirect(url_for('inbox'))






if __name__ == '__main__':
    app.run()