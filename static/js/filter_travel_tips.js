"use strict";
console.log('connected to js')

const filterTips = (evt) => {
    evt.preventDefault();
    // alert("Prevent default is working")

    const tag_val = $('input[name="filter-tags"]:checked').val()

    if (tag_val === 'location'){
        console.log(true)
        $('#travel-tips-filter-tags').html(`<label>Select the Location You'd Like to Filter:</label><p></p>
                    <label for="state">State: </label>
                    <input id="search-destination-state-input" type="text" name="state">
                    <label for="city"> City: </label>
                    <input id="search-destination-city-input" type="text" name="city">`)
    }
};


$('#travel-tips-filter-submit').on('click', filterTips);
