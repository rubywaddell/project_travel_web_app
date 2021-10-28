"use strict";

// Prep list functions
const addPrepListItem = (evt) => {
    const newItem = $('#add-new-prep-list-item').val()
    const listId = evt.target.name;
    console.log(listId);
    $('#travel-prep-list-ul').append(`<li>${newItem}</li>`);
}

$('#prep-list-add-item-btn').on('click', addPrepListItem);

// Clothing packing list functions
const addClothesListItem = (evt) => {
    const newItem = $('#add-new-clothes-list-item').val()
    const listId = evt.target.name;
    console.log(listId);
    $('#clothes-bag-list-ul').append(`<li>${newItem}</li>`);
}

$('#clothes-list-add-item-btn').on('click', addClothesListItem);

// Toiletries packing list functions
const addToiletriesListItem = (evt) => {
    const newItem = $('#add-new-toiletries-list-item').val()
    const listId = evt.target.name;
    console.log(listId);
    $('#toiletries-bag-list-ul').append(`<li>${newItem}</li>`);
}

$('#toiletries-list-add-item-btn').on('click', addToiletriesListItem);

// Misc. packing lsit functions
const addMiscListItem = (evt) => {
    const newItem = $('#add-new-misc-list-item').val()
    const listId = evt.target.name;
    console.log(listId);
    $('#misc-bag-list-ul').append(`<li>${newItem}</li>`);
}

$('#misc-list-add-item-btn').on('click', addMiscListItem);