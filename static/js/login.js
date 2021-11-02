"use strict";

const checkPassword = (evt) => {
    evt.preventDefault();

    const username = $('#login-username-input').val();
    const password = $('#login-password-input').val();

    const formData = {username: username, password: password};
    $.post('/login', formData, response => {
        if (response === "Username not recognized, please create an account"){
            $('#login-msg-div').html(
                `<p>Username not recognized, please check the spelling or create an account</p>
                <p><button type="button" class='btn btn-primary'><a href="/create_account">Create Account</a></button></p>`
                );

        }else if (response === "Incorrect password"){
            $('#login-msg-div').text('Incorrect password, please try again');
        }else{
            $('#login-submit-input').unbind("click")
        }
    });
};

$('#login-submit-input').bind('click', checkPassword);


// ----------------------- FUNCTIONS FOR LOGIN VIDEO -----------------------------
const loginVideo = document.querySelector('.login-background-video video');

const scaleVideo = () => {
    const innerWidth = window.innerWidth;
    const innerHeight = window.innerHeight;

    console.log('innerWidth = ', innerWidth);
    console.log('window.innerWidth', window.innerWidth);

    if (innerWidth > innerHeight){
        loginVideo.setAttribute('width', innerWidth);
        loginVideo.setAttribute('height', '');
    }else{
        loginVideo.setAttribute('width', '');
        loginVideo.setAttribute('height', innerHeight);
    }

    const videoHeight = getComputedStyle(loginVideo).height;
    document.querySelector('header').style.height = videoHeight;
}

window.onload = scaleVideo;

window.onresize = scaleVideo;