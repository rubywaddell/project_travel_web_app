"use strict";
// alert("JS file connected");

const checkNewUserInputsInDb = (evt) => {
    evt.preventDefault();
    // alert('you clicked the form submit');
    const inputUsername = $('#new-user-username-input').val();
    console.log(inputUsername);
    const inputEmail = $('#new-user-email-input').val();
    console.log(inputEmail);

    const formData = {"input_username" : inputUsername, "input_email" : inputEmail};

    $.get('/check_new_username_email', formData, response => {
        console.log(response);
        // possible responses: 'user does not exist', 'user exists', 'email exists', 'username exists'
        if (response === "User does not exist"){
            $('#new-user-form-submit').unbind('click');
        }else if (response === "User exists"){
            $('#new-user-password').append(`
            <p>Account already exists, please <a href="/login">log in</a></p>`);
        }else if (response === "Email exists"){
            $('#new-user-password').append(`
            <p>Account already exists, please <a href="/login">log in</a></p>`);
        }else if (response === "Username exists"){
            $('#new-user-username').append(`
            <p>Username ${inputUsername} taken, please choose a new one</p>`);
    };
    
})};

$('#new-user-form-submit').bind('click', checkNewUserInputsInDb);