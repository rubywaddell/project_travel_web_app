"use strict";

$.get("/check_session", response => {
    if (response === "False"){
        console.log("Not logged in");
    }else{
        // change homepage card from displaying create account info, to
        // display profile info and link to profile in button
        $('#homepage-account-paragraph').html(`
        View your profile to add tips, add new trips, and plan for your 
        trips with our personalizable packing lists
        `);
        $('#homepage-account-link').html(`
            <a id="homepage-profile-link" 
                href="/profile_${response}">View Profile</a>
        `)
        // change homepage button from link to log in, to link to log out
        $('#homepage-login-paragraph').html(`
            <button class="btn btn-primary">
                <a id="homepage-login-link" href="/logout">Log Out</a>
            </button>
        `);

    }
});

// ----------------------- FUNCTIONS FOR HOMEPAGE VIDEO -----------------------------
const homepageVideo = document.querySelector('.background-video video');

const scaleVideo = () => {
    const innerWidth = window.innerWidth;
    const innerHeight = window.innerHeight;

    console.log('innerWidth = ', innerWidth);
    console.log('window.innerWidth', window.innerWidth);

    if (innerWidth > innerHeight){
        homepageVideo.setAttribute('width', innerWidth);
        homepageVideo.setAttribute('height', '');
    }else{
        homepageVideo.setAttribute('width', '');
        homepageVideo.setAttribute('height', innerHeight);
    }

    // const videoHeight = getComputedStyle(homepageVideo).height;
    // document.querySelector('header').style.height = videoHeight;
}

window.onload = scaleVideo;

window.onresize = scaleVideo;