"use strict";

const showCities = (evt) => {
    evt.preventDefault();

    const url = '/search_destination/cities.json'
    const formData = {state : $('#states-dropdown').val()};

    $.get(url, formData, response => {
        alert('hi');
    });
    
};

$('#sumbit-state-btn').on('click', showCities);