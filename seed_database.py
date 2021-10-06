import os
import json
import urllib
import requests 

from crud import create_city, create_state, create_travel, create_user
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

for n in range(10):
    
    fname = FIRST_NAMES[n]
    lname = LAST_NAMES[n]
    username = f"{fname.lower()}{n}"
    email = f"{fname.lower()}@test.com"
    password = f"Password{n}!"
    print(f"username={username}, fname={fname}, lname={lname}, email={email}, password={password}")
    new_user = create_user(username, fname, lname, email, password)

    departure_date = f"01.{n+1}.2010"
    arrival_date = f"01.{n+5}.2010"
    new_travel = create_travel(departure_date=departure_date, arrival_date=arrival_date)

for n in range(50):
    state_name = STATES[n]
    new_state = create_state(state_name=state_name)

CITIES = ["San Francisco", "Oakland", "Sacramento", "Palo Alto", "Santa Cruz"]

for city in CITIES:
    state = model.State.query.filter(model.State.state_name == "California").first()
    new_city = create_city(city_name= city, state_id=state.state_id)