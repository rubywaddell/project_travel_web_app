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