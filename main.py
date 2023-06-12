from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

from connections import DBase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ssebugenyijuma95@localhost/wifi_connections'
db=SQLAlchemy(app)
Dbconnection = None

@app.before_request
def before_request():
    global Dbconnection
    Dbconnection = DBase.Connect()
    if Dbconnection is None:
        # Handle connection failure
        # For example, you can redirect to an error page
        return render_template('error.html')

@app.teardown_request
def teardown_request(exception=None):
    global Dbconnection
    if Dbconnection is not None:
        Dbconnection.close()
        Dbconnection = None

@app.before_first_request
def create_tables():
    db.create_all()
    seeding()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')
            return redirect(url_for('login', next = request.url))
    return wrap



@app.route('/', method=['GET','POST'])
def Register():
    if request.method == 'POST':
        # Perform user sign-up and store the user details in the database
        username = request.form['username']
        user_password = request.form['password']
        
        connection = DBase.Connect()
        cursor = DBase.Cursor(connection)
        query = '''insert into public.users(username,password) values (%s,%s)'''
        try:
            cursor.execute(query,(username,user_password))
            connection.commit()
            flash('Sign up successful. Please log in.')
            return redirect(url_for('login'))
        except psycopg2.Error as e:
            print(e)
    return render_template('register.html')

@app.route('/Home_dashboard')
def dashboard():
    return render_template('Home_dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

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
