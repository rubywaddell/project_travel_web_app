"""CRUD operations for data in model.py"""

import model

def create_user(username, fname, lname, email, password):
    """Create a return a new user"""

    user = model.User(username=username, fname=fname, lname=lname, email=email, password=password)

    model.db.session.add(user)
    model.db.session.commit()

    return user

def show_users():
    """Return a list of all users"""

    return model.User.query.all()

def get_user_by_id(user_id):
    """Return the first user with a given id number"""

    user = model.User.query.filter(model.User.user_id == user_id).first()
    return user

def get_user_by_email(email):
    """Return the first user with a given email"""

    user = model.User.query.filter(model.User.email == email).first()
    return user

def get_user_by_fname(fname):
    """Return the first user with a given first name"""

    user = model.User.query.filter(model.User.fname == fname).first()
    return user

def create_travel(departure_date, arrival_date):
    """Create and return a new travel object"""

    travel = model.Travel(departure_date=departure_date, arrival_date=arrival_date)

    model.db.session.add(travel)
    model.db.session.commit()

    return travel

def show_travels():
    """Return a list of all travel objects"""

    return model.Travel.query.all()

def get_travel_by_departure_date(departure_date):
    """Return the first travel object with the given departure date"""

    travel = model.Travel.query.filter(model.Travel.departure_date == departure_date).first()
    return travel

def create_user_with_travel_id(username, fname, lname, email, password, travel_id):
    """Create and return a new user object that has relationship with travel table"""

    user = model.User(username=username, fname=fname, lname=lname, email=email, password=password, travel_id=travel_id)

    model.db.session.add(user)
    model.db.session.commit()

    return user


def create_state(state_name):
    """Create and return a new state object"""

    state = model.State(state_name=state_name)

    model.db.session.add(state)
    model.db.session.commit()

    return state


def create_city(city_name, state_id=None):
    """Create and return a new city object"""

    city = model.City(city_name=city_name, state_id=state_id)

    model.db.session.add(city)
    model.db.session.commit()

    return city


def create_tip(tip_text):
    """Create and return a new tip object"""

    tip = model.Tip(tip_text=tip_text)

    model.db.session.add(tip)
    model.db.session.commit()

    return tip


def create_tip_tag():
    """Create and return a new tip_tag object"""

    tip_tag = model.TipTag()

    model.db.session.add(tip_tag)
    model.db.session.commit()

    return tip_tag


def create_tag(tag_name):
    """Create and return a new tag object"""

    tag = model.Tag(tag_name=tag_name)

    model.db.session.add(tag)
    model.db.session.commit()

    return tag



if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)