"use strict";

const filterTips = (evt) => {
    evt.preventDefault();
    alert("Prevent default is working")

};


$('#travel-tips-filter-btn').on('click', filterTips);
