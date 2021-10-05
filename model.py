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


def connect_to_db(flask_app, db_uri="postgresql:///travel_project", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)