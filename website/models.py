import flask_login
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    logs = db.relationship('Userlog')


class manlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(10))
    header = db.Column(db.String(1000))
    message = db.Column(db.String(10000))

class Userlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    error_num = db.Column(db.Integer)
    operator = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_equipment_broken = db.Column(db.String(10))
    equipment = db.Column(db.String(1000))
    circumstances = db.Column(db.String(5000))
    actions = db.Column(db.String(5000))
    prevent = db.Column(db.String(5000))
