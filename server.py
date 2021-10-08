"""Server for travel safety app."""

# from re import U
from flask import Flask, render_template, request, flash, session, redirect

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

    users_in_db = crud.show_users()
    if username in users_in_db:
        flash("Logged in!")
        return redirect(f"/profile/{username}")
    else:
        flash("Username not recognized, please create an account")
        return redirect("/create_account")

@app.route("/profile/<username>")
def show_user_profile(username):
    """Renders the user's profile page once they have logged in"""

    user = crud.get_user_by_username(username)
    
    return render_template("profile.html", user=user)

@app.route("/create_account")
def show_create_account():
    """Renders the create_account page to allow a user to create a new account"""

    return render_template("create_account.html")

@app.route("/new-user", methods=["POST"])
def add_new_user():
    """Adds new user to the database after they submit """

    username= request.form.get("username")
    fname= request.form.get("fname")
    lname= request.form.get("lname")
    email= request.form.get("email")
    password= request.form.get("password")

    departure_date= request.form.get("departure-date")
    arrival_date= request.form.get("arrival-date")

    state= request.form.get("state")
    city= request.form.get("city")

    new_city = crud.create_city(city_name=city)
    new_state = crud.create_state(state_name=state, city_id=new_city.city_id)
    new_vacation_label = crud.create_vacation_label(departure_date=departure_date, arrival_date=arrival_date,
                        state_id=new_state.state_id)
    new_vacation = crud.create_vacation(vacation_label_id=new_vacation_label.vacation_label_id)
    new_user = crud.create_user(username=username, fname=fname, lname=lname, email=email, password=password,
                                    vacation_id=new_vacation.vacation_id)
    
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
    username= request.form.get("username")

    state_name= request.form.get("state")
    city_name= request.form.get("city")

    tip_text = request.form.get("tip-text")

    tag_name = request.form.get("tags")

    user = model.User.query.filter(model.User.username == username).first()

    if user == None:
        flash("Please login before adding a travel tip")
        return redirect("/login")
    
    else:
        new_tip = crud.create_tip(tip_text=tip_text, user_id=user.user_id)
        new_tag = crud.create_tag(tag_name=tag_name, tag_state=state_name, tag_city=city_name)
        new_tip_tag = crud.create_tip_tag(tag_id=new_tag.tag_id, tip_id=new_tip.tip_id)

        flash(f"Thank you for adding your tip about {city_name}, {state_name}")
        return redirect("/view_travel_tips")


if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)