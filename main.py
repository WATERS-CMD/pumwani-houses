from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
import os
from connections import Dbase

app=Flask(__name__)
#db=SQLALCHEMY(app)
Dbconnection=None
connection=Dbase.connection(Dbconnection)
cursor=Dbase.cursor(connection)

#from models.admin import admin
#from models.user import user


@app.route('/')
def Register():
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




if __name__=='__main__':
  app.run(debug=True,host=('0.0.0.0'))