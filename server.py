"""Server for travel safety app."""

# from re import U
from flask import Flask, render_template, request, flash, session, redirect, jsonify

import model
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "@#%()#HRTN$#OT#%ons!"
app.jinja_env.undefined = StrictUndefined

model.connect_to_db(app)
model.db.create_all()

@app.route("/")
def show_homepage():
    """Renders the homepage html to bring users to the homepage of app"""

    return render_template("homepage.html")

@app.route("/view_travel_tips")
def show_travel_tips():
    """Renders the travel_tips page to show all tips in the database"""

    tips = crud.show_tips()
    tags = crud.show_tags()

    return render_template("travel_tips.html", tips=tips, tags=tags)

@app.route("/login")
def show_login_page():
    """Renders the login page to allow users to log in to their account"""
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def check_user_in_database():
    """Takes in log-in form submission and redirects depending on if user is in db or not"""

    username = request.form.get("username")
    password = request.form.get("password")

    user = crud.get_user_by_username(username=username)

    if user == None:
        flash("Username not recognized, please create an account")
        return redirect("/create_account")

    elif (username == user.username) and (password != user.password):
        flash("Incorrect password, please try again")
        return redirect("/login")

    elif (username == user.username) and (password == user.password):
        flash("Logged in!")
        session["logged_in_username"] = user.username
        return redirect(f"/profile/{username}")

    else:
        flash("Something else is happening")
        return redirect("/login")
        
@app.route("/logout")
def log_user_out():
    """Logs the user out of their profile and removes them from session"""

    session.pop("logged_in_username")
    return redirect("/")

@app.route("/profile/<username>")
def show_user_profile(username):
    """Renders the user's profile page once they have logged in"""

    user = crud.get_user_by_username(username)

    user_vacation_query = model.db.session.query(model.User).options(
        model.db.joinedload(model.User.vacation, innerjoin=True).
            joinedload(model.Vacation.vacation_label, innerjoin=True).
                joinedload(model.VacationLabel.state, innerjoin=True)
                    ).filter(model.User.user_id == user.user_id)

    user_vacations = model.Vacation.query.filter(model.Vacation.user_id == user.user_id).all()

    vacation_labels = []

    test = []
    #Is not iterating correctly, when looking at type of user_vacations it's a list
    #But, doing for vacation in user_vacations
    #and for i in range(len(user_vacations))
    #just return the same object each time, it doesn't seem to actually be getting to the first index
    #just returns the 0 index
    
    for i in range(len(user_vacations)):
        vacation_id = user_vacations[i].vacation_id
        vacation_label = model.db.session.query(model.VacationLabel).options(
            model.db.joinedload(model.VacationLabel.vacation)
        ).filter(model.Vacation.vacation_id == vacation_id).first()
        vacation_labels.append(vacation_label)
    
    states = []

    for vacation_label in vacation_labels:
        vacation_label_id = vacation_label.vacation_label_id
        state = model.db.session.query(model.State).options(
            model.db.joinedload(model.State.vacation_label)
        ).filter(model.VacationLabel.vacation_label_id == vacation_label_id).first()
        states.append(state)

    print("\n"*5)
    print("="*40)
    print(user_vacations)
    print(type(user_vacations))
    # print(user_vacations.vacation.vacation_id)
    # print(user_vacation_labels)
    # print(user_vacation_query)
    # print(user_vacation_query.all())
    print(vacation_labels)
    print(states)
    print("="*40)
    print("\n"*5)
    
    return render_template("profile.html", user=user)


@app.route("/create_account")
def show_create_account():
    """Renders the create_account page to allow a user to create a new account"""

    return render_template("create_account.html")


@app.route("/new-user", methods=["POST"])
def add_new_user():
    """Adds new user to the database after they submit """

    username= request.form.get("username")
    fname= request.form.get("fname").title()
    lname= request.form.get("lname").title()
    email= request.form.get("email")
    password= request.form.get("password")

    new_user = crud.create_user(username=username, fname=fname, lname=lname, email=email, password=password)

    departure_date= request.form.get("departure-date")
    arrival_date= request.form.get("arrival-date")

    state= request.form.get("state").title()
    city= request.form.get("city").title()

    check_state, check_city = crud.check_if_city_state_in_db_create_if_not(state=state, city=city)
    
    new_vacation_label = crud.create_vacation_label(departure_date=departure_date, arrival_date=arrival_date, state_id=check_state.state_id)
    new_vacation = crud.create_vacation(vacation_label_id=new_vacation_label.vacation_label_id, user_id=new_user.user_id)
    
    session["logged_in_username"] = new_user.username

    return redirect(f"/profile/{new_user.username}")


@app.route("/create_tip")
def show_new_tip():
    """Renders the new_tip page to allow a user to create a new travel tip"""

    return render_template("new_tip.html")


@app.route("/add_new_tip", methods=["POST"])
def add_new_tip():
    """Adds new tip to the database after they submit the add new tip form"""
#Need to look more into how to get the value of checkbox and radio button inputs
#currently just returning None, can't save None to the database
    # username= request.form.get("username")
    if session == {}:
        flash("Please log in first")
        return redirect("/login")

    username = session["logged_in_username"]

    state_name= request.form.get("state").title()
    city_name= request.form.get("city").title()

    tip_text = request.form.get("tip-text")

    tag_name = request.form.get("tags")

    user = crud.get_user_by_username(username=username)

    new_tip = crud.create_tip(tip_text=tip_text, user_id=user.user_id)
    new_tag = crud.create_tag(tag_name=tag_name, tag_state=state_name, tag_city=city_name)
    new_tip_tag = crud.create_tip_tag(tag_id=new_tag.tag_id, tip_id=new_tip.tip_id)

    flash(f"Thank you for adding your tip about {city_name}, {state_name}")
    return redirect("/view_travel_tips")


@app.route("/create_vacation")
def show_new_vacation():
    """Renders for that allows users to create a new vacation for their profile"""

    if session == {}:
        flash("Please log in first!")
        return redirect("/login")

    return render_template("new_vacation.html")


@app.route("/add_new_vacation")
def add_new_vacation():
    """Adds new vacation to the database once user submits form"""
    
    username = session["logged_in_username"]
    user = crud.get_user_by_username(username=username)

    state = request.args.get("state").title()
    city = request.args.get("city").title()
    departure_date = request.args.get("departure-date")
    arrival_date = request.args.get("arrival-date")

    check_state, check_city = crud.check_if_city_state_in_db_create_if_not(state=state, city=city)
    
    new_vacation_label = crud.create_vacation_label(departure_date=departure_date, arrival_date=arrival_date, state_id=check_state.state_id)
    new_vacation = crud.create_vacation(vacation_label_id=new_vacation_label.vacation_label_id, user_id=user.user_id)

    return redirect(f"/profile/{user.username}")


@app.route("/search_destination")
def show_search_destination_page():
    """Renders the search page where user can select a destination to search"""
    states = crud.show_tag_states()
    states = set(states)
    states = list(states)
    states.sort()
    return render_template("search_destination_page.html", states=states)


@app.route("/search_destination/cities.json")
def show_search_destination_page_w_cities():
    """Using AJAX, shows the cities associated with the chosen state"""

    state_name = request.args.get("state").title()

    state_tags = crud.get_tags_by_tag_state(state=state_name)
    #crud.get_tags_by_tag_state returns a list of tag objects
    #will return duplicates, need to get rid of them for the dropdown list
    cities_list = []
    cities_dict = {}
    
    for tag in state_tags:
        cities_list.append(tag.tag_city)

    cities_set = set(cities_list)

    for i, city in enumerate(cities_set):
        cities_dict[i] = city

    return jsonify(cities_dict)
    

if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)