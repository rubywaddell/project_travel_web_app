"""CRUD operations for data in model.py"""

import model

def create_user(username, fname, lname, email, password):
    """Create a return a new user"""

    user = model.User(username=username, fname=fname, lname=lname, email=email, password=password)

    model.db.session.add(user)
    model.db.session.commit()

    return user


def create_travel(departure_date, arrival_date):
    """Create and return a new travel object"""

    travel = model.Travel(departure_date=departure_date, arrival_date=arrival_date)

    model.db.session.add(travel)
    model.db.session.commit()

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


if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)