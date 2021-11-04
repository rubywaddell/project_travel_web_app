# TravelWise
---
Learn more about the developer: https://www.linkedin.com/in/rubywaddell/

## INTRO:
TravelWise is a full-stack web-app dedicated to helping people travel throughout the United States in a safe and fun way. The developer, Ruby Waddell, is an avid travller herself who, though she enjoys taking trips alone, sometimes struggles with keeping track of planned trips and finding insider tips about how to stay safe and where to go. TravelWise is intended to help users stay safe while travelling by accessing fellow users' travel tips. It is also intended to help people have fun and learn about what events are happening while they are on vacation by showing users events requested from the TicketMaster Discovery API. 

## Technologies Used:
- Python
- Flask
- PostreSQL
- Jinja2
- HTML
- JavaScript
- jQuery
- AJAX
- CSS
- Bootstrap
- TicketMaster Discovery API
- Regex

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