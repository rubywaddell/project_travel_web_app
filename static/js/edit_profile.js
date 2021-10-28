"use strict";

//------------------------------------------------- DELETE PROFILE FUNCTION -------------------------------------------------
const deleteUserAccount = (evt) =>{

    const userId = evt.target.name;
    
    const confirmation = confirm("Are you sure you'd like to delete your account?\nAll data will be deleted forever");
    if (confirmation == true){
        console.log(true);
        $.get(`/delete_user_${userId}`, response => {
            window.open("/", "_self");
        });
    };
};

$('#delete-account-button').on('click', deleteUserAccount);

//-------------------------------------------- DELETE VACATION FUNCTION -------------------------------------------------
const deleteVacation = (evt) => {

    const vacationId = evt.target.id;

    const confirmation = confirm("Are you sure you'd like to delete this vacation?\nAction cannot be undone");
    if (confirmation === true){
        $('#profile-vacations-for-loop-container').html('');

        $.get(`/delete_vacation_${vacationId}`, response => {
            const username = response;
            location.reload();
        });
    }else{
        console.log("User chose NOT to delete");
    };
};

$('.delete-vacay-btn').on('click', deleteVacation);

// --------------------------------------------- EDIT FUNCTIONS TO EDIT USER OBJECT ----------------------------------------------
const emailPattern = /\w*\@\w*\.\w{3}/

const showEditEmailForm = () => {
    $('#profile-user-contact-info-grid-container').append(`
    <form id="edit-user-email" action="/edit_email">
    <div id="edit-user-email">
        <label><strong>Update Email:</strong></label><p></p>
        <label>Old email address: </label>
        <input type="email" name="old-email">
        <label>New email address: </label>
        <input type="email" name="new-email" pattern=${emailPattern} title="Please enter a valid email address">
        <input type="submit" id="change-email-submit">
    </div>
    </form>
    <p></p>
    `);
}

const showEditUsernameForm = () => {
    $('#profile-user-contact-info-grid-container').append(`
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
    $('#profile-user-contact-info-grid-container').append(`
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


//------------------------------------------ EDIT FUNCTIONS TO EDIT VACATION_LABEL OBJECT -----------------------------------------
const showEditVacationLabelForm = (evt) => {
    
    console.log(evt.target.id);
    const vacationId = evt.target.id
    $('#profile-vacations-for-loop-container').append(`
    <strong>Enter new vacation information here:</strong>
    <form action="/edit_vacation_dates_id_${vacationId}">
    <div id="edit-vacation-dates">
        <label>From:</label>
        <input type="date" id="new-departure-date" name="departure-date">
        <label>To:</label>
        <input type="date" id="new-arrival-date" name="arrival-date">
        <input type="submit">
    </div>
    </form>

    <form action="/edit_vacation_location_id_${vacationId}">
    <div id="edit-vacation-location">
        <label>Please enter the city and state</label>
        <label>State:</label><input type="text" name="state">
        <label>City:</label><input type="text" name="city">
    <input type="submit">    
    </div>
    </form>
    <p></p>
    `);
};

$('.edit-vacation-btn').on('click', showEditVacationLabelForm);

