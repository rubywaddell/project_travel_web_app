"""Server for travel safety app."""

from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

lines = []
with open("secrets.sh") as s:
    for line in s:
        line = line.strip()
        line = line.split("=")
        lines.append(line)

MY_API_KEY = lines[0][1]
app.secret_key = lines[1][1]

connect_to_db(app)
# model.db.create_all()

#=====================================================HOMEPAGE ROUTE========================================================
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

    # pag_obj = crud.get_paginated_user_filtered_tip_tags(user_id=user.user_id)
    # tip_tag_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=pag_obj)

    user_tips = user.tip
    tip_tags = []
    for tip in user_tips:
        tip_tags.extend(tip.tip_tag)
    

    vacations = user.vacation

    if len(vacations) == 1:
        city = vacations[0].vacation_label.state.city.city_name
        departure_date = vacations[0].vacation_label.departure_date
        arrival_date = vacations[0].vacation_label.arrival_date

        events = crud.search_events_by_city_and_dates(api_key=MY_API_KEY, city=city, start_date=departure_date, end_date=arrival_date)
        if events:
            event_names, event_urls, img_urls, start_dates, start_times, venues = crud.clean_up_event_results(all_events=events)

            return render_template("profile.html", user=user, vacations=vacations, tip_tags=tip_tags,event_names=event_names,
            event_urls=event_urls, img_urls=img_urls, start_dates=start_dates, start_times=start_times, venues=venues)
        
        else:   
            return render_template("profile.html", user=user, vacations=vacations, tip_tags=tip_tags, event_names=False)

    else:   
        return render_template("profile.html", user=user, vacations=vacations, tip_tags=tip_tags, event_names=False)


#======================================================EDIT VACATION ROUTES========================================================

@app.route("/delete_vacation_<vacation_id>")
def delete_vacation(vacation_id):
    """Deletes a vacation from the database, called when user clicks delete button in profile"""

    vacation = crud.get_vacation_by_id(vacation_id=vacation_id)
    user = crud.get_user_by_id(vacation.user_id)
    crud.delete_vacation(vacation=vacation)

    vacations = user.vacation
    vacation_labels = []
    for vacation in vacations:
        vacation_labels.append(vacation.vacation_label)

    vacation_label_dict = crud.make_vacation_label_dict(vacation_labels)

    return user.username


@app.route("/edit_vacation_dates_id_<vacation_id>")
def edit_vacation_dates(vacation_id):
    """Edits the departure and arrival dates for the given vacation and redirects to profile"""

    new_departure_date = request.args.get("departure-date")
    new_arrival_date = request.args.get("arrival-date")

    vacation = crud.get_vacation_by_id(vacation_id)
    vacation_label_id = crud.get_vacation_label_by_vacation(vacation).vacation_label_id

    crud.change_arrival_and_departure_dates(vacation_label_id, new_departure_date, new_arrival_date)

    user = crud.get_user_by_vacation_id(vacation_id=vacation_id)

    return redirect(f"/profile_{user.username}")

@app.route("/edit_vacation_location_id_<vacation_id>")
def edit_vacation_location(vacation_id):
    """Edits the location for the given location and redirects to profile"""

    new_state = request.args.get("state")
    new_city = request.args.get("city")

    vacation = crud.get_vacation_by_id(vacation_id)
    vacation_label_id = crud.get_vacation_label_by_vacation(vacation).vacation_label_id

    crud.change_vacation_label_location(vacation_label_id, new_state, new_city)

    user = crud.get_user_by_vacation_id(vacation_id)

    return redirect(f"/profile_{user.username}")


#======================================================EDIT VACATION ROUTES========================================================
@app.route("/edit_tag_name_<tip_tag_id>")
def edit_tag_name(tip_tag_id):
    """Edits the tag_name for the given tag and redirects back to the user profile"""

    new_tag_name = request.args.get("tags")
    tag_id = crud.get_tag_by_tip_tag(tip_tag_id=tip_tag_id).tag_id

    crud.edit_tag_name(new_tag_name=new_tag_name, tag_id=tag_id)

    username = session["logged_in_username"]

    return redirect(f"/profile_{username}")     


@app.route("/edit_tip_text_<tip_tag_id>")
def edit_tip_text(tip_tag_id):
    """Edits the tip_text for the given tip and redirects back to the profile"""

    new_tip_text = request.args.get("new-tip-text")
    tip_id = crud.get_tip_by_tip_tag(tip_tag_id=tip_tag_id).tip_id

    tip = crud.edit_tip_text(new_text=new_tip_text, tip_id=tip_id)

    username = session["logged_in_username"]

    return redirect(f"/profile_{username}")

#======================================================EDIT PROFILE ROUTES========================================================

@app.route("/edit_username")
def edit_user_account():
    """Changes user profile based upon user input in edit_profile form then redirects back to profile"""

    old_username = request.args.get("old-username")
    new_username = request.args.get("new-username")
    
    session["logged_in_username"] = new_username

    user = crud.change_user_username(old_username=old_username, new_username=new_username)

    return redirect(f"/profile_{user.username}")

@app.route("/edit_email")
def edit_user_email():
    """Changes user's email stored in database based on user input in edit_profile form, redirects to profile"""

    old_email = request.args.get("old-email")
    new_email = request.args.get("new-email")

    user = crud.change_user_email(new_email=new_email, old_email=old_email)

    return redirect(f"/profile_{user.username}")

@app.route("/edit_password_user_<user_id>", methods=["POST"])
def edit_user_password(user_id):
    """Changes user's password stored in database and redirects to their profile"""

    new_password = request.form.get("new-password")
    
    user_id = int(user_id)
    
    user = crud.change_user_password(user_id=user_id, new_password=new_password)

    return redirect(f"/profile_{user.username}")


#======================================================DELETE PROFILE ROUTES========================================================
@app.route("/delete_user_<user_id>")
def delete_user_account(user_id):
    """Deletes user, clears session, and redirects to homepage"""

    crud.delete_user(user_id)
    session.clear()
    return redirect("/")

#=================================================CREATE ACCOUNT ROUTE FUNCTIONS=================================================
@app.route("/create_account")
def show_create_account():
    """Renders the create_account page to allow a user to create a new account"""

    return render_template("create_account.html")

@app.route("/check_new_username_email")
def check_new_user_username_email():
    """Checks the database to verify if a username and/or email already exits"""

    input_username = request.args.get("input_username")
    input_email = request.args.get("input_email")
    username_user = crud.get_user_by_username(input_username)
    email_user = crud.get_user_by_email(input_email)
    
    if username_user == None and email_user == None:
        return "User does not exist"
    elif username_user != None and email_user != None:
        return "User exists"
    elif username_user == None and email_user != None:
        return "Email exists"
    elif username_user != None and email_user == None:
        return "Username exists"

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

    if session == {}:
        flash("Please log in first")
        return redirect("/login")

    page_one = crud.get_paginated_tip_tags()

    pages = crud.get_dict_of_tip_tag_pages(pagination_obj=page_one)

    tip_tag_pagination = crud.navigate_through_pages(pagination_obj=page_one, page_num=1)

    return render_template("new_tip.html", tip_tag_pages=pages, pagination_obj=tip_tag_pagination, page_num=1)


@app.route("/add_new_tip")
def add_new_tip():
    """Adds new tip to the database after they submit the add new tip form"""

    username = session["logged_in_username"]

    state_name= request.args.get("state").title()
    city_name= request.args.get("city").title()

    #If user leaves location inputs blank, add None value to database
    #so that, if later user filters by State and leave City blank, empty string
    #tips won't appear
    if state_name == "" and city_name == "":
        state_name = None
        city_name = None
    elif state_name == "":
        state_name = None
    elif city_name == "":
        city_name = None
    
    tip_text = request.args.get("tip-text")

    tag_name = request.args.get("tags")

    user = crud.get_user_by_username(username=username)

    new_tip = crud.create_tip(tip_text=tip_text, user_id=user.user_id)
    new_tag = crud.create_tag(tag_name=tag_name, tag_state=state_name, tag_city=city_name)
    new_tip_tag = crud.create_tip_tag(tag_id=new_tag.tag_id, tip_id=new_tip.tip_id)

    flash(f"Thank you for adding your tip about {city_name}, {state_name}")
    return redirect("/view_travel_tips_page_1")


#=================================================CREATE VACATION ROUTE FUNCTIONS===========================================
@app.route("/create_vacation")
def show_new_vacation():
    """Renders for that allows users to create a new vacation for their profile"""

    if session == {}:
        flash("Please log in first!")
        return redirect("/login")

    username = session["logged_in_username"]
    
    user = crud.get_user_by_username(username)

    pag_obj = crud.get_paginated_user_filtered_tip_tags(user_id=user.user_id)
    tip_tag_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=pag_obj)

    vacations = user.vacation

    return render_template("new_vacation.html", user=user, vacations=vacations, tip_tag_pages=tip_tag_pages,
    pagination_obj=pag_obj, page_num=1)


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


#=================================================SEARCH DESTINATION ROUTE FUNCTIONS==========================================
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
            # city_tags = crud.get_tags_by_tag_city(city=city)
            # city_tip_tags = crud.parse_through_tags(tags=city_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)

            city_pag_obj = crud.get_paginated_city_filtered_tip_tags(city=city)
            city_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=city_pag_obj)
            page_num = 1
            
            return render_template("destination_details.html", tip_tag_pages=city_pages, pagination_obj=city_pag_obj,page_num=page_num, 
            city=city, state=state, departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=event_names,
            event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,start_times=start_times, venues=venues)
        
        elif state_in_tags == True:
            state_tags = crud.get_tags_by_tag_state(state=state)
            state_tip_tags = crud.parse_through_tags(tags=state_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)

            state_pag_obj = crud.get_paginated_state_filtered_tip_tags(state=state)
            state_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=state_pag_obj)
            page_num = 1

            return render_template("destination_details.html", tip_tag_pages=state_pages, pagination_obj=state_pag_obj,page_num=page_num,
            city=city, state=state, departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=event_names, 
            event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,start_times=start_times, venues=venues)
        
        else:
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)
            return render_template("destination_details.html", tip_tag_pages=[], city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=event_names, 
            event_urls=event_urls, img_urls=img_urls, start_dates=start_dates,start_times=start_times, venues=venues)

    else:
        #If there are not events for the given search
        if city_in_tags == True:
            city_tags = crud.get_tags_by_tag_city(city=city)
            city_tip_tags = crud.parse_through_tags(tags=city_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)

            city_pag_obj = crud.get_paginated_city_filtered_tip_tags(city=city)
            city_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=city_pag_obj)
            page_num = 1
            
            return render_template("destination_details.html", tip_tag_pages=city_pages, pagination_obj=city_pag_obj,page_num=page_num, 
            city=city, state=state, departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=False)
        
        elif state_in_tags == True:
            state_tags = crud.get_tags_by_tag_state(state=state)
            state_tip_tags = crud.parse_through_tags(tags=state_tags)
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)

            state_pag_obj = crud.get_paginated_state_filtered_tip_tags(state=state)
            state_pages = crud.get_dict_of_tip_tag_pages(pagination_obj=state_pag_obj)
            page_num = 1

            return render_template("destination_details.html", tip_tag_pages=state_pages, pagination_obj=state_pag_obj,page_num=page_num, 
            city=city, state=state, departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=False)
        
        else:
            display_departure_date = crud.format_date_strings(departure_date)
            display_arrival_date = crud.format_date_strings(arrival_date)
            return render_template("destination_details.html", tip_tag_pages=[], city=city, state=state, 
            departure_date=display_departure_date, arrival_date=display_arrival_date, event_names=False)


#=================================================TO DO LIST ROUTE FUNCTIONS===========================================
@app.route("/travel_prep_checklist_vacation_<vacation_id>")
def show_travel_prep_checklist(vacation_id):
    """Renders the to-do-list template"""

    checklists = crud.get_vacation_checklists_by_vacation(vacation_id=vacation_id)

    todo_list_items = []
    clothes_list_items = []
    toiletries_list_items = []
    misc_list_items = []

    for checklist in checklists:
        if checklist.checklist_name == "todo items":
            todo_list_items.extend(checklist.checklist_item)
            todo_id = checklist.checklist_id
        elif (checklist.checklist_name == "clothes" or 
        checklist.checklist_name == "summer clothes" or checklist.checklist_name == "winter clothes"):
            clothes_list_items.extend(checklist.checklist_item)
            clothes_id = checklist.checklist_id
        elif checklist.checklist_name == "toiletries":
            toiletries_list_items.extend(checklist.checklist_item)
            toiletries_id = checklist.checklist_id
        elif checklist.checklist_name == "misc items":
            misc_list_items.extend(checklist.checklist_item)
            misc_id = checklist.checklist_id

    return render_template("to_do_list.html", todo_list_items=todo_list_items, todo_id=todo_id, clothes_list_items=clothes_list_items,
    clothes_id=clothes_id, toiletries_list_items=toiletries_list_items, toiletries_id=toiletries_id, misc_list_items=misc_list_items, misc_id=misc_id)

@app.route("/add_checklist_item")
def add_item_to_checklist():
    """Adds item to the given VacationChecklist"""

    item = request.args.get("item")
    checklist_id = request.args.get("checklist_id")
    new_item = crud.create_checklist_item(item=item, checklist_id=checklist_id)

    return f"{new_item.item_id}"

@app.route("/delete_checklist_item")
def delete_checklist_item():
    """Deletes checklist_item from the database when user clicks delete span"""

    item_id = request.args.get("item_id")
    crud.delete_checklist_item(item_id=item_id)
    
    return "Successfully deleted from db"

@app.route("/complete_checklist_item")
def complete_checklist_item():
    """Updates checklist_item completion status to True"""

    item_id = request.args.get("item_id")
    checklist_item = crud.complete_list_item(item_id=item_id)

    return f"Completed {checklist_item} status={checklist_item.completed}"


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)
    # model.connect_to_db(app)
    # model.db.create_all()