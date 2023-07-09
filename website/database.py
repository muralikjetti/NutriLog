from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Date


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=func.date(func.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbohydrates = db.Column(db.Float)
    fats = db.Column(db.Float)
    foods = db.relationship('Food', backref='user', lazy=True)