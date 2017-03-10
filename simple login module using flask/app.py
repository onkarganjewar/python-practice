# import the Flask class from the flask module
from flask import (Flask, render_template, redirect, flash,
                   url_for, request, session)
from dbTest import dbConnect
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# create the application object
app = Flask(__name__)
db = dbConnect()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(250))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


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
    if request.method == 'POST':
        if (request.form['username'] != 'admin' or
                request.form['password'] != 'admin'):
            error = 'Invalid Credentials. Please try again.'
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
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'],
                request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
