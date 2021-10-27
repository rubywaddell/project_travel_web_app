import os
import json

import crud
import model
# import server

print(__name__)
print(type(__name__))
print(__name__ == "__main__")


cities_in_db = []
states_in_db = []
vacation_labels_in_db = []
vacations_in_db = []
users_in_db = []
tips_in_db = []
tip_tags_in_db = []
tags_in_db = []

def seed_cities_table():
    """Seed the cities table with mock data"""
    
    with open("data/mock_city_data.json") as city_data:
            cities = json.loads(city_data.read())
    
    for city in cities:
        new_city = crud.create_city(city_name=city["city_name"])
        cities_in_db.append(new_city)

    return cities_in_db


def seed_states_table():
    """Seed the states table with mock data"""

    with open("data/mock_state_data.json") as state_data:
        states = json.loads(state_data.read())
    
    for i, state in enumerate(states):
        new_state = crud.create_state(state_name=state["state_name"], city_id=cities_in_db[i].city_id)
        states_in_db.append(new_state)
    
    return states_in_db

def seed_vacation_label_table():
    """Seed the vacation_label table with mock data"""

    with open("data/mock_travel_data.json") as vacation_data:
        vacations = json.loads(vacation_data.read())
    
    for i, vacation_label in enumerate(vacations):
        new_vacation_label = crud.create_vacation_label(departure_date=vacation_label["departure_date"],
                arrival_date=vacation_label["arrival_date"], state_id=states_in_db[i].state_id)

        model.db.session.add(new_vacation_label)
        model.db.session.commit()

        vacation_labels_in_db.append(new_vacation_label)
    
    return vacation_labels_in_db 

def seed_vacation_table():
    """Seed the vacations table with mock data"""

    for i, vacation_label in enumerate(vacation_labels_in_db):
        user_id = users_in_db[i].user_id
        new_vacation = crud.create_vacation(vacation_label_id=vacation_label.vacation_label_id, user_id=user_id)
        vacations_in_db.append(new_vacation)

    return vacations_in_db

def seed_user_table():
    """Seed the users table with mock data"""

    with open("data/mock_user_data.json") as user_data:
        users = json.loads(user_data.read())
    
    for i, user in enumerate(users):

        username = user["username"]
        fname = user["fname"]
        lname = user["lname"]
        email = user["email"]
        password = user["password"]

        # vacation_id = vacations_in_db[i].vacation_id        

        new_user = crud.create_user(username=username, fname=fname, lname=lname, email=email, 
                password=password)
        
        users_in_db.append(new_user)

    return users_in_db

def seed_tip_table():
    """Seed the tip table with mock data"""

    with open("data/mock_tip_data.json") as tip_data:
        tips = json.loads(tip_data.read())
    
    for i, tip in enumerate(tips):
        tip_text = tip["tip_text"]
        user_id = users_in_db[i].user_id

        new_tip = crud.create_tip(tip_text=tip_text, user_id=user_id)
        tips_in_db.append(new_tip)
    
    return tips_in_db

def seed_tag_table():
    """Seed the tag table with mock data"""

    with open("data/mock_tag_data.json") as tag_data:
        tags = json.loads(tag_data.read())

    for tag in tags:
        tag_name = tag["tag_name"]
        tag_state = tag["tag_state"]
        tag_city = tag["tag_city"]

        new_tag = crud.create_tag(tag_name=tag_name, tag_state=tag_state, tag_city=tag_city)

        tags_in_db.append(new_tag)
    return tags_in_db

def seed_tip_tag_table():
    """Seed the tip_tag table with mock data"""

    for i in range(len(tips_in_db)):
        tip_id = tips_in_db[i].tip_id
        tag_id = tags_in_db[i].tag_id

        new_tip_tag = crud.create_tip_tag(tag_id=tag_id, tip_id=tip_id)

        tip_tags_in_db.append(new_tip_tag)
    
    return tip_tags_in_db


if __name__ == "__main__":
    import server

    os.system('dropdb travel_app')
    os.system('createdb travel_app')

    model.connect_to_db(server.app)
    model.db.create_all()

seed_cities_table()
seed_states_table()
seed_vacation_label_table()
seed_user_table()
seed_vacation_table()
seed_tip_table()
seed_tag_table()
seed_tip_tag_table()