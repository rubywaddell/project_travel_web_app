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
    $('#edit-username-paragraph').html(`
    <div id="edit-user-username">
    <form id="edit-user-username" action="/edit_username">
        <label><strong>Change Your Username:</strong></label>
        <p></p>
        <label>Old username:</label>
        <input type="text" name="old-username">
        <label>New username:</label>
        <input type="text" name="new-username" pattern="\w{1, 15}" title="Username too long, please limit to 15 characters">
        <input type="submit" id="change-username-submit">
    </div>
    </form>
    `);
}

const showEditPasswordForm = () => {
    alert('showEditPasswordForm function on click is working');
}

$('#edit-email-button').on('click', showEditEmailForm);
$('#edit-username-button').on('click', showEditUsernameForm);
$('#edit-password-button').on('click', showEditPasswordForm);