"use strict";

console.log('connected to js');

const showTagFilteredTips = (evt) => {
    evt.preventDefault();
    alert("Prevent default is working");

    const tag_val = $('input[name="filter-tags"]:checked').val();
    console.log(tag_val)

    const url = '/view_travel_tips/filtered_by_tag.json';
    const formData = {tag_name: tag_val};

    $.get(url, formData, response => {
        console.log(response)
    })

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
                <div class="grid-container">
                    <div class="grid-item">${response["tag_name"]}</div>
                    <div class="grid-item">${response["tag_state"]}</div>
                    <div class="grid-item">${response["tag_city"]}</div>
                    <div class="grid-item">${response["tip_text"]}</div>
                </div>
            `)}
    }});
}

$('#tags-filter-submit').on('click', showTagFilteredTips);
$('#city-state-filter-submit').on('click', showLocationFilteredTips);