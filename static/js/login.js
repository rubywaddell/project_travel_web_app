"use strict";

console.log('Connected to JS file');

const checkPassword = (evt) => {
    evt.preventDefault();
    // alert('Prevent default is working');
    const username = $('#login-username-input').val();
    const password = $('#login-password-input').val();
    // console.log(username);
    // console.log(password);
    const formData = {username: username, password: password};
    console.log(formData)
    $.post('/login', formData, response => {
        console.log(response)
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