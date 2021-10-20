"use strict";

// ************************* Functions for Tip Filtering: ************************************
const showTagFilteredTips = (evt) => {
    evt.preventDefault();

    const tag_val = $('input[name="filter-tags"]:checked').val();
    console.log(tag_val)

    const url = '/view_travel_tips/filtered_by_tag.json';
    const formData = {tag_name: tag_val};

    $.get(url, formData, response => {
        
        $('#travel-tips-header').html(`<h2>Travel Tips About ${tag_val}</h2>`);
        $('#travel-tips-filter-div').html('');
        $('#view-travel-tips-tip-data-div').html('');

        if (response === ""){
            $('#view-tips-div').html(`
            <h2>Sorry, there are no tips about ${tag_val} yet.</h2>
            <p>You can add one <a href="/create_tip">here</a></p>`);
        }else{
            $('#view-travel-tips-headers').html(`
            <div class="grid-container">
                <div class="grid-item"><h4>State: </h4></div>
                <div class="grid-item"><h4>City: </h4></div>
                <div class="grid-item"><h4>Tip: </h4></div>
            </div>
            `)
            for (let i in response){
                $('#view-travel-tips-tip-data-div').append(`
                <div class="grid-container">
                    <div class="grid-item">${response[i]["tag_state"]}</div>
                    <div class="grid-item">${response[i]["tag_city"]}</div>
                    <div class="grid-item">${response[i]["tip_text"]}</div>
                </div>
                `)}};
    });
};


const showLocationFilteredTips = (evt) => {
    
    evt.preventDefault();
    
    const url = '/view_travel_tips/filtered_by_location.json';
    const formData = {state: $('#travel-tips-filter-state-input').val(), city: $('#travel-tips-filter-city-input').val()};

    const state = $('#travel-tips-filter-state-input').val();
    const city = $('#travel-tips-filter-city-input').val();

    $('#travel-tips-header').html(`<h2>Travel Tips About ${city}, ${state}</h2>`);

    $.get(url, formData, response => {
        $('#travel-tips-filter-div').html('')
        console.log(response)
        if (response === ""){
            $('#view-tips-div').html(`<h2>Sorry, there are no tips for ${city} or ${state} yet.</h2>
                <h4>You can add one <a href="/create_tip">here</a></h4>`)
        }else{
            $('#travel-tips-header').html(`<h2>Tips for ${state}`)
            $('#view-travel-tips-tip-data-div').html('');
            for (let i in response){
            $('#view-travel-tips-tip-data-div').append(`
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


// ************************* Functions for Pagination: ************************************

let page_num = 1;

const showNextPageTips = () => {
    
    page_num += 1;

    $.get("/page_results", response => {
        
        const current_page = response[page_num];
        $('#view-travel-tips-tip-data-div').html('');
        for (const tip in current_page){
            $('#view-travel-tips-tip-data-div').append(`
                <div class="grid-container-four-columns">
                    <div class="grid-item">${current_page[tip]["tag_name"]}</div>
                    <div class="grid-item">${current_page[tip]["tag_state"]}</div>
                    <div class="grid-item">${current_page[tip]["tag_city"]}</div>
                    <div class="grid-item">${current_page[tip]["tip_text"]}</div>
                </div>
            `);
        };
    });
};

$('#view-tips-next-page-btn').on('click', showNextPageTips);