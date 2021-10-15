"use strict";
console.log('connected to js')

const filterTipsByTags = (evt) => {
    evt.preventDefault();
    alert("Prevent default is working")
    const tag_val = $('input[name="filter-tags"]:checked').val();

    console.log(tag_val)
};


const showLocationFilteredTips = (evt) => {

    evt.preventDefault();

    alert("Prevent default is working")
    
    const url = '/view_travel_tips/filtered_by_location.json';
    const formData = {state: $('#travel-tips-filter-state-input').val(), city: $('#travel-tips-filter-city-input').val()};

    $.get(url, formData, response => {
        console.log(response);
    });
};


// const filterByTagNames = (tag_val) => {
//     console.log(tag_val);
// }

$('#tags-filter-submit').on('click', filterTipsByTags);
$('#city-state-filter-submit').on('click', showLocationFilteredTips);