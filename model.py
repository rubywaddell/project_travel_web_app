"""Data models for travel safety app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """An app user, stores their personal information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(15), unique=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(15))

    travel_id = db.Column(db.Integer, db.ForeignKey("travels.travel_id"))

    travel = db.relationship("Travel", backref="travels")

    def __repr__(self):
        return f"<User object: user_id={self.user_id}, username={self.username}, full_name={self.fname} {self.lname}>"


class Travel(db.Model):
    """A user's travel information, related to the User table"""

    __tablename__ = "travels"

    travel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    departure_date = db.Column(db.Date, nullable=True)
    arrival_date = db.Column(db.Date, nullable=True)
    #travel_id = Foreign Key in Users table

    state_id = db.Column(db.Integer, db.ForeignKey("states.state_id"))

    state = db.relationship("State", backref="states")

    def __repr__(self):
        return f"<Travels object: travel_id={self.travel_id}>"

class State(db.Model):
    """A US state, related to the Travel table"""

    __tablename__ = "states"

    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_name = db.Column(db.String)
    #state_id used as a foreign key in the travels table

    def __repr__(self):
        return f"<State object: state_id={self.state_id} state_name={self.state_name}"


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