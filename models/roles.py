from sqlalchemy.orm import backref
from connections import db

class Role(db.Model):
    __tablename__ = 'roles'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    staff = db.relationship('Staff', backref='roles', lazy=True)