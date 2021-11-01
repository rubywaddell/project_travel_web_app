"use strict";

alert("JS connected, congrats!");

$.get("/check_session", response => {
    if (response === "False"){
        console.log("Not logged in");
    }else{
        console.log("Logged in");
    //     $('#login-link').html(`<li class="nav-item" id="logout-link"><a class="nav-link" href="/logout">Log Out</a></li>`);
    //     $('#create-account-link').html(`<li class="nav-item" id="view-profile-link">
    //         <a class="nav-link" href="/profile_${response}">Profile</a></li>`);
    //     $('#navbar-links-list').append(`
    //     <li class="nav-item" id="add-tip-link"><a class="nav-link" href="/create_tip">Add a New Travel Tip</a></li>
    //     <li class="nav-item" id="add-vacation-link"><a class="nav-link" href="/create_vacation">Add a New Vacation to Profile</a></li>`);
    }
});