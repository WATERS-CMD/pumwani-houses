from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/pumwani'
db = SQLAlchemy(app)
app.secret_key='qw123eyfknvnfhf356457nkfvfjhfnfyre78777'
connection = None
cursor = None

# Define the Users model for SQLAlchemy
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    housenumber = db.Column(db.String(10), nullable=False, unique=True)
    telephone = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, firstname, lastname, housenumber, telephone, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.housenumber = housenumber
        self.telephone = telephone
        self.email = email
        self.password = password


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')
            return redirect(url_for('login', next=request.url))

    return wrap


@app.route('/')
def Register():
    return render_template('register.html')


@app.route('/register', methods=['POST','GET'])
def register():
    global connection, cursor

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    housenumber = request.form['housenumber']
    telephone = request.form['telephone']
    email = request.form['email']
    userpassword = request.form['password']

    try:
        connection = psycopg2.connect(host='localhost', database='pumwani', user='postgres', password='12345')
        cursor = connection.cursor()

        query = '''INSERT INTO users(firstname, lastname, housenumber, telephone, email, password)
                   VALUES (%s, %s, %s, %s, %s, %s)'''

        cursor.execute(query, (firstname, lastname, housenumber, telephone, email, userpassword))
        connection.commit()

        flash('Sign up successful. Please log in.')
        return redirect(url_for('login'))
    except psycopg2.Error as e:
        flash('An error occurred. Please try again.')
        print(e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

    return render_template('register.html')





@app.route('/login',methods=['POST','GET'])
def login():
    # Handle login form submission
    if request.method == 'POST':
        firstname = request.form.get('firstname'+'')
        lastname = request.form.get('lastname'+'')
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(firstname=firstname, lastname=lastname, email=email, password=password).first()

        if user:
            flash('Login successful. Welcome! Enjoy your stay at Pumwani')
            return redirect('/dashboard')
        elif admin:
            flash('Welcome Administrator!')
            return redirect('/admindashboard.html')
        else:
            flash('Login failed. Please check your credentials and try again.')
            return redirect('/login.html')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard.html')
def dashboard_html():
    return redirect('/dashboard')


@app.route('/payments')
def payments():
    return render_template('payments.html')


@app.route('/receipt')
def receipt():
    return render_template('receipt.html')


@app.route('/transactions')
def transactions():
    return render_template('transactions.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/adminsignup')
def adminsignup():
    return render_template('adminsignup.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
