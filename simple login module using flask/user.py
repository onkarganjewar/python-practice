# circular dependency
# from dbTest import dbConnect
from werkzeug.security import generate_password_hash, check_password_hash

# db = dbConnect()


class User(object):
    firstName = ""
    email = ""
    # primary_key AUTO_INCREMENT
    # id = None
    password = ""
    lastName = ""

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        # store the password hash instead in plain text
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def verify_password_hash(passHash, password):
        return check_password_hash(passHash, password)

    def __repr__(self):
        return '<User %r %r %r %r>' % (self.email,
                                       self.firstName,
                                       self.lastName, self.password)


'''
    def get_id(self):
        return str(self.id)
'''
