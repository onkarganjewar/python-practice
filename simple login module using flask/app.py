# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session

# create the application object
app = Flask(__name__)


# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string


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
    if request.method == 'POST':
        if (request.form['username'] != 'admin' or
                request.form['password'] != 'admin'):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['loggedIn'] = True
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


# route for handling the login page logic
@app.route('/logout')
def logout():
    session.pop('loggedIn', None)
    return redirect(url_for('login'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
