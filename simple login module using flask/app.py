# In python 2.7
from __future__ import print_function
import sys
# import the Flask class from the flask module
# from flask.ext.login import LoginManager
from flask import (Flask, render_template, redirect, flash,
                   url_for, request, session, make_response)
# from flask_login import (login_required, login_user)
import dbTest
from datetime import datetime
from functools import wraps, update_wrapper
from user import User

# create the application object
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60
app.config["CACHE_TYPE"] = "null"

db = dbTest.dbConnect()


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, \
        must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


'''
@app.teardown_request
def teardown_request(exception):
    if exception:
        print(exception)
    g.db.close()
'''


'''
@app.before_request
def before_request():
    print(session.keys(), session.values())
    print("before request")
    print('username' in session, "in session?")
    g.db = dbTest.dbConnect()
    g.user = None
    if "username" in session:
        g.user = get_user(session['username'])
'''

'''
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, \
                                  post-check=0, pre-check=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "-1"
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers['Cache-Control'] = 'public, max-age=0'
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    return r
'''


# use decorators to link the function to a url
@app.route('/')
def home():
    # return "Hello, World!"  # return a string
    return render_template('home.html')


@app.route('/index')
# @login_required
@nocache
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
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
            # return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', error=error)


# route for handling the logout page logic
@app.route('/logout')
def logout():
    print("SESSION GETTING POPPED", file=sys.stderr)
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('loggedIn', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    customUser = User(request.form['firstName'], request.form['lastName'],
                      request.form['email'], request.form['password'])

    dbTest.dbInsert(db, customUser)
    # login_user(customUser)
    # db.session.add(user)
    # db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = 'login'
    app.run(debug=True)
