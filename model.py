"""Data models for travel safety app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """An app user, stores their personal information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(15), unique=True)
    full_name = db.Column(db.String(25))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(15))

    def __repr__(self):
        return f"<User object: user_id={self.user_id}, username={self.username}, full_name={self.full_name}>"
    