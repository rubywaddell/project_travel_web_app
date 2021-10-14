"use strict";

// const showCities = (evt) => {
//     evt.preventDefault();
//     // alert("Prevent default is working")

//     const url = '/search_destination/cities.json';
//     const formData = {state : $('#states-dropdown').val()};

//     $.get(url, formData, response => {
//         $('#cities-dropdown').html('<option value="choose-city">~Select a City~</option>')
//         for (const city_id in response){
//             $('#cities-dropdown').append(`<option value="${response[city_id]}">${response[city_id]}</option>`)
//         }
//     });  
// };

const enableSubmissionButton = (evt) => {
    $('#submit-form-button-div').html('<button class="btn btn-primary" type="submit" id="submit-state-city-btn" enabled>View Travel Tips and Events</button>')
}

$('#submit-state-btn').on('click', showCities);
$('#search-destination-arrival-date').on('click', enableSubmissionButton)
// Need to find a better method of enabling button - should prevent user from submitting until all form inputs are completed
// Right now, they could click on arrival date first, then hit submit