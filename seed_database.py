import os
from crud import create_user
import model
import server


os.system('dropdb travel_project')
os.system('createdb travel_project')

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    username = f"username{n}"
    fname = f"first_name{n}"
    lname = f"last_name{n}"
    email = f"user{n}@test.com"
    password = f"password{n}"
    print(f"username={username}, fname={fname}, lname={lname}, email={email}, password={password}")
    new_user = create_user(username, fname, lname, email, password)