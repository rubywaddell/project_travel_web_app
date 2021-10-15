"use strict";
console.log('connected to js')

const filterTips = (evt) => {
    evt.preventDefault();
    // alert("Prevent default is working")
    const tag_val = $('input[name="filter-tags"]:checked').val();

    if (tag_val === 'location'){
        addCityStateInputs()
    }else{
        console.log(tag_val)
    };
};

const addCityStateInputs = () => {
    $('#travel-tips-filter-div').html(
        `<form action="/view_travel_tips/filtered_by_location">
        <label>Select the Location You'd Like to Filter For:</label><p></p>
        <label for="state">State: </label>
        <input id="search-destination-state-input" type="text" name="state">
        <label for="city"> City: </label>
        <input id="search-destination-city-input" type="text" name="city">
        <input id="city-state-filter-submit" type="submit"></form>`
    );
};

const filterCityState = (evt) => {
    evt.preventDefault()
    alert('Prevent default is working')
}


$('#travel-tips-filter-submit').on('click', filterTips);
$('#city-state-filter-submit').on('click', filterCityState);