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
                <p><button href='/create_account' class='btn btn-primary'>Create Account</button></p>`
                );

        }else if (response === "Incorrect password"){
            $('#login-msg-div').text('Incorrect password, please try again');
        }
    });
};

$('#login-submit-input').on('click', checkPassword);