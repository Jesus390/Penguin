from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Professional(UserMixin, db.Model):
    __tablename__ = 'professionals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    location = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # Relación reversa (opcional, si lo necesitas desde User)
    user = db.relationship('User', back_populates='professional_profile')

    received_requests = db.relationship('ServiceRequest', back_populates='professional', cascade='all, delete-orphan')
