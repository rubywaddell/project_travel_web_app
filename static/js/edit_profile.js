"use strict";

console.log("edit-profile.js connected");

const showEditEmailForm = () => {
    $('#edit-email-paragraph').html(`
    <form id="edit-user-email" action="/edit_email">
    <div id="edit-user-email">
        <label><strong>Update Email:</strong></label><p></p>
        <label>Old email address: </label><input type="email" name="old-email">
        <label>New email address:</label>
        <input type="email" name="new-email" pattern="\w*\@\w*\.\w{3}" title="Please enter a valid email address">
        <input type="submit" id="change-email-submit">
    </div>
    </form>
    <p></p>
    `);
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