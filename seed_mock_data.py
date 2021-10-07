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

def seed_user_table():
    """Seed user table with mock user data"""

    with open("data/mock_user_data.json") as users:
        user_data = json.loads(users.read())
    
    for user in user_data:
        username = user["username"]
        fname = user["fname"]
        lname = user["lname"]
        email = user["email"]
        password = user["password"]
        
        new_user = crud.create_user(username=username, fname=fname,
            lname=lname, email=email, password=password)
        
        users_in_db.append(new_user)

    return users_in_db

def seed_travel_table():
    """Seed travels table with mock travel data"""

    with open("data/mock_travel_data.json") as travels:
        travel_data = json.loads(travels.read())

    for travel in travel_data:
        departure_date = travel["departure_date"]
        arrival_date = travel["arrival_date"]

        new_travel = crud.create_travel(departure_date=departure_date, arrival_date=arrival_date)

        travels_in_db.append(new_travel)
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