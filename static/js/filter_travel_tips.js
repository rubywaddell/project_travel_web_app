"use strict";

console.log('connected to js');

const filterTipsByTags = (evt) => {
    evt.preventDefault();
    alert("Prevent default is working");

    const tag_val = $('input[name="filter-tags"]:checked').val();
    console.log(tag_val)
};


const showLocationFilteredTips = (evt) => {

    evt.preventDefault();
    // alert("Prevent default is working")
    
    const url = '/view_travel_tips/filtered_by_location.json';
    const formData = {state: $('#travel-tips-filter-state-input').val(), city: $('#travel-tips-filter-city-input').val()};

    const state = $('#travel-tips-filter-state-input').val();
    const city = $('#travel-tips-filter-city-input').val();

    $.get(url, formData, response => {
        $('#travel-tips-filter-div').html('')
        if (response === ""){
            $('#view-travel-tips-table-div').html(`<h2>Sorry, there are no tips for ${city} or ${state} yet.</h2>
                <h4>You can add one <a href="/add_new_tip">here</a></h4>`)
        }else{
            $('#travel-tips-header').html(`<h2>Tips for ${state}`)
            for (const i in response){
            $('#view-travel-tips-table-div').html(`
                <div>
                <p></p>
                <p>
                    ${response["tag_name"]}
                    ${response["tag_state"]}
                    ${response["tag_city"]}
                    ${response["tip_text"]}
                </p>
                </div>`
            )}
    }});
}

$('#tags-filter-submit').on('click', filterTipsByTags);
$('#city-state-filter-submit').on('click', showLocationFilteredTips);