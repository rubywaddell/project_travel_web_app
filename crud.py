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


if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)