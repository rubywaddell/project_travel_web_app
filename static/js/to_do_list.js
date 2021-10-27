"use strict";

// Prep list functions
const addPrepListItem = () => {
    const newItem = $('#add-new-prep-list-item').val()
    
    $('#travel-prep-list-ul').append(`<li>${newItem}</li>`);
}

$('#prep-list-add-item-btn').on('click', addPrepListItem);

// Clothing packing list functions
const addClothesListItem = () => {
    const newItem = $('#add-new-clothes-list-item').val()
    
    $('#clothes-bag-list-ul').append(`<li>${newItem}</li>`);
}

$('#clothes-list-add-item-btn').on('click', addClothesListItem);

// Toiletries packing list functions
const addToiletriesListItem = () => {
    alert('You sure clicked that button');
}

$('#toiletries-list-add-item-btn').on('click', addToiletriesListItem);

// Misc. packing lsit functions
const addMiscListItem = () => {
    alert('You sure clicked that button');
}

$('#misc-list-add-item-btn').on('click', addMiscListItem)