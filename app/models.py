from datetime import datetime
from app import db, login# mdb
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #not only does this give us User.ratings, but also
    #this adds a Ratings.reviewer expression that will return the reviewe given a rating
    ratings = db.relationship('Ratings', backref='reviewer', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ratings(db.Model):
    Rating_id = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Film_id = db.Column(db.Integer)
    Score_given = db.Column(db.Integer)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

