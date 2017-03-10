import pymysql

'''
class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)

    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
'''


def dbConnect():
    # db = pymysql.connect(host='10.0.0.140', user='root', passwd='password')
    db = pymysql.connect(host='127.0.0.1', user='root')
    cursor = db.cursor()
    query = ("SHOW DATABASES")
    cursor.execute(query)
    # Print the list of databases in mysql localhost
    for r in cursor:
        print(r)
    return db


# Insert to the database
def dbInsert(db):
    try:
        with db.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db.commit()

        with db.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        db.close()


connection = dbConnect()
dbInsert(connection)
