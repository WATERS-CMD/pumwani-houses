from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from functools import wraps
import psycopg2
import datetime
from connections import conn,cur

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

class Payments(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey('user.id'))
    amount = db.Column(db.Float())
    transaction_ref = db.Column(db.String(139))
    date = db.Column(db.DateTime())

    user = db.relationship("Users", backref="payments")
    __tablename__='Payments'
    def save_payment(self):
        newPayment = Payment(id=self.id,user_id=self.user_id,amount=self.amount,date=self.date,transaction_ref=self.transaction_ref
        )
        try:
            db.session.add(newPayment)
            db.session.commit()
        except Exception as e:
                print (e)
                raise ValueError ("Error occured while saving the data to database.")
        finally:
                    pass
def get_all_payments(cls):
                    payments = cls.query.order_by('-id').all()
                    return jsonify([i.__dict__ for i in payments])
                    #return "success"
                    #print("Success")
                    #return jsonify({"message":"Successfully saved"})
                    #return jsonify({'data': newPayment})




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

@app.route('/paynow', methods=['POST'])
def process_payment():
    data = request.get_json()
            
            # Extract the transaction details from the request
    firstname=request.form["firstname"]
    lastname=request.form["lastname"]
    transaction_id = data.get('transaction_id')
    amount = data.get('amount')
    date=datetime.now()
            
            # Generate a payment request to Safaricom's API
    safaricom_response = make_payment_request(transaction_id, amount)
        
    if safaricom_response.status_code == 200:
                # Store the payment details in the database
            cur.execute("INSERT INTO payments VALUES (?, ?,?,?,?)", (firstname,lastname,transaction_id, amount,date))
            conn.commit()
                
                # Return a success response
            return 'Payment processed successfully'
    else:
                # Handle payment failure
                return 'Payment failed'
def make_payment_request(transaction_id, amount):
        # Make a request to Safaricom's payment API
    url = 'https://safaricom-payment-api-url'  # Replace with the actual API URL
    headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Replace with your access token
            }
    payload = {
                'firstname':firstname,
                'lastname':lastname,
                'transaction_id': transaction_id,
                'amount': amount,
                'paybill_number': '888880',
                'date':date
                # Include any additional required parameters
            }
            
    response = requests.post(url, json=payload, headers=headers)
    return response    

@app.errorhandler(403)
def forbidden(e):
    flash("You don't have permission for that", "danger")
    



@app.route('/receipt')
def receipt():
    return render_template('receipt.html')


@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/property')
def property():
    return render_template('property.html')


@app.route('/role')
@login_required
def dashboards():
    if role_id==1:
        return redirect("/admin_dashboard")
    elif role_id==2:
        return redirect("/dashboard")
    else:
        abort(403)
        flash("wrong credentials! Try again")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
