from main import db
import psycopg2
import psycopg2.extras

class Admin(db.Model):
  __tablename__=''