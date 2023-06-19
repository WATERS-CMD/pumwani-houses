class RegisterUser:
  __tablenamae__="users"
  id=db.column(db.integer,primary_key=True,autoincrement=True)
  firstname=db.column(db.string(200), nullable=False ,unique=True)
  lastname=db.column(db.string(200), nullable=False ,unique=True)
  email=db.column(db.string(200), nullable=False ,unique=True)
  house_number=db.column(db.string(200), db.Foreign_key('house_id'))
  phone_contact=db.column(db.string(200), nullable=False, unique=True)
  password=db.column(db.string(200), nullable=False)

  property=db.relationship('property' ,backref="user", lazy=True)


  def __init__(self,id, fisrtname,lastname, password, email, house_number,phone_contact):
    self.id=id
    self.firstname=firstname
    self.lastname=lastname
    self.password=password
    self.email=email
    self.house_number=house_number
    self.phone_contact=phone_contact

 