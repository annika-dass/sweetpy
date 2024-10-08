from flask import Flask, render_template, request, redirect, url_for, session, json
from waitress import serve
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'rcia_mic'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bleattodeath'
app.config['MYSQL_DB'] = 'rcialogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:8000/rcialogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/rcialogin/', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg=''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()        
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'        
    # Output message if something goes wrong...
    return render_template('index.html', msg=msg)

# http://localhost:8000/rciapython/logout - this will be the logout page
@app.route('/rcialogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:8000/rcialogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/rcialogin/register', methods=['GET', 'POST'])
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
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
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
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:8000/rcialogin/home - this will be the home page, only accessible for logged in users
@app.route('/rcialogin/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        user = session['username'].capitalize()
        # User is loggedin show them the home page
        return render_template('home.html', msg='Welcome back ' + user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:8000/rcialogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/rcialogin/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))

# http://localhost:8000/rcialogin/enroll - this will be the home page, only accessible for logged in users
@app.route('/rcialogin/enroll', methods=['GET', 'POST'])
def enroll():
    # Save user name and Id from session values
    user = session['username'].capitalize()
    userid = session['id']
    # Output message if something goes wrong...
    msg = user + '! please fill in the RCIA enrollment form, and click enroll.'
    # Check if the user is logged in
    if 'loggedin' in session:
        if request.method == 'GET':
            # User is loggedin show them the home page
            return render_template('enroll.html', msg=msg)
        if request.method == 'POST':
            # Create variables for easy access
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            birthdate = request.form['birthdate']
            maritalstatus = request.form['maritalstatus']
            mothername = request.form['mothername']
            motherreligion = request.form['motherreligion']
            fathername = request.form['fathername']
            fatherreligion = request.form['fatherreligion']
            religiousbg = request.form['religiousbg']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Insert new RCIA enrollment into the enroll table
            cursor.execute('INSERT INTO enroll VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (userid, firstname, lastname, birthdate, maritalstatus, mothername, motherreligion, fathername, fatherreligion, religiousbg))
            mysql.connection.commit()
            return render_template('home.html', msg='Congratulations! you have successfully enrolled!')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)