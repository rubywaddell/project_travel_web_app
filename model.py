"""Models for travel safety app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """An app user, stores their personal information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(15), unique=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(15))

    vacation = db.relationship("Vacation", back_populates="user")

    tip = db.relationship("Tip", back_populates="user")

    def __repr__(self):
        return f"<User Object: user_id={self.user_id} username={self.username}>"
    
class Vacation(db.Model):
    """A user's vacation information"""

    __tablename__ = "vacations"

    vacation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    vacation_label_id = db.Column(db.Integer, db.ForeignKey("vacation_labels.vacation_label_id"))
    vacation_label = db.relationship("VacationLabel", back_populates="vacation")

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    user = db.relationship("User", back_populates="vacation")

    def __repr__(self):
        return f"<Vacation Object: vacation_id={self.vacation_id}>"


class VacationLabel(db.Model):
    """Tags to classify and query through vacation objects"""

    __tablename__ = "vacation_labels"

    vacation_label_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    departure_date = db.Column(db.Date, nullable=True)
    arrival_date = db.Column(db.Date, nullable=True)

    state_id = db.Column(db.Integer, db.ForeignKey("states.state_id"))
    state = db.relationship("State", back_populates="vacation_label")

    vacation = db.relationship("Vacation", back_populates="vacation_label")

    def __repr__(self):
        return f"<VacationLabel object: vacation_label_id={self.vacation_label_id} departure_date={self.departure_date}>"

class State(db.Model):
    """State object to tag vacations with location data"""

    __tablename__ = "states"

    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_name = db.Column(db.String)

    # city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"))
    city = db.relationship("City", back_populates="state")

    vacation_label = db.relationship("VacationLabel", back_populates="state")

    def __repr__(self):
        return f"<State Object: state_id= {self.state_id} state_name= {self.state_name}>"

class City(db.Model):
    """City object, connected to States via one to many relationship"""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String)

    state_id = db.Column(db.Integer, db.ForeignKey("states.state_id"))
    state = db.relationship("State", back_populates="city")

    def __repr__(self):
        return f"<City Object: city_id={self.city_id}, city_name={self.city_name}>"

class Tip(db.Model):
    """Tip object, connected to the User, so users can generate travel tips"""

    __tablename__ = "tips"

    tip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tip_text = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", back_populates="tip")

    tip_tag = db.relationship("TipTag", back_populates="tip")

    def __repr__(self):
        return f"<Tip Object: tip_id= {self.tip_id}>"

class TipTag(db.Model):
    """Tags to classify and query through tip objects"""

    __tablename__ = "tip_tags"

    tip_tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    tip_id = db.Column(db.Integer, db.ForeignKey("tips.tip_id"))
    tip = db.relationship("Tip", back_populates="tip_tag")

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"))
    tag = db.relationship("Tag", back_populates="tip_tag")

    def __repr__(self):
        return f"<TipTag Object: tip_tag_id= {self.tip_tag_id}>"

class Tag(db.Model):
    """Tags to store tagged data for tips"""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag_name = db.Column(db.String)
    tag_state = db.Column(db.String)
    tag_city = db.Column(db.String)

    tip_tag = db.relationship("TipTag", back_populates="tag")

    def __repr__(self):
        return f"<Tag Object: tag_id= {self.tag_id} tag_name= {self.tag_name}>"


def connect_to_db(flask_app, db_uri="postgresql:///travel_app", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)