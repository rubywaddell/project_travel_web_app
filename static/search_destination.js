"use strict";

const showCities = (evt) => {
    evt.preventDefault();

    console.log($('#states-dropdown').value)
    
};

$('#search-destination-form').on('submit',() =>{
    showCities();
});