"use strict";

console.log('connected to js');

const showTagFilteredTips = (evt) => {
    evt.preventDefault();
    // alert("Prevent default is working");

    const tag_val = $('input[name="filter-tags"]:checked').val();
    console.log(tag_val)

    const url = '/view_travel_tips/filtered_by_tag.json';
    const formData = {tag_name: tag_val};

    $.get(url, formData, response => {
        console.log(response);
        $('#travel-tips-header').html(`<h2>Travel Tips About ${tag_val}</h2>`);
        $('#travel-tips-filter-div').html('');

        if (response === ""){
            $('#view-travel-tips-table-div').html(`
            <h2>Sorry, there are no tips about ${tag_val} yet.</h2>
            <p>You can add one <a href="/create_tip">here</a></p>`);
        }else{
            $('#view-travel-tips-table-div').html(`
            <div class="grid-container">
                <div class="grid-item"><h4>State: </h4></div>
                <div class="grid-item"><h4>City: </h4></div>
                <div class="grid-item"><h4>Tip: </h4></div>
            </div>
            `)
            for (let i in response){
                $('#view-filtered-tips-div').append(`
                <div class="grid-container">
                    <div class="grid-item">${response[i]["tag_state"]}</div>
                    <div class="grid-item">${response[i]["tag_city"]}</div>
                    <div class="grid-item">${response[i]["tip_text"]}</div>
                </div>
                `);
            };
        };
    });
};


const showLocationFilteredTips = (evt) => {
    
    evt.preventDefault();
    // alert("Prevent default is working")
    
    const url = '/view_travel_tips/filtered_by_location.json';
    const formData = {state: $('#travel-tips-filter-state-input').val(), city: $('#travel-tips-filter-city-input').val()};

    const state = $('#travel-tips-filter-state-input').val();
    const city = $('#travel-tips-filter-city-input').val();

    $('#travel-tips-header').html(`<h2>Travel Tips About ${city}, ${state}</h2>`);

    $.get(url, formData, response => {
        $('#travel-tips-filter-div').html('')
        console.log(response)
        if (response === ""){
            $('#view-travel-tips-table-div').html(`<h2>Sorry, there are no tips for ${city} or ${state} yet.</h2>
                <h4>You can add one <a href="/create_tip">here</a></h4>`)
        }else{
            $('#travel-tips-header').html(`<h2>Tips for ${state}`)
            $('#view-travel-tips-table-div').html(`
            <div class="grid-container-four-columns">
                <div class="grid-item"><h4>Tag: </h4></div>
                <div class="grid-item"><h4>State: </h4></div>
                <div class="grid-item"><h4>City: </h4></div>
                <div class="grid-item"><h4>Tip: </h4></div>
            </div>
            `);
            for (let i in response){
                console.log(response[i])
            $('#view-filtered-tips-div').append(`
                <div class="grid-container-four-columns">
                    <div class="grid-item">${response[i]["tag_name"]}</div>
                    <div class="grid-item">${response[i]["tag_state"]}</div>
                    <div class="grid-item">${response[i]["tag_city"]}</div>
                    <div class="grid-item">${response[i]["tip_text"]}</div>
                </div>
            `)};
    }});
};

$('#tags-filter-submit').on('click', showTagFilteredTips);
$('#city-state-filter-submit').on('click', showLocationFilteredTips);