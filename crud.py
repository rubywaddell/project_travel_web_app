"""CRUD operations for data in model.py"""

# from os import stat
import model

#User CRUD functions:
# def create_user(username, fname, lname, email, password, vacation_id=None):
def create_user(username, fname, lname, email, password):
    """Create a return a new user"""

    user = model.User(username=username, fname=fname, lname=lname, email=email, 
            password=password)

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

def get_user_by_username(username):
    """Return the first user with a give username"""

    user = model.User.query.filter(model.User.username == username).first()
    return user

def add_new_vacation_to_user(user_id, vacation_id):
    """Adds a new vacation to an existing user profile"""

    user = get_user_by_id(user_id=user_id)
    new_user = create_user(username=user.username, fname=user.fname, lname=user.lname, email=user.email,
                password=user.password, vacation_id=vacation_id)

    return new_user

#Vacation CRUD functions:
def create_vacation(vacation_label_id, user_id):
    """Create and return a vacation object"""

    vacation = model.Vacation(vacation_label_id=vacation_label_id, user_id=user_id)

    model.db.session.add(vacation)
    model.db.session.commit()

    return vacation

def show_vacations():
    """Return a list of all vacation objects in the database"""

    vacations = model.Vacation.query.all()
    return vacations

def get_vacation_by_id(vacation_id):
    """Get and return the first vacation object with a given id number"""

    vacation = model.Vacation.query.filter(model.Vacation.vacation_id == vacation_id).first()
    return vacation

#VacationLabel CRUD Functions:
def create_vacation_label(departure_date, arrival_date, state_id=None):
    """Create and return a vacation_label object"""

    vacation_label = model.VacationLabel(departure_date=departure_date, arrival_date=arrival_date, state_id=state_id)

    model.db.session.add(vacation_label)
    model.db.session.commit()

    return vacation_label

def show_vacation_labels():
    """Return a list of all vacation_labels in the database"""

    return model.VacationLabel.query.all()

def get_vacation_label_by_id(vacation_label_id):
    """Query and return the first vacation_label object with a given id number"""

    vacation_label = model.VacationLabel.query.filter(model.VacationLabel.vacation_label_id == vacation_label_id).first()
    return vacation_label

#State CRUD functions:
def create_state(state_name, city_id=None):
    """Create a new state, add to database, and return it"""

    new_state = model.State(state_name=state_name, city_id=city_id)

    model.db.session.add(new_state)
    model.db.session.commit()
    
    return new_state

def show_states():
    """"Return a list of all states in database"""

    return model.State.query.all()

def get_state_by_name(state_name):
    """Query and return the first state with a given name"""

    state = model.State.query.filter(model.State.state_name == state_name).first()
    return state


#City CRUD functions
def create_city(city_name):
    """Create a new city, add to database, and return it"""

    new_city = model.City(city_name=city_name)

    model.db.session.add(new_city)
    model.db.session.commit()
    
    return new_city

def show_cities():
    """"Return a list of all cities in database"""

    return model.City.query.all()

def get_city_by_name(city_name):
    """Query and return the first city with a given name"""

    city = model.City.query.filter(model.City.city_name == city_name).first()
    return city


#Tip CRUD functions
def create_tip(tip_text, user_id=None):
    """Create a new tip, add to database, and return it"""

    new_tip = model.Tip(tip_text=tip_text, user_id=user_id)

    model.db.session.add(new_tip)
    model.db.session.commit()
    
    return new_tip

def show_tips():
    """"Return a list of all tips in database"""

    return model.Tip.query.all()

#TipTag CRUD functions:
def create_tip_tag(tag_id, tip_id):
    """Create a new tip_tag, add it to the database, and return it"""

    new_tip_tag = model.TipTag(tag_id=tag_id, tip_id=tip_id)

    model.db.session.add(new_tip_tag)
    model.db.session.commit()

    return new_tip_tag

def show_tip_tags():
    """Return a list of all tip_tags"""

    return model.TipTag.query.all()

#Tag CRUD functions
def create_tag(tag_name, tag_state, tag_city):
    """Create a new tag, add it to the database, and return it"""

    new_tag = model.Tag(tag_name=tag_name, tag_state=tag_state, tag_city=tag_city)

    model.db.session.add(new_tag)
    model.db.session.commit()

    return new_tag

def show_tags():
    """REturn a list of all tag objects in the database"""

    return model.Tag.query.all()


if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)
    model.db.create_all()