from . import db 
from flask_login import UserMixin


class Deliverable (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(500), nullable=False)
    duedate = db.Column(db.String(150), nullable=True)
    category = db.Column(db.String(150), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    deliverable = db.relationship('Deliverable')

