"use strict";

console.log("edit-profile.js connected");

const showEditEmailForm = () => {
    alert('showEmailForm function on click is working');
}

const showEditUsernameForm = () => {
    alert('showEditUsernameForm function on click is working');
}

const showEditPasswordForm = () => {
    alert('showEditPasswordForm function on click is working');
}

$('#edit-email-button').on('click', showEditEmailForm);
$('#edit-username-button').on('click', showEditUsernameForm);
$('#edit-password-button').on('click', showEditPasswordForm);