"""Server for travel safety app."""

from flask import Flask, render_template, request, flash, session, redirect

import model

import crud

from seed_mock_data import seed_tip_table

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

@app.route("/login")
def show_login_page():
    """Renders the login page to allow users to log in to their account"""
    return render_template("login.html")

# @app.route("/profile/<user_id>", methods=["POST"])
# def show_user_profile(user_id):
#     """Renders the user's profile page once they have logged in"""

#     username = request.form.get("username")
#     user = crud.get_user_by_username(username)
#     return render_template("profile.html", user=user)

@app.route("/view_travel_tips")
def show_travel_tips():
    """Renders the travel_tips page to show all tips in the database"""

    tips = seed_tip_table()

    return render_template("travel_tips.html", tips=tips)

if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)