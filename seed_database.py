import os
import json
import urllib
import requests 

import crud
import model
import server

# url = 'https://parseapi.back4app.com/classes/Usabystate_States/list-of-cities?keys=name,totalAreaSquareKilometers,totalAreaSquareMiles,updatedAt,waterAreaSquareKilometers,waterAreaSquareMiles'

# payload = {
#     'X-Parse-Application-Id': 'x2ZubjWTlPlsKQlzW3uKTZNmAQfxBE7cI5UIdEH7', # This is the app's application id
#     'X-Parse-REST-API-Key': 'Fg07v7RB9wDdO9bTa52gtWsu1GYGN7aFG64WfQzu' # This is the app's REST API key
# }

# response = requests.get(url, params=payload)
# # data.content.decode('utf-8')
# # print(json.dumps(data, indent=2))
# data = response.json()
# print('\n*'*5)
# print(data)
# print('\n*'*5)

os.system('dropdb travel_project')
os.system('createdb travel_project')

model.connect_to_db(server.app)
model.db.create_all()

FIRST_NAMES = ["Ruby", "Shawn", "Gus", "Juliet", "Carlton", "Olivia", "Amanda", "Sonny", "Fin", "Karen"]
LAST_NAMES = ["Waddell", "Spencer", "Burton", "O'Hara", "Lassiter", "Benson", "Rollins", "Carisi", "Tutuola", "Vick"]

STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
        "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", 
        "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

CA_CITIES = ["San Francisco", "Oakland", "Sacramento", "Palo Alto", "Santa Cruz",
            "Carmel", "Monterey", "Los Angeles", "San Luis Obispo", "Capitola"]

users_in_db = []
travels_in_db = []
states_in_db = []
cities_in_db = []
tips_in_db = []
# tags_in_db = []
# tip_tags_in_db = []


def seed_users_table():
    """Seed User table with test data"""
    for n in range(10):
        
        fname = FIRST_NAMES[n]
        lname = LAST_NAMES[n]
        username = f"{fname.lower()}{n}"
        email = f"{fname.lower()}@test.com"
        password = f"Password{n}!"

        new_user = crud.create_user(username, fname, lname, email, password)
        users_in_db.append(new_user)

    return users_in_db

def seed_travels_table():
    """Seed Travel table with test data"""

    for n in range(10):

        departure_date = f"01.{n+1}.2010"
        arrival_date = f"01.{n+5}.2010"

        new_travel = crud.create_travel(departure_date=departure_date, arrival_date=arrival_date)
        travels_in_db.append(new_travel)
    
    return travels_in_db

def seed_states_table():
    """Seed State table with test data"""

    for n in range(50):
        state_name = STATES[n]
        new_state = crud.create_state(state_name=state_name)
        states_in_db.append(new_state)
    
    return states_in_db

def seed_cities_table():
    """Seed City table with example data"""
    for n in range(10):
        new_city = crud.create_city(city_name= CA_CITIES[n])
        cities_in_db.append(new_city)

    return cities_in_db

def seed_tips_table():
    """Seed Tip table with example data"""

    for n in range(10):
        tip_text = f"Test tip {n}"
        new_tip = crud.create_tip(tip_text)
        tips_in_db.append(new_tip)
    
    return tips_in_db