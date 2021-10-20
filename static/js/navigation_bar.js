"use strict";

$.get("/check_session", response => {
    if (response === "False"){
        console.log("Not logged in");
    }else{
        console.log("Logged in")
        $('#login-link').html(`<li id="logout-link"><a href="/logout">Log Out</a></li>`);
        $('#create-account-link').html(`<li id="view-profile-link"><a href="/profile_${response}">Profile</a></li>`);
        $('#navigation-links-list').append(`
        <li id="add-tip-link"><a href="/create_tip">Add a New Travel Tip</a></li>
        <li id="add-vacation-link"><a href="/create_vacation">Add a New Vacation to Profile</a></li>`);
    }
});