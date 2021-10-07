"""Server for travel safety app."""

from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "@#%()#HRTN$#OT#%ons!"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def show_homepage():
    """Renders the homepage html to bring users to the homepage of app"""

    return render_template("homepage.html")


if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)