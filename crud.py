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

def get_vacation_by_user_id(user_id):
    """Get and return all vacation objects associated iwth a given user_id numbers"""

    user_vacations = model.Vacation.query.filter(model.Vacation.user_id == user_id).all()
    return user_vacations


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

def join_vacation_w_vacation_label():
    """Join the vacation and vacation_label tables, return the BaseQuery for further querying in other functions"""

    vacation_vacation_label_join = model.db.session.query(model.VacationLabel).join(model.VacationLabel.vacation)
    
    return vacation_vacation_label_join

#State CRUD functions:
def create_state(state_name, city_id):
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

def get_state_by_id(state_id):
    """Query and return the first state with a given id number"""

    state = model.State.query.filter(model.State.state_id == state_id).first()

    return state

def get_state_by_city_id(city_id):
    """Query and return the first state tied to a given city id number"""

    state = model.db.session.query(model.State).filter(model.State.city_id == city_id)
    return state

def get_state_by_city(city_name):
    """Query and return the state tied to a given city name"""

    city = get_city_by_name(city_name=city_name)

    state = model.db.session.query(model.State).filter(model.State.city_id == city.city_id)

    return state

def check_if_state_in_db(state_name):
    """Checks if the given state name is already stored in the database, returns True or False"""

    state = get_state_by_name(state_name=state_name)
    if state == None:
        return False
    else:
        return True

def check_if_state_has_city(state_name, city_name):
    """Checks if a given city is already in the database and connected to the given state, returns a boolean"""

    # state = get_state_by_name(state_name=state_name)

    city_state_join = model.db.session.query(model.City).join(model.City.state)
    state_filter = city_state_join.filter(model.State.state_name == state_name)
    cities = state_filter.all()

    city_names = []

    for city in cities:
        city_names.append(city.city_name)

    if city_name in city_names:
        return True
    else:
        return False


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

def get_city_by_state(state_name):
    """Query and return the cities tied to a given state id number"""

    state = get_state_by_name(state_name=state_name)

    city_state_join = model.db.session.query(model.City).join(model.City.state)
    state_filter = city_state_join.filter(model.State.state_name == state_name)
    cities = state_filter.all()

    return cities

def check_if_city_in_db(city_name):
    """Checks if the given city name is already stored in the database, returns True or False"""

    city = get_city_by_name(city_name=city_name)
    if city == None:
        return False
    else:
        return True

def check_if_city_state_in_db_create_if_not(city, state):
    """Checks if a given state and city are already stored in the database
        If they are not, they will be created"""

    check_city = check_if_city_in_db(city_name=city)
    # check_state = check_if_state_in_db(state_name=state)

    if check_city == False:
        new_city = create_city(city_name=city)
        new_state = create_state(state_name=state, city_id=new_city.city_id)
        return new_city, new_state
        
        # if check_state == False:
        #     new_state = create_state(state_name=state, city_id=new_city.city_id)
        #     return new_city, new_state
        
        # db_state = get_state_by_name(state_name=state)
        # return new_city, db_state

    else:
        db_city = get_city_by_name(city_name=city)
        db_state = get_state_by_city_id(city_id=db_city.city_id)

        # if check_city == False:
        #     new_state = create_state(state_name=state, city_id=db_city.city_id)
        #     return db_city, new_state

        # db_state = get_state_by_name(state_name=state)
        return db_city, db_state


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

def show_tag_states():
    """Return a list of all tag_states in the database"""

    return model.db.session.query(model.Tag.tag_state).all()

def show_tag_cities():
    """Return a list of all tag_cities in the database"""

    return model.db.session.query(model.Tag.tag_city).all()

def get_tags_by_tag_state(state):
    """Return a list of all tags with a given tag_state"""

    state_tags = model.Tag.query.filter(model.Tag.tag_state == state).all()
    return state_tags

def get_tags_by_tag_city(city):
    """Return a list of all tags with a given tag_city"""

    city_tags = model.Tag.query.filter(model.Tag.tag_city == city).all()
    return city_tags


if __name__ == "__main__":
    from server import app, session
    model.connect_to_db(app)
    model.db.create_all()