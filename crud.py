"""CRUD operations for data in model.py"""

# from os import stat
import model
import requests
from datetime import datetime

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~User CRUD functions:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

def get_user_by_vacation_id(vacation_id):
    """Return the first user with the given vacation_id"""

    user_vacation_join = model.User.query.join(model.User.vacation)
    user = user_vacation_join.filter(model.Vacation.vacation_id == vacation_id).first()
    return user

def change_user_email(new_email, old_email):
    """Updates user's email address and returns the user"""

    user = get_user_by_email(old_email)
    user.email = new_email
    model.db.session.commit()
    return user

def change_user_username(old_username, new_username):
    """Updates user's username and returns the user"""

    user = get_user_by_username(old_username)
    user.username = new_username
    model.db.session.commit()
    return user

def change_user_password(user_id, new_password):
    """Updates user's password and returns the user"""

    user = get_user_by_id(user_id)
    user.password = new_password
    model.db.session.commit()
    return user

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vacation CRUD functions:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

def get_vacation_by_vacation_label_id(vacation_label_id):
    """Queries and returns the first vacation object with the given vacation_label_id"""

    vacation_vacation_label_join = model.db.session.query(model.Vacation).join(model.Vacation.vacation_label)
    return vacation_vacation_label_join.filter(model.VacationLabel.vacation_label_id == vacation_label_id).first()

def get_vacation_by_vacation_label(vacation_label):
    """Queries and returns the first vacation object tied to the given vacation_label"""

    vacation_vacation_label_join = model.db.session.query(model.Vacation).join(model.Vacation.vacation_label)
    return vacation_vacation_label_join.filter(model.VacationLabel.vacation_label_id == vacation_label.vacation_label_id).first()

def delete_vacation(vacation):
    """Deletes the given vacation and its vacation_label from the database"""

    vacation_label = get_vacation_label_by_vacation(vacation)
    model.db.session.delete(vacation_label)
    model.db.session.delete(vacation)
    model.db.session.commit()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~VacationLabel CRUD Functions:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

def get_vacation_label_by_vacation(vacation):
    """Query and returns the first vacation_label object with the given vacation relation"""

    vacation_label = model.db.session.query(model.VacationLabel).join(model.VacationLabel.vacation).filter(
        model.Vacation.vacation_id == vacation.vacation_id).first()
    
    return vacation_label

def change_arrival_and_departure_dates(vacation_label_id, new_departure_date, new_arrival_date):
    """Updates the departure and arrival dates and returns the vacation_label"""
    
    vacation_label = model.db.session.query(model.VacationLabel).get(vacation_label_id)
    vacation_label.departure_date = new_departure_date
    vacation_label.arrival_date = new_arrival_date
    model.db.session.commit()
    return vacation_label

def change_vacation_label_location(vacation_label_id, new_state, new_city):
    """Updates the state and city for given vacation_label_id and returns the vacation_label"""

    vacation_label = model.db.session.query(model.VacationLabel).get(vacation_label_id)
    vacation_label.state.state_name = new_state
    vacation_label.state.city.city_name = new_city
    model.db.session.commit()
    return vacation_label

def make_vacation_label_dict(vacation_labels):
    """Iterates through a list of vacations and returns a dictionary that is jsonifiable"""

    vacation_label_dict = {}
    for i, vacation_label in enumerate(vacation_labels):
        departure_month = vacation_label.departure_date.month
        departure_day = vacation_label.departure_date.day
        departure_year = vacation_label.departure_date.year
        arrival_month = vacation_label.arrival_date.month
        arrival_day = vacation_label.arrival_date.day
        arrival_year = vacation_label.arrival_date.year

        vacation_label_dict[i] = {
            "departure_month" : departure_month,
            "departure_day" : departure_day,
            "departure_year" : departure_year,
            "arrival_month" : arrival_month,
            "arrival_day" : arrival_day,
            "arrival_year" : arrival_year,
            "state_name" : vacation_label.state.state_name,
            "city_name" : vacation_label.state.city.city_name
        }

    return vacation_label_dict

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~State CRUD functions:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

    state = model.db.session.query(model.State).filter(model.State.city_id == city_id).first()
    return state

def get_state_by_city(city_name):
    """Query and return the state tied to a given city name"""

    city = get_city_by_name(city_name=city_name)

    state = model.db.session.query(model.State).filter(model.State.city_id == city.city_id).first()

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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~City CRUD functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

    if check_city == False:
        new_city = create_city(city_name=city)
        new_state = create_state(state_name=state, city_id=new_city.city_id)
        return new_city, new_state

    else:
        db_city = get_city_by_name(city_name=city)
        db_state = get_state_by_city_id(city_id=db_city.city_id)

        return db_city, db_state


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Tip CRUD functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_tip(tip_text, user_id=None):
    """Create a new tip, add to database, and return it"""

    new_tip = model.Tip(tip_text=tip_text, user_id=user_id)

    model.db.session.add(new_tip)
    model.db.session.commit()
    
    return new_tip

def show_tips():
    """"Return a list of all tips in database"""

    return model.Tip.query.all()

def show_tips_with_user_id(user_id):
    """Return a list of all tips with the given user_id"""

    return model.db.session.query(model.Tip).filter(model.Tip.user_id == user_id).all()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TipTag CRUD functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_tip_tag(tag_id, tip_id):
    """Create a new tip_tag, add it to the database, and return it"""

    new_tip_tag = model.TipTag(tag_id=tag_id, tip_id=tip_id)

    model.db.session.add(new_tip_tag)
    model.db.session.commit()

    return new_tip_tag

def show_tip_tags():
    """Return a list of all tip_tags"""

    return model.TipTag.query.all()

def order_tip_tags_by_tip_tag_id_desc():
    """Returns a list of all tip_tags in descending order"""

    return model.db.session.query(model.TipTag).order_by(model.db.desc(model.TipTag.tip_tag_id)).all()

def order_tip_tags_by_tip_id():
    """Returns a list of all tip_tags ordered by tip_id"""

    return model.db.session.query(model.TipTag).order_by(model.TipTag.tip_id).all()

def order_tip_tags_by_tag_id():
    """Returns a list of all tip_tags ordered by tag_id"""

    return model.db.session.query(model.TipTag).order_by(model.TipTag.tag_id).all()

def order_tip_tags_by_user_id():
    """Returns a list of all tip_tags ordered by the user_id stored in tips"""

    tip_tag_join_tips = model.db.session.query(model.TipTag).join(model.TipTag.tip)
    return tip_tag_join_tips.order_by(model.Tip.user_id).all()

def get_paginated_tip_tags():
    """Returns a pagination of all tip_tags in the database"""

    # tip_tag_base_query = model.db.session.query(model.TipTag)
    tip_tag_base_query = model.db.session.query(model.TipTag).order_by(model.db.desc(model.TipTag.tip_tag_id))
    return tip_tag_base_query.paginate(per_page=10)

def get_paginated_tag_filtered_tip_tags(filter_tag):
    """Returns a pagination object of all tip_tags filtered by the given tag name"""

    tip_tag_join_tags = model.db.session.query(model.TipTag).join(model.TipTag.tag)
    join_filter = tip_tag_join_tags.filter(model.Tag.tag_name == filter_tag)

    return join_filter.paginate(per_page=10)

def get_paginated_state_filtered_tip_tags(state):
    """Returns a pagination object of all tip_tags filtered by the given state"""

    tip_tag_join_tags = model.db.session.query(model.TipTag).join(model.TipTag.tag)
    join_filter = tip_tag_join_tags.filter(model.Tag.tag_state == state)

    return join_filter.paginate(per_page=10)

def get_paginated_city_filtered_tip_tags(city):
    """Returns a pagination object of all tip_tags filtered by the given city"""

    tip_tag_join_tags = model.db.session.query(model.TipTag).join(model.TipTag.tag)
    join_filter = tip_tag_join_tags.filter(model.Tag.tag_city == city)

    return join_filter.paginate(per_page=10)

def get_dict_of_tip_tag_pages(pagination_obj):
    """Returns a dictionary of pagination items, where keys are page numbers and values are a list of items displayed per page"""

    pages_iter = pagination_obj.iter_pages()
    pages_dict = {}
    for page in pages_iter:
        tip_tags = pagination_obj.items
        tip_tag_dict = make_dict_of_tip_tags(tip_tags)
        pages_dict[page] = tip_tag_dict
        pagination_obj = pagination_obj.next()
    
    return pages_dict

def make_dict_of_tip_tags(tip_tags):
    """Helper function for view_travel_tips filtering, to return a dictionary to then jsonify
        Dictionary will hold data for the tip_tag as well as its corresponding tip and tag objects"""

    tip_tag_dict = {}
    for i, tip_tag in enumerate(tip_tags):
        tip_tag_dict[i] = {
            "tip_text" : tip_tag.tip.tip_text,
            "tag_name" : tip_tag.tag.tag_name,
            "tag_state" : tip_tag.tag.tag_state,
            "tag_city" : tip_tag.tag.tag_city
        }
    
    return tip_tag_dict

def navigate_through_pages(page_num, pagination_obj):
    """Returns the pagination object for the given page number"""

    if page_num != 1:
        i = 0
        while i < page_num:
            tip_tag_pagination = pagination_obj.next()
            i += 1
    else:
        tip_tag_pagination = pagination_obj

    return tip_tag_pagination

def get_tip_tag_by_tag_id(tag_id):
    """Query and return the first tip_tag with the given tag_id"""

    return model.TipTag.query.filter(model.TipTag.tag_id == tag_id).first()

def get_tip_tag_by_tip_id(tip_id):
    """Query and return the first tip_tag with the given tip_id"""

    return model.TipTag.query.filter(model.TipTag.tip_id == tip_id).first()

def get_tip_tag_by_tag(tag):
    """Query and return the first tip_tag with the given tag"""

    return model.TipTag.query.filter(model.TipTag.tag == tag).first()

def get_tip_tag_by_tip(tip):
    """Query and return the first tip_tag with the given tip"""

    return model.TipTag.query.filter(model.TipTag.tip == tip).first()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Tag CRUD functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_tag(tag_name, tag_state, tag_city):
    """Create a new tag, add it to the database, and return it"""

    new_tag = model.Tag(tag_name=tag_name, tag_state=tag_state, tag_city=tag_city)

    model.db.session.add(new_tag)
    model.db.session.commit()

    return new_tag

def show_tags():
    """REturn a list of all tag objects in the database"""

    return model.Tag.query.all()

def show_tag_names():
    """Return a list of all tag_names in the database"""

    return model.db.session.query(model.Tag.tag_name).all()

def order_tags_by_tag_name():
    """Returns all tags ordered by the tag_name"""

    return model.db.session.query(model.Tag).order_by(model.Tag.tag_name).all()

def show_tag_states():
    """Return a list of all tag_states in the database"""

    return model.db.session.query(model.Tag.tag_state).all()

def order_tags_by_tag_state():
    """Returns all tags ordered by tag state"""

    return model.db.session.query(model.Tag).order_by(model.Tag.tag_state).all()

def show_tag_cities():
    """Return a list of all tag_cities in the database"""

    return model.db.session.query(model.Tag.tag_city).all()

def order_tags_by_tag_city():
    """Returns a list of all tags ordered by the tag_city"""

    return model.db.session.query(model.Tag).order_by(model.Tag.tag_city).all()

def get_tags_by_tag_name(tag_name):
    """Return a list of all tags with a given tag_name"""

    return model.Tag.query.filter(model.Tag.tag_name == tag_name).all()

def get_tags_by_tag_state(state):
    """Return a list of all tags with a given tag_state"""

    state_tags = model.Tag.query.filter(model.Tag.tag_state == state).all()
    return state_tags

def get_tags_by_tag_city(city):
    """Return a list of all tags with a given tag_city"""

    city_tags = model.Tag.query.filter(model.Tag.tag_city == city).all()
    return city_tags

def check_if_state_in_tag_states(state):
    """Queries a list of all tag_states in database and searches for the given state, returns Boolean"""

    tag_states = show_tag_states()
    #Show_tag_states returns a list of Tuples, need to iterate through that list to check for inclusion
    for tag_state in tag_states:
        if state in tag_state:
            return True
    return False

def check_if_city_in_tag_cities(city):
    """Queries a list of all tag_cities in database and searches for the given city, returns Boolean"""

    tag_cities = show_tag_cities()
    #Show_tag_cities returns a list of Tuples, need to iterate through that list to check for inclusion
    for tag_city in tag_cities:
        if city in tag_city:
            return True
    return False

def parse_through_tags(tags):
    """Helper function for show_destination_details view function
        Parses through the result of querying for a list of all tags to return a list of tip_tags"""

    tip_tags = []
    for tag in tags:
        #tag.tip_tag returns a list (even if there's only one)
        #Want to go through and append the individual object, to return a list not a list of lists
        tip_tag_list = tag.tip_tag
        for tip_tag in tip_tag_list:
            tip_tags.append(tip_tag)

    return tip_tags

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Format dates inputted by HTML form~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def format_date_strings(date):
    """Takes string in yyyy-mm-dd format and returns datetime to display on desitnation_details page"""

    format = "%Y-%m-%d"
    return datetime.strptime(date, format)

def format_time_strings(time):
    """Takes string in HH:MM:SS 24 hour time and returns a string in HH:MM format to display on destination_details page"""

    time_split = time.split(":")
    hour = time_split[0]
    hour = int(hour)
    minute = time_split[1]
    if hour > 12:
        hour = hour-12
        time_split[2] = "PM"
        time_split[0] = str(hour) + ':'
        return ''.join(time_split)
    elif hour == 12:
        time_split[2] = "PM"
        time_split[0] = str(hour) + ':'
        return ''.join(time_split)
    else:
        time_split[2] = "AM"
        time_split[0] = str(hour) + ':'
        return ''.join(time_split)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions for TicketMaster API: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Notes on Ticketmaster Discovery API:
    #The results are not entirely consistent, some events have data for the event time and date, others just the date
        #some events have data for the venue, others don't, included in these functions are helper functions to parse through

def reformat_city_names(city_name):
    """Reformats the city name so that it can be passed in API url"""

    formatted_city = ""

    for char in city_name:
        if char == " ":
            formatted_city += "%20"
        else:
            formatted_city += char
    
    return formatted_city

def reformat_date(date):
    """Reformats the given date so that it can be passed through an API request"""
    #TicketMaster dates are YYYY-MM-DD
    #My date inputs are currently YYYY-MM-DD
    time = "T00:00:00Z"
    date = str(date)
    formatted_date = date+time
    return formatted_date

def search_events_by_city(api_key, city):
    """Searches for events in Ticketmaster in a given city area. Returns the results as JSON object"""

    formatted_city = reformat_city_names(city_name=city)

    url = f"https://app.ticketmaster.com/discovery/v2/events?apikey={api_key}&locale=*&city={formatted_city}"

    response = requests.get(url)

    results = response.json()

    if results["_embedded"]:
        #If the query returns results store them in a variable that is then returned
        all_events = results["_embedded"]["events"]
        return all_events
    else:
        #otherwiese, return False
        return False

def search_events_by_dates(api_key, start_date, end_date):
    """Searches for events in the TicketMaster API for a given date range. Returns JSON"""

    formatted_start_date = reformat_date(date=start_date)
    formatted_end_date = reformat_date(date=end_date)

    url = f"""https://app.ticketmaster.com/discovery/v2/events?apikey={api_key}&locale=*&startDateTime={formatted_start_date}&endDateTime={formatted_end_date}"""
    
    response = requests.get(url)

    results = response.json()

    if results["_embedded"]:
        #If the query returns results store them in a variable that is then returned
        all_events = results["_embedded"]["events"]
        return all_events
    else:
        #otherwiese, return False
        return False

def search_events_by_city_and_dates(api_key, city, start_date, end_date):
    """Searches for events in TicketMaster in a given city area from a given date to a given end date
    Returns the results as JSON"""

    formatted_city = reformat_city_names(city_name=city)
    formatted_start_date = reformat_date(date=start_date)
    formatted_end_date = reformat_date(date=end_date)

    url = f"""https://app.ticketmaster.com/discovery/v2/events?apikey={api_key}&locale=*&startDateTime={formatted_start_date}&endDateTime={formatted_end_date}&city={formatted_city}"""
        
    response = requests.get(url)

    results = response.json()

    if "_embedded" in results.keys():
        #If the query returns results store them in a variable that is then returned
        all_events = results["_embedded"]["events"]
        return all_events
    else:
        #otherwiese, return False
        return False

def clean_up_event_results(all_events):
    """Loop through all_events returned from API request and return data needed for webapp functions"""
    event_names = []
    event_urls = []
    img_urls = []
    start_dates = []
    start_times = []
    venues = []
    for event in all_events:
        #all events have a name, stored under 'name' key
        event_names.append(event["name"])
        #all events have a url that links to a page to buy tickets, stored under 'url' key
        event_urls.append(event['url'])
        #all events have a list of images, stored under the 'images' key
        #I will take the image at the first index and maintain format consistency using CSS styling
        img_urls.append(event['images'][0]['url'])
        #all events have a start date, stored under the 'dates' key, then 'start key

        start_dates.append(event['dates']['start']['localDate'])
        #NOT all events have a start time, need to check if it is there first:
        if 'localTime' in event['dates']['start'].keys():
            time = format_time_strings(event['dates']['start']['localTime'])
            start_times.append(time)
        else:
            #Need to append a value to start_times so that start_times[index] matches the event at even_names[index]
            start_times.append(False)
        #NOT all events have a venue, need to check if it is there first:
        if 'venues' in event['_embedded'].keys():
            venues.append(event['_embedded']['venues'][0]['name'])
        else:
            venues.append(False)

    return event_names, event_urls, img_urls, start_dates, start_times, venues

if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)
    model.db.create_all()