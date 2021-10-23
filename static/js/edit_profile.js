"use strict";

console.log("edit-profile.js connected");

//----------------- DELETE VACATION FUNCTION -----------------------------
const deleteVacation = (evt) => {
    evt.preventDefault();
    console.log('Prevent default on delete button is working');
    const vacationId = $('#profile-delete-vacation-btn').attr('name');
    const confirmation = confirm("Are you sure you'd like to delete this vacation? Action cannot be undone");
    if (confirmation === true){
        console.log("User chose to delete");
        evt.unbind() //---> i'm v hopeful this wil help, not sure
    }else{
        console.log("User chose NOT to delete");
    };
};

$('#profile-delete-vacation-btn').on('click', deleteVacation);

// ------------------ EDIT FUNCTIONS TO EDIT USER OBJECT ---------------------------
const showEditEmailForm = () => {
    $('#edit-email-paragraph').html(`
    <form id="edit-user-email" action="/edit_email">
    <div id="edit-user-email">
        <label><strong>Update Email:</strong></label><p></p>
        <label>Old email address: </label><input type="email" name="old-email">
        <label>New email address:</label>
        <input type="email" name="new-email">
        <input type="submit" id="change-email-submit">
    </div>
    </form>
    <p></p>
    `);
    // Regex pattern not working (pattern below) currently saying all email inputs are invalid (but title is not msg appearing)
    // pattern="\w*\@\w*\.\w{3}" title="Please enter a valid email address"
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
    $('#edit-password-paragraph').html(`
    <form id="edit-user-password" action="/edit_password_user_{{user.user_id}}" method="POST">
    <div id="edit-user-password">
        <label><strong>Change Password:</strong></label><p></p>
        <label>Old Password:</label>
        <input type="password" name="old-password">
        <label>New Password:</label>
        <input type="password" name="new-password">
        <input type="submit" id="change-password-submit">
    </div>
    </form>
    `);
}

$('#edit-email-button').on('click', showEditEmailForm);
$('#edit-username-button').on('click', showEditUsernameForm);
$('#edit-password-button').on('click', showEditPasswordForm);


//------------------------ EDIT FUNCTIONS TO EDIT VACATION_LABEL OBJECT -------------------
const showEditVacationLabelForm = (evt) => {
    evt.preventDefault();
}

$('#profile-edit-vacation-btn').on('click', showEditVacationLabelForm);