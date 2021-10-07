from io import TextIOWrapper
import os
import json

import crud
import model
import server

os.system('dropdb travel_project')
os.system('createdb travel_project')

model.connect_to_db(server.app)
model.db.create_all()


users_in_db = []
travels_in_db = []
states_in_db = []
cities_in_db = []
tips_in_db = []
tags_in_db = []
tip_tags_in_db = []

def seed_user_table():
    """Seed user table with mock user data"""

    with open("data/mock_user_data.json") as users:
        user_data = json.loads(users.read())
    i = 0
    for user in user_data:
        username = user["username"]
        fname = user["fname"]
        lname = user["lname"]
        email = user["email"]
        password = user["password"]
        
        travel_id = travels_in_db[i].travel_id

        new_user = crud.create_user_with_travel_id(username=username, fname=fname,
            lname=lname, email=email, password=password, travel_id=travel_id)
        
        users_in_db.append(new_user)

        i += 1

    return users_in_db

def seed_travel_table():
    """Seed travels table with mock travel data"""

    with open("data/mock_travel_data.json") as travels:
        travel_data = json.loads(travels.read())

    i = 0
    for travel in travel_data:
        departure_date = travel["departure_date"]
        arrival_date = travel["arrival_date"]

        state_id = states_in_db[i].state_id

        new_travel = crud.create_travel_with_state_id(departure_date=departure_date, 
            arrival_date=arrival_date, state_id=state_id)

        travels_in_db.append(new_travel)

        i += 1

    return travels_in_db

def seed_state_table():
    """Seed states table with American states"""

    with open("data/mock_state_data.json") as states:
        state_data = json.loads(states.read())

    for state in state_data:
        state_name = state["state_name"]

        new_state = crud.create_state(state_name)

        states_in_db.append(new_state)
    return states_in_db

def seed_city_table():
    """Seed cities table with mock city data"""

    with open("data/mock_city_data.json") as cities:
        city_data = json.loads(cities.read())
    
    for city in city_data:
        city_name = city["city_name"]

        new_city = crud.create_city(city_name)

        cities_in_db.append(new_city)
    return cities_in_db

def seed_tip_table():
    """Seed tips table with mock data"""

    with open("data/mock_tip_data.json") as tips:
        tip_data = json.loads(tips.read())

    for tip in tip_data:
        tip_text = tip["tip_text"]

        new_tip = crud.create_tip(tip_text)

        tips_in_db.append(new_tip)
    return tips_in_db

def seed_tag_table():
    """Seed tags table with mock data"""

    with open("data/mock_tag_data.json") as tags:
        tag_data = json.loads(tags.read())
    
    for tag in tag_data:
        tag_name = tag["tag_name"]
        new_tag = crud.create_tag(tag_name)
        tags_in_db.append(new_tag)
    return tags_in_db

def seed_tip_tag_table():
    """Seed tip_tags table with mock data"""

    for i in range(50):
        new_tip_tag = crud.create_tip_tag_w_tip_and_tag_id(
            tip_id= tips_in_db[i].tip_id,
            tag_id=tags_in_db[i].tag_id
        )
        tip_tags_in_db.append(new_tip_tag)

    return tip_tags_in_db