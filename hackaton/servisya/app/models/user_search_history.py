from app.extensions import db
from datetime import datetime

class UserSearchHistory(db.Model):
    __tablename__ = 'user_search_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_term = db.Column(db.String(255), nullable=False)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='search_history')
