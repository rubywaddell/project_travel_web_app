"""CRUD operations for data in model.py"""

import model

def create_user(username, fname, lname, email, password):
    """Create a return a new user"""

    user = model.User(username=username, fname=fname, lname=lname, email=email, password=password)

    model.db.session.add(user)
    model.db.session.commit()

    return user



if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)