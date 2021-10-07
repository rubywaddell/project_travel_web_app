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
    travel = db.relationship("Travel", back_populates="user")

    tip = db.relationship("Tip", back_populates="user")

    def __repr__(self):
        return f"<User object: user_id={self.user_id}, username={self.username}, full_name={self.fname} {self.lname}>"


class Travel(db.Model):
    """A user's travel information, related to the User table"""

    __tablename__ = "travels"

    travel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    departure_date = db.Column(db.Date, nullable=True)
    arrival_date = db.Column(db.Date, nullable=True)

    state_id = db.Column(db.Integer, db.ForeignKey("states.state_id"))
    state = db.relationship("State", back_populates="travel")

    user = db.relationship("User", back_populates="travel")

    def __repr__(self):
        return f"<Travels object: travel_id={self.travel_id}>"

class State(db.Model):
    """A US state, related to the Travel table"""

    __tablename__ = "states"

    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_name = db.Column(db.String)

    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"))
    city = db.relationship("City", back_populates="state")

    tip_tag_id = db.Column(db.Integer, db.ForeignKey("tip_tags.tip_tag_id"))
    tip_tag = db.relationship("TipTag", back_populates="state")
 
    travel = db.relationship("Travel", back_populates="state")

    def __repr__(self):
        return f"<State object: state_id={self.state_id} state_name={self.state_name}"


class City(db.Model):
    """Table to store cities and their corresponding states"""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String)

    state = db.relationship("State", back_populates="city")

    def __repr__(self):
        return f"<Cities object: city_id={self.city_id} city_name={self.city_name}>"


class Tip(db.Model):
    """User generated tips about safety while travelling"""

    __tablename__ = "tips"

    tip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tip_text = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", back_populates="tip")

    tip_tag = db.relationship("TipTag", back_populates="tip")

    def __repr__(self):
        return f"<Tip object: tip_id={self.tip_id}>"


class TipTag(db.Model):
    """Association table between Tips and Tags tables"""

    __tablename__ = "tip_tags"

    tip_tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    tip_id = db.Column(db.Integer, db.ForeignKey("tips.tip_id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"))

    tip = db.relationship("Tip", back_populates="tip_tag")
    tag = db.relationship("Tag", back_populates="tip_tag")

    state = db.relationship("State", back_populates="tip_tag")

    def __repr__(self):
        return f"<TipTags object: tip_tags_id={self.tip_tag_id}>"


class Tag(db.Model):
    """Tags to help filter safety tips"""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(25))

    tip_tag = db.relationship("TipTag", back_populates="tag")

    def __repr__(self):
        return f"<Tags object: tag_id={self.tag_id} tag_name={self.tag_name}"


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