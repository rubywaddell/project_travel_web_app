# TravelWise
---
Learn more about the developer: https://www.linkedin.com/in/rubywaddell/

You can visit the app at http://54.70.84.63 or follow the installations below to run locally on your own computer.

## INTRO:
TravelWise is a full-stack web-app dedicated to helping people travel throughout the United States in a safe and fun way. The developer, Ruby Waddell, is an avid traveller herself who, though she enjoys taking trips alone, struggled with keeping track of planned trips and finding insider tips about how to stay safe and where to go. TravelWise is intended to help users solve these problems by allowing them to create a profile where they can save planned vacations, view and write tips about any domestic destination, and view events requested from the TicketMaster Discovery API scheduled during their dates of travel. 
TravelWise is intended to help users stay safe while travelling by accessing fellow users' travel tips. It is also intended to help people have fun and learn about what events are happening while they are on vacation by showing users events requested from the TicketMaster Discovery API. 

## Technologies Used:
- Python
- Flask
- PostreSQL
- Flask-SQLAlchemy
- Jinja2
- HTML
- JavaScript
- jQuery
- AJAX
- CSS
- Bootstrap
- TicketMaster Discovery API
- Regex

## How To Run Locally:
1. Click "clone" and copy the link that appears
2. In your terminal, type the command `git clone` and paste the link
3. Once cloned, create a virtual environment using the command `virtualenv env`
4. Activate your virtual environment `source env/bin/activate`
5. Install the requirements by running `pip3 install -r requirements.txt`
6. Make sure you have the necessary database by running `createdb travel_app`
7. Seed the database by running `python3 seed_database.py`
8. Run the server with `python3 server.py`
9. Then, access the app on your browser by going to localhost:5000
10. You're ready to create an account and explore the app!

## Features:
#### View Travel Tips:
Users can view a list of tips that have been created by other users pertaining to any domestic location and tagged with information such as "LGBT+", "money/theft", "solo-travel", and more. Users can then filter the search results by tag or by location, if they choose.
Users can add travel tips if they are logged into their account. They can make edits to tips that they have written, and can view all the tips they have written from their profile page.

#### Search Destination:
Users can search a destination to view travel tips and events for that destination and the dates searched. 
The events displayed are the result of a GET request made to the TicketMaster Discovery API upon submission of the destination search. 
The travel tips displayed are retrieved from the database and filtered by the location that the user searched.
Users do not need to be logged in or have an account to use this feature.

#### Save a Vacation to Profile:
Users can create an account and save planned vacations to their profile.  The vacations are stored in the database and displayed on the user's profile page. On the profile, users can also see the events scheduled during their dates of travel at the planned destination. 
Users can also access a to-do list for each vacation which they can add items to, delete items from, and check items off of. Each time a new vacation is created these checklists are created as well, if the vacation is planned during the winter months the packing list will include winter-wear and, if during the summer, will include summer clothes. 
Users can make edits to the vacations on their profile and they can delete a vacation off of their profile.

## Coming Soon:
- Integrating the Google Calendar API to allow users to set deadlines for items on their checklists
- Integrating the Kayak API search widget to allow users to search for flights
- Adding a like/vote feature to allow users to upvote travel tips they found useful
- Adding tags to vacations (such as method of travel) that will then filter and display travel tips relating to those tags
- Expanding all features to allow for international destinations and event queries.
- Once expanded internationally, also integrating the TravelBrief API to show users country-specifc information about visa requirements, travel regulations, health and vaccines, etc.