from main import db
from sqlalchemy.orm import relationship,backref
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
  __tablename__='users'

  id=db.column(db.integer, primary_key=True, autoincrement=True)
  user_name=db.column(db.string(200),nullable=False,unique=True)
  email=db.colum(db.string(100),nullable=False,unique=True)
  phone_contact=db.column(db.string(20),nullable=False,unique=True)
  house_number=db.column(db.string(200), db.Foreign_key('house_id'))
  password=db.column(db.string(60),nullable=False,format=hash)

  def user(self,id,user_name,email,phone_contact,house_number,password):
    self.id=id
    self.email=email
    self.user_name=user_name
    self.phone_contact=phone_contact
    self.house_number=house_number
    self.password=password

    property = db.relationship('property', backref='user', lazy=True)

    def insert(self):
        db.add(self)
        db.commit()

        return self

    @classmethod
    def check_password(cls,email,password):
        record = cls.query.filter_by(email=email).first()

        if record and check_password_hash(record.password, password):
            return True
        else:
            return False

    @classmethod
    def check_email_exists(cls, email):
        record = cls.query.filter_by(email = email).first()

        if record:
            return True
        else:
            return False

    # fetch by email
    @classmethod
    def fetch_by_email(cls,email):
        return cls.query.filter_by(email = email).first()


  