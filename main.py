from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from functools import wraps
import psycopg2
import datetime
from connections import conn, cur
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/pumwani'
app.secret_key = 'qw123eyfknvnfhf356457nkfvfjhfnfyre78777'
db = SQLAlchemy(app)

hostname='localhost'
database='pumwani'
user='postgres'
password='12345'
port_id=5432


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    housenumber = db.Column(db.String(10), nullable=False, unique=True)
    telephone = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    role = db.relationship("Roles", primaryjoin="Users.role_id == Roles.id", backref="users")

    def __init__(self, firstname, lastname, housenumber, telephone, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.housenumber = housenumber
        self.telephone = telephone
        self.email = email
        self.password = password


class Payments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    amount = db.Column(db.Float())
    transaction_ref = db.Column(db.String(139))
    date = db.Column(db.DateTime())

    user = db.relationship("Users", primaryjoin="Payments.user_id == Users.id", backref="payments")

    __tablename__ = 'Payments'

    def save_payment(self):
        newPayment = Payments(id=self.id, user_id=self.user_id, amount=self.amount, date=self.date,
                              transaction_ref=self.transaction_ref)
        try:
            db.session.add(newPayment)
            db.session.commit()
        except Exception as e:
            print(e)
            raise ValueError("Error occurred while saving the data to the database.")
        finally:
            pass


class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(10))

    __tablename__ = 'roles'

    def save_role(self):
        self.save()
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            raise ValueError('Error occurred while adding role')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')
            return redirect(url_for('login'))

    return wrap

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/addperson', methods=['POST', 'GET'])
def addperson():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    housenumber = request.form['housenumber']
    telephone = request.form['telephone']
    email = request.form['email']
    userpassword = request.form['password']

    new_user = Users(firstname=firstname, lastname=lastname, housenumber=housenumber,
                     telephone=telephone, email=email, password=userpassword)
    try:
        db.session.add(new_user)
        db.session.commit()

        flash('Sign up successful. Please log in.')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred. Please try again.')
        print(e)

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    # Handle login form submission
    if request.method == 'POST':
        firstname = request.form.get('firstname', '')
        lastname = request.form.get('lastname', '')
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(firstname=firstname, lastname=lastname, email=email, password=password).first()

        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            flash('Login successful. Welcome! Enjoy your stay at Pumwani')
            return redirect('/dashboard')
        else:
            flash('Login failed. Please check your credentials and try again.')
            return redirect('/login')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/receipt')
def receipt():
    return render_template('receipt.html')


@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    car_type = db.Column(db.String(50))
    car_model = db.Column(db.String(50))
    car_plate = db.Column(db.String(20))
    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs:
            setattr(self, key, kwargs[key])

        __tablename__ = 'properties'

    def save_property(self):
        self.save()
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            raise ValueError('Error occurred while adding property')

@app.route('/property')
def property():
    conn = psycopg2.connect(host=hostname, database=database, user=user, password=password)
    cur=conn.cursor()
    cur.execute('SELECT * FROM property')
    data=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('property.html',data=data)     
# Route to handle the form submission
@app.route('/addproperty', methods=['POST'])
def add_property():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    car_type = request.form['car_type']
    car_model = request.form['car_model']
    car_plate = request.form['car_plate']

    # Create a new Property object
    new_property = Property(firstname=firstname, lastname=lastname, car_type=car_type,car_model=car_model, car_plate=car_plate)

    # Add the new property to the database
    db.session.add(new_property)
    db.session.commit()

    return redirect('/property')


@app.route('/dashboard.html')
def dashboard_html():
    return redirect('/dashboard')


@app.route('/admin')
@login_required
def loginAdmin():
    user_id = session.get('user_id')
    if user_id == 1:
        return render_template('admin_dashboard.html')
    else:
        return redirect('/dashboard')


@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    user_id = session.get('user_id')
    if user_id == 1:
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            housenumber = request.form['housenumber']
            telephone = request.form['telephone']
            email = request.form['email']
            password = request.form['password']

            new_user = Users(firstname=firstname, lastname=lastname, housenumber=housenumber,
                             telephone=telephone, email=email, password=password)
            try:
                db.session.add(new_user)
                db.session.commit()

                flash('User added successfully.')
                return redirect('/admin')
            except Exception as e:
                flash('An error occurred while adding the user.')
                print(e)

        return render_template('add_user.html')
    else:
        flash('Unauthorized! Only the super admin can add users.')
        return redirect('/admin')

@app.route('/payments')
def payments():

    return render_template('payments.html')

@app.route('/paynow', methods=['POST'])
def process_payment():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    transaction_id = request.form.get('transaction_id')
    amount = request.form.get('amount')
    date = datetime.now()

    # Generate a payment request to Safaricom's API
    safaricom_response = make_payment_request(firstname, lastname, transaction_id, amount, date)

    if safaricom_response.status_code == 200:
        # Store the payment details in the database
        cur.execute("INSERT INTO payments VALUES (?, ?, ?, ?, ?)", (firstname, lastname, transaction_id, amount, date))
        conn.commit()
       

        # Return a success response
        return 'Payment processed successfully'
    else:
        # Handle payment failure
        return 'Payment failed'

def make_payment_request(firstname, lastname, transaction_id, amount, date):
    url = 'https://safaricom-payment-api-url'  # Replace with the actual API URL
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Replace with your access token
    }
    payload = {
        'firstname': firstname,
        'lastname': lastname,
        'transaction_id': transaction_id,
        'amount': amount,
        'paybill_number': '888880',
        'date': date
        # Include any additional required parameters
    }

    response = requests.post(url, json=payload, headers=headers)
    return response
@app.route('/delete', methods=['POST'])
def delete():
   # Get the index of the item to delete from the request
   index = int(request.form['index'])

   # Delete the item from the database using the index or any other identifier
   # Connect to the database
   conn = psycopg2.connect(host=hostname, database=database, user=user, password=password)
   cursor = conn.cursor()

   # Execute the delete statement
   cursor.execute('DELETE FROM your_table WHERE id=?', (index,))  # Replace 'id' with your identifier column

   # Commit the changes
   conn.commit()

   # Close the database connection
   conn.close()

   # Return a response indicating the deletion was successful (optional)
   return 'Item deleted successfully'

@app.errorhandler(403)
def forbidden(e):
    flash("You don't have permission for that", "danger")

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
