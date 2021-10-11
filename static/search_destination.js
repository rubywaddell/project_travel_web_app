"use strict";

const showCities = (evt) => {
    evt.preventDefault();
    // alert("Prevent default is working")

    const url = '/search_destination/cities.json';
    const formData = {state : $('#states-dropdown').val()};
    // alert(`FormData.state looks like this:\n${formData.state}`)

    $.get(url, formData, response => {
        console.log(response)
        $('#cities-dropdown').html('<option value="choose-city">~Select a City~</option>')
        for (const city_id in response){
            console.log(response[city_id])
            $('#cities-dropdown').append(`<option value="${response[city_id]}">${response[city_id]}</option>`)
        }
    });  
};

$('#submit-state-btn').on('click', showCities);