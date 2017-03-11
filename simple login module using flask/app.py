# In python 2.7
from __future__ import print_function
import sys
# import the Flask class from the flask module
from flask import (Flask, render_template, redirect, flash,
                   url_for, request, session)
import dbTest
from user import User

# create the application object
app = Flask(__name__)

db = dbTest.dbConnect()


# use decorators to link the function to a url
@app.route('/')
def home():
    # return "Hello, World!"  # return a string
    return render_template('home.html')


@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
#        return 'Logged in as ' + username + '<br>' + \
#            "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
        "click here to log in</b></a>"


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render welcome template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    passHash = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = dbTest.dbFetchOne(db, username)
        # Check whether the query returned w/ any record
        if ((result is not None) and (result != "")):
            passHash = User.verify_password_hash(result["password"], password)
            print("RESULT IS {}".format(passHash), file=sys.stderr)

            ''' Alternate way of doing the user authentication w/ check_password()
            print("RETURNED RESULT IS {}".format(result), file=sys.stderr)
            customUser = User(result["FirstName"],
                              result["LastName"], username, password)
            print(customUser, file=sys.stderr)
            # True or False
            print("RESULT IS {}".
                  format(customUser.check_password(password)),
                  file=sys.stderr)
            '''
        # If the query returned with empty(0) rows
        if (result is None or result == ""):
            error = "User not found! Please try again."
        # Password hash returned empty or null
        elif ((passHash is None) or (passHash == "")):
            # print("PASSHASH IS ==> {}".format(passHash), file=sys.stderr)
            error = 'Oops... Something went wrong! Please try again.'
        # Password verification unsuccessful
        elif (passHash is False):
            error = 'Invalid Credentials. Please try again.'
        # Password verified successfully
        else:
            session['loggedIn'] = True
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


# route for handling the logout page logic
@app.route('/logout')
def logout():
    session.pop('loggedIn', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    customUser = User(request.form['firstName'], request.form['lastName'],
                      request.form['email'], request.form['password'])

    dbTest.dbInsert(db, customUser)
    # db.session.add(user)
    # db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
