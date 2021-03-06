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
    };
};

$('.delete-vacay-btn').on('click', deleteVacation);


// --------------------------------------------- EDIT FUNCTIONS TO EDIT USER OBJECT ----------------------------------------------

const showEditEmailForm = (evt) => {
    const emailPattern = /\w*\@\w*\.\w{3}/
    const oldEmail = evt.target.name;
    $('#profile-user-contact-info-grid-container').append(`
    <form id="edit-user-email" action="/edit_email">
    <div id="edit-user-email">
        <label><strong>Update Email:</strong></label><p></p>
        <label>Old email address: </label>
        <input type="email" name="old-email" value=${oldEmail}>
        <label>New email address: </label>
        <input type="email" name="new-email" pattern=${emailPattern} title="Please enter a valid email address">
        <input type="submit" id="change-email-submit">
    </div>
    </form>
    <p></p>
    `);
}

const showEditUsernameForm = (evt) => {
    const oldUsername = evt.target.name;
    $('#profile-user-contact-info-grid-container').append(`
    <div id="edit-user-username">
    <form id="edit-user-username" action="/edit_username">
        <label><strong>Change Your Username:</strong></label>
        <p></p>
        <label>Old username:</label>
        <input type="text" name="old-username" value=${oldUsername}>
        <label>New username:</label>
        <input type="text" name="new-username" pattern="\w{1, 15}" title="Username too long, please limit to 15 characters">
        <input type="submit" id="change-username-submit">
    </div>
    </form>
    `);
}

const showEditPasswordForm = (evt) => {
    const oldPassword = evt.target.name;
    const userId = $('.edit-password-div')[0]['id']
    console.log(oldPassword);
    console.log(userId);
    $('#profile-user-contact-info-grid-container').append(`
    <form id="edit-user-password" action="/edit_password_user_${userId}" method="POST">
    <div id="edit-user-password">
        <label><strong>Change Password:</strong></label><p></p>
        <label>Old Password:</label>
        <input type="password" name="old-password" id="old-password-input">
        <label>New Password:</label>
        <input type="password" name="new-password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
        title="Password must be 8 characters, contain one number, and one uppercase letter.">
        <input type="submit" id="change-password-submit">
    </div>
    </form>
    `);
    const validatePassword = (evt) => {
        evt.preventDefault();
        const inputPassword = $('#old-password-input').val();
        if (oldPassword !== inputPassword){
            alert('Incorrect password, please re-enter');
        }else{
            $('#change-password-submit').unbind('click');
        }
    }
    $('#change-password-submit').bind('click', validatePassword);
}

$('#edit-email-button').on('click', showEditEmailForm);
$('#edit-username-button').on('click', showEditUsernameForm);
$('#edit-password-button').on('click', showEditPasswordForm);


//------------------------------------------ EDIT FUNCTIONS TO EDIT VACATION_LABEL OBJECT -----------------------------------------
const showEditVacationLabelForm = (evt) => {
    
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

//------------------------------------------ EDIT FUNCTIONS TO EDIT USER TIP AND/OR TAG OBJECT -----------------------------------------

const showEditUserTipTagFrom = () => {
    const userTipDiv = $('.edit-user-tip-div');
    console.log(userTipDiv);
    // const tipId = $('.edit-user-tip-div').name();
    const tipTagId = userTipDiv[0]['id'];
    console.log(tipTagId);
    $('#view-travel-tips-tip-data-div').append(`
    <h3>New Tip Information:</h3>
    <form action="/edit_tag_name_${tipTagId}">
    <div id="new-tag">
        <label>Select tags:</label>
        <input type="radio" name="tags" id="money-tag" value="money"><label>Money/Theft</label>
        <input type="radio" name="tags" id="food-tag" value="food"><label>Food</label>
        <input type="radio" name="tags" id="health-tag" value="health"><label>Health</label>
        <input type="radio" name="tags" id="lgbt-tag" value="lgbt"><label>LGBTQIA+</label>
        <input type="radio" name="tags" id="solo-travel-tag" value="solo-travel"><label>Solo Travel</label>
        <input type="radio" name="tags" id="roadtrip-tag" value="roadtrips"><label>Roadtrip</label>
        <input type="radio" name="tags" id="hiking-tag" value="hiking"><label>Hiking/Backpacking</label>
        <input type="radio" name="tags" id="camping-tag" value="camping"><label>Camping</label>
        <input type="radio" name="tags" id="other-tag" value="other"><label>Other</label>
        <input type="submit">
    </div>
    </form>
    <p></p>
    <form action="/edit_tip_text_${tipTagId}">
    <div id="new-tip-text">
        <label>Enter your tip here:</label>
        <textarea name="new-tip-text"></textarea>
        <input type="submit">
    </div>
    </form>
    `);
};

$('#edit-user-tip-btn').on('click', showEditUserTipTagFrom);