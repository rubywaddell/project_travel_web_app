"""Server for travel safety app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
# from flask.helpers import _prepare_send_file_kwargs

import model
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "@#%()#HRTN$#OT#%ons!"
app.jinja_env.undefined = StrictUndefined


MY_API_KEY = "NdMgdlGGSobRosfxcoA3WH8r8ifKMjOX"

model.connect_to_db(app)
model.db.create_all()


#=================================================HOMEPAGE ROUTE========================================================
@app.route("/")
def show_homepage():
    """Renders the homepage html to bring users to the homepage of app"""

    return render_template("homepage.html")


#=====================================================SESSION ROUTE=======================================================
@app.route("/check_session")
def check_session_for_user():
    """Checks the session to see if user is logged in, and returns username or False as strings for AJAX functions in navigation_bar"""
    if session == {}:
        return "False"
    else:
        username = session["logged_in_username"]
 
        return username

#=================================================LOGIN ROUTE FUNCTIONS=================================================
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
        return "Username not recognized, please create an account"

    elif (username == user.username) and (password != user.password):
        return "Incorrect password"

    elif (username == user.username) and (password == user.password):
        flash("Logged in!")
        session["logged_in_username"] = user.username
        return redirect(f"/profile_{username}")

#=================================================LOGOUT ROUTE=================================================     
@app.route("/logout")
def log_user_out():
    """Logs the user out of their profile and removes them from session"""

    session.clear()
    return redirect("/login")

#======================================================PROFILE ROUTE========================================================
@app.route("/profile_<username>")
def show_user_profile(username):
    """Renders the user's profile page once they have logged in"""

    user = crud.get_user_by_username(username)

    tips = user.tip
    tip_tags = []
    for tip in tips:
        tip_tag = crud.get_tip_tag_by_tip(tip=tip)
        tip_tags.append(tip_tag)

    vacations = user.vacation

    if len(vacations) == 1:
        city = vacations[0].vacation_label.state.city.city_name
        departure_date = vacations[0].vacation_label.departure_date
        arrival_date = vacations[0].vacation_label.arrival_date

        events = crud.search_events_by_city_and_dates(api_key=MY_API_KEY, city=city, start_date=departure_date, end_date=arrival_date)
        if events:
            event_names, event_urls, img_urls, start_dates, start_times, venues = crud.clean_up_event_results(all_events=events)

            return render_template("profile.html", user=user, vacations=vacations, tip_tags=tip_tags, event_names=event_names, 
                event_urls=event_urls, img_urls=img_urls, start_dates=start_dates, start_times=start_times, venues=venues)
        
        else:   
            return render_template("profile.html", user=user, vacations=vacations, tip_tags=tip_tags, event_names=False)

    else:   
        return render_template("profile.html", user=user, vacations=vacations, tip_tags=tip_tags, event_names=False)

@app.route("/delete_vacation_<vacation_id>")
def delete_vacation(vacation_id):
    """Deletes a vacation from the database, called when user clicks delete button in profile"""

    vacation = crud.get_vacation_by_id(vacation_id=vacation_id)
    crud.delete_vacation(vacation=vacation)
    user_id = vacation.user_id
    user = crud.get_user_by_id(user_id)

    return redirect(f"/profile_{user.username}")


#======================================================EDIT PROFILE ROUTE========================================================
@app.route("/edit_profile")
def show_edit_profile_template():
    """Renders the edit profile template where user can select what they want to change"""

    return render_template("edit_profile.html")

#=================================================CREATE ACCOUNT ROUTE FUNCTIONS=================================================
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

    check_city, check_state = crud.check_if_city_state_in_db_create_if_not(state=state, city=city)
    
    new_vacation_label = crud.create_vacation_label(departure_date=departure_date, arrival_date=arrival_date, state_id=check_state.state_id)
    new_vacation = crud.create_vacation(vacation_label_id=new_vacation_label.vacation_label_id, user_id=new_user.user_id)
    
    session["logged_in_username"] = new_user.username

    return redirect(f"/profile_{new_user.username}")

#=================================================VIEW TRAVEL TIPS ROUTE FUNCTIONS===========================================

@app.route("/view_travel_tips_page_<page_num>")
def show_travel_tips(page_num):
    """Returns the pagination results for the next items in pagination object"""

    page_one = crud.get_paginated_tip_tags()

    pages = crud.get_dict_of_tip_tag_pages(pagination_obj=page_one)

    page_num = int(page_num)

    tip_tag_pagination = crud.navigate_through_pages(pagination_obj=page_one, page_num=page_num)

    return render_template("travel_tips.html", tip_tag_pages=pages, pagination_obj=tip_tag_pagination, page_num=page_num)


#=================================================FILTER TRAVEL TIPS FUNCTIONS================================================

@app.route("/view_travel_tips_filtered_by_location_page_<page_num>")
def show_paginated_travel_tips_filtered_by_location(page_num):
    """Filters travel tips by the state and city inputted by user and returns pagination object"""

    state = request.args.get("state").title()
    city = request.args.get("city").title()

    state_in_tags = crud.check_if_state_in_tag_states(state=state)
    city_in_tags = crud.check_if_city_in_tag_cities(city=city)
    #both CRUD functions return a Boolean

    if city_in_tags == True:
        city_pag_obj = crud.get_paginated_city_filtered_tip_tags(city=city)
        city_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=city_pag_obj)
        page_num = int(page_num)

        if city_pag_obj.page == 1:
            return render_template("travel_tips.html", tip_tag_pages=city_pages, pagination_obj=city_pag_obj, page_num=page_num)
        else:
            page_items = crud.navigate_through_pages(page_num=page_num, pagination_obj=city_pages)
            return render_template("travel_tips.html", tip_tag_pages=city_pages, pagination_obj=page_items, page_num=page_num)
    
    elif state_in_tags == True:
        state_pag_obj = crud.get_paginated_state_filtered_tip_tags(state=state)
        state_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=state_pag_obj)
        page_num = int(page_num)
        if state_pag_obj.page == 1:
            return render_template("travel_tips.html", tip_tag_pages=state_pages, pagination_obj=state_pag_obj, page_num=page_num)
        else:
            page_items = crud.navigate_through_pages(page_num=page_num, pagination_obj=state_pages)
            return render_template("travel_tips.html", tip_tag_pages=state_pages, pagination_obj=page_items, page_num=page_num)
    
    else:
        return render_template("travel_tips.html", tip_tag_pages=False, pagination_obj=False, page_num=page_num)

@app.route("/view_travel_tips_filtered_by_tag_page_<page_num>")
def show_pageinated_travel_tips_filtered_by_tag(page_num):
    """"Filters tips by tag name and returns pagination object"""

    tag_name = request.args.get("filter-tags").lower()

    all_tags = crud.get_tags_by_tag_name(tag_name=tag_name)
    tip_tags = crud.parse_through_tags(tags=all_tags)

    tip_tags_dict = crud.make_dict_of_tip_tags(tip_tags=tip_tags)
    if tip_tags_dict == {}:
        return render_template("travel_tips.html", tip_tag_pages=False, pagination_obj=False, page_num=page_num)
    else:
        tag_pag_obj = crud.get_paginated_tag_filtered_tip_tags(filter_tag=tag_name)
        tag_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=tag_pag_obj)
        page_num = int(page_num)
        if tag_pag_obj.page == 1:
            return render_template("travel_tips.html", tip_tag_pages=tag_pages, pagination_obj=tag_pag_obj, page_num=page_num)
        else:
            page_items = crud.navigate_through_pages(page_num=page_num, pagination_obj=tag_pages)
            return render_template("travel_tips.html", tip_tag_pages=tag_pages, pagination_obj=page_items, page_num=page_num)

#=================================================CREATE TRAVEL TIP ROUTE FUNCTIONS==========================================
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
    return redirect("/view_travel_tips_page_1")


#=================================================CREATE VACATION ROUTE FUNCTIONS================================
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

    return redirect(f"/profile_{user.username}")


#=================================================SEARCH DESTINATION ROUTE FUNCTIONS================================
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

    state_in_tags = crud.check_if_state_in_tag_states(state=state)
    city_in_tags = crud.check_if_city_in_tag_cities(city=city)
    #both CRUD functions return a Boolean

    events = crud.search_events_by_city_and_dates(api_key=MY_API_KEY, city=city, start_date=departure_date, end_date=arrival_date)
    if events:
        #If the query returns a list of events, then retrieve the necessary information to display
        event_names, event_urls, img_urls, start_dates, start_times, venues = crud.clean_up_event_results(all_events=events)

        if city_in_tags == True:
            city_tags = crud.get_tags_by_tag_city(city=city)
            city_tip_tags = crud.parse_through_tags(tags=city_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)
            
            return render_template("destination_details.html", tip_tags=city_tip_tags, city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=event_names, event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,
            start_times=start_times, venues=venues)
        
        elif state_in_tags == True:
            state_tags = crud.get_tags_by_tag_state(state=state)
            state_tip_tags = crud.parse_through_tags(tags=state_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)

            return render_template("destination_details.html", tip_tags=state_tip_tags, city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=event_names, event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,
            start_times=start_times, venues=venues)
        
        else:
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)
            return render_template("destination_details.html", tip_tags=[], city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=event_names, event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,
            start_times=start_times, venues=venues)

    else:
        #If there are not events for the given search
        if city_in_tags == True:
            city_tags = crud.get_tags_by_tag_city(city=city)
            city_tip_tags = crud.parse_through_tags(tags=city_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)
            
            return render_template("destination_details.html", tip_tags=city_tip_tags, city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=False)
        
        elif state_in_tags == True:
            state_tags = crud.get_tags_by_tag_state(state=state)
            state_tip_tags = crud.parse_through_tags(tags=state_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)

            return render_template("destination_details.html", tip_tags=state_tip_tags, city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=False)
        
        else:
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)
            return render_template("destination_details.html", tip_tags=[], city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=False)

if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)