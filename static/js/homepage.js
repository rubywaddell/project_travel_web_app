"use strict";

$.get("/check_session", response => {
    if (response === "False"){
        console.log("Not logged in");
    }else{
        console.log("Logged in");
        $('#homepage-account-paragraph').html(`
        View your profile to add tips, add new trips, and plan for your 
        trips with our personalizable packing lists
            <button class="btn btn-outline-primary"><a id="homepage-profile-link" 
                href="/profile_${response}">View Profile</a>
            </button>
                    
        `);
    }
});