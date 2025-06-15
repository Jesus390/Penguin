from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # user, admin, professional

    # professional_profile = db.relationship('Professional', backref='user', uselist=False)


    # Relación uno a uno
    professional_profile = db.relationship('Professional', back_populates='user', uselist=False)

    search_history = db.relationship('UserSearchHistory', back_populates='user', cascade='all, delete-orphan')

    service_requests = db.relationship('ServiceRequest', back_populates='user', cascade='all, delete-orphan')


