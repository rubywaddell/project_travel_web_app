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