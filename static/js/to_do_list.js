"use strict";

// Prep list functions
const addPrepListItem = (evt) => {
    const newItem = $('#add-new-prep-list-item').val()
    const listId = evt.target.name;

    const formData = {"item" : newItem, "checklist_id" : listId};
    console.log(formData);

    $.get("/add_checklist_item", formData, response => {
        console.log(response)
    });

    $('#travel-prep-list-ul').append(`<li>${newItem}</li>`);
}

$('#prep-list-add-item-btn').on('click', addPrepListItem);

// Clothing packing list functions
const addClothesListItem = (evt) => {
    const newItem = $('#add-new-clothes-list-item').val()
    const listId = evt.target.name;

    const formData = {"item" : newItem, "checklist_id" : listId};
    console.log(formData);

    $.get("/add_checklist_item", formData, response => {
        console.log(response)
    });

    $('#clothes-bag-list-ul').append(`<li>${newItem}</li>`);
}

$('#clothes-list-add-item-btn').on('click', addClothesListItem);

// Toiletries packing list functions
const addToiletriesListItem = (evt) => {
    const newItem = $('#add-new-toiletries-list-item').val()
    const listId = evt.target.name;

    const formData = {"item" : newItem, "checklist_id" : listId};
    console.log(formData);

    $.get("/add_checklist_item", formData, response => {
        console.log(response)
    });

    $('#toiletries-bag-list-ul').append(`<li>${newItem}</li>`);
}

$('#toiletries-list-add-item-btn').on('click', addToiletriesListItem);

// Misc. packing list functions
const addMiscListItem = (evt) => {
    const newItem = $('#add-new-misc-list-item').val()
    const listId = evt.target.name;
    
    const formData = {"item" : newItem, "checklist_id" : listId};
    console.log(formData);

    $.get("/add_checklist_item", formData, response => {
        console.log(response)
    });

    $('#misc-bag-list-ul').append(`<li>${newItem}</li>`);
}

$('#misc-list-add-item-btn').on('click', addMiscListItem);


// Delete list item function

const deleteListItem = (evt) => {

    const itemId = evt.target.id;
    alert(`You clicked the delete span\nitem id = ${itemId}`);

    const formData = {"item_id" : itemId};

    $.get("/delete_checklist_item", formData, response => {
        console.log(response);
        location.reload();
    });
}

$('.delete-list-item').on('click', deleteListItem);