"""Server for travel safety app."""

# from re import U
from flask import Flask, render_template, request, flash, session, redirect, jsonify

import model
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "@#%()#HRTN$#OT#%ons!"
app.jinja_env.undefined = StrictUndefined

MY_API_KEY = "PASS"

model.connect_to_db(app)
model.db.create_all()


#===========================HELPER FUNCTION FOR SEARCH DESTINATION AND VIEW TIPS ROUTES==================
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

#========================HOMEPAGE ROUTE================================
@app.route("/")
def show_homepage():
    """Renders the homepage html to bring users to the homepage of app"""

    return render_template("homepage.html")


#========================LOGIN ROUTE FUNCTIONS================================
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

#========================LOGOUT ROUTE================================     
@app.route("/logout")
def log_user_out():
    """Logs the user out of their profile and removes them from session"""

    session.clear()
    return redirect("/")

#========================PROFILE ROUTE================================
@app.route("/profile/<username>")
def show_user_profile(username):
    """Renders the user's profile page once they have logged in"""

    user = crud.get_user_by_username(username)

    vacations = user.vacation
 
    return render_template("profile.html", user=user, vacations=vacations)

#========================CREATE ACCOUNT ROUTE FUNCTIONS================================
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

#========================================VIEW TRAVEL TIPS ROUTE FUNCTIONS===========================================
@app.route("/view_travel_tips")
def show_travel_tips():
    """Renders the travel_tips page to show all tips in the database"""

    tips = crud.show_tips()
    tags = crud.show_tags()

    return render_template("travel_tips.html", tips=tips, tags=tags)

def make_dict_of_tip_tags(tip_tags):
    """Helper function for view_travel_tips filtering, to return a dictionary to then jsonify
        Dictionary will hold data for the tip_tag as well as its corresponding tip and tag objects"""

    tip_tag_dict = {}
    for tip_tag in tip_tags:
        tip_tag_dict["tip_tag_id"] = tip_tag.tip_tag_id
        tip_tag_dict["tip_id"] = tip_tag.tip.tip_id
        tip_tag_dict["tip_text"] = tip_tag.tip.tip_text
        tip_tag_dict["tag_id"] = tip_tag.tag.tag_id
        tip_tag_dict["tag_name"] = tip_tag.tag.tag_name.title()
        tip_tag_dict["tag_state"] = tip_tag.tag.tag_state
        tip_tag_dict["tag_city"] = tip_tag.tag.tag_city
    
    return tip_tag_dict

@app.route("/view_travel_tips/filtered_by_location.json")
def show_travel_tips_filtered_by_location():
    """Filters travel tips by the state and city inputted by user and returns them"""

    state = request.args.get("state")
    city = request.args.get("city")

    state_in_tags = crud.check_if_state_in_tag_states(state=state)
    city_in_tags = crud.check_if_city_in_tag_cities(city=city)
    #both CRUD functions return a Boolean

    if city_in_tags == True:
        city_tags = crud.get_tags_by_tag_city(city=city)
        city_tip_tags = parse_through_tags(tags=city_tags)
        tip_tag_dict = make_dict_of_tip_tags(tip_tags=city_tip_tags)
        return jsonify(tip_tag_dict)
    
    elif state_in_tags == True:
        state_tags = crud.get_tags_by_tag_state(state=state)
        state_tip_tags = parse_through_tags(tags=state_tags)

        tip_tag_dict = make_dict_of_tip_tags(tip_tags=state_tip_tags)
        return jsonify(tip_tag_dict)
    
    else:
        return ""


#================================CREATE TRAVEL TIP ROUTE FUNCTIONS================================
@app.route("/create_tip")
def show_new_tip():
    """Renders the new_tip page to allow a user to create a new travel tip"""

    return render_template("new_tip.html")


@app.route("/add_new_tip")
def add_new_tip():
    """Adds new tip to the database after they submit the add new tip form"""

    # username= request.form.get("username")
    if session == {}:
        flash("Please log in first")
        return redirect("/login")

    username = session["logged_in_username"]

    state_name= request.args.get("state").title()
    city_name= request.args.get("city").title()

    tip_text = request.args.get("tip-text")

    tag_name = request.args.get("tags")

    user = crud.get_user_by_username(username=username)

    new_tip = crud.create_tip(tip_text=tip_text, user_id=user.user_id)
    new_tag = crud.create_tag(tag_name=tag_name, tag_state=state_name, tag_city=city_name)
    new_tip_tag = crud.create_tip_tag(tag_id=new_tag.tag_id, tip_id=new_tip.tip_id)

    flash(f"Thank you for adding your tip about {city_name}, {state_name}")
    return redirect("/view_travel_tips")


#================================CREATE VACATION ROUTE FUNCTIONS================================
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

    check_city, check_state = crud.check_if_city_state_in_db_create_if_not(city=city, state=state)
    
    new_vacation_label = crud.create_vacation_label(departure_date=departure_date, arrival_date=arrival_date, state_id=check_state.state_id)
    new_vacation = crud.create_vacation(vacation_label_id=new_vacation_label.vacation_label_id, user_id=user.user_id)

    return redirect(f"/profile/{user.username}")

#================================SEARCH DESTINATION ROUTE FUNCTIONS================================
@app.route("/search_destination")
def show_search_destination_page():
    """Renders the search page where user can select a destination to search"""

    return render_template("search_destination_page.html")


@app.route("/destination_details")
def show_destination_details():
    """Shows user a page with travel tips and events for given destination"""

    state = request.args.get("state").title()
    city = request.args.get("city").title()
    departure_date = request.args.get("departure-date")
    arrival_date = request.args.get("arrival-date")

    events = crud.search_events_by_city_and_dates(api_key=MY_API_KEY, city=city, start_date=departure_date, end_date=arrival_date)

    event_names, event_urls, img_urls, start_dates, start_times, venues = crud.clean_up_event_results(all_events=events)

    state_in_tags = crud.check_if_state_in_tag_states(state=state)
    city_in_tags = crud.check_if_city_in_tag_cities(city=city)
    #both CRUD functions return a Boolean

    if city_in_tags == True:
        city_tags = crud.get_tags_by_tag_city(city=city)
        city_tip_tags = parse_through_tags(tags=city_tags)
        
        return render_template("destination_details.html", tip_tags=city_tip_tags, city=city, state=state, 
        departure_date=departure_date, arrival_date=arrival_date, event_names=event_names, event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,
        start_times=start_times, venues=venues)
    
    elif state_in_tags == True:
        state_tags = crud.get_tags_by_tag_state(state=state)
        state_tip_tags = parse_through_tags(tags=state_tags)

        return render_template("destination_details.html", tip_tags=state_tip_tags, city=city, state=state, 
        departure_date=departure_date, arrival_date=arrival_date, event_names=event_names, event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,
        start_times=start_times, venues=venues)
    
    else:
        return render_template("destination_details.html", tip_tags=[], city=city, state=state, 
        departure_date=departure_date, arrival_date=arrival_date, event_names=event_names, event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,
        start_times=start_times, venues=venues)


if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)