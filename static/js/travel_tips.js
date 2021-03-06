"use strict";

// ************************* Function for Adding a New Tip Dynamically: ************************************
const showDynamicAddTipForm = () => {
    $.get("/check_session", response => {
        if (response === "False"){
            window.open("/login", "_self");
            alert("Please log in before adding a travel tip");
        }else{
            $('#travel-tips-filter-div').html(`
            <form id="new-tip-information" action="/add_new_tip">
            <h4>Add Your New Tip Here:</h4>
            <div id="tags">
                <label>Select tags:</label>
                <input type="radio" name="tags" id="money-tag" value="money"><label>Money/Theft</label>
                <input type="radio" name="tags" id="food-tag" value="food"><label>Food</label>
                <input type="radio" name="tags" id="health-tag" value="health"><label>Health</label>
                <input type="radio" name="tags" id="lgbt-tag" value="lgbt"><label>LGBTQIA+</label>
                <input type="radio" name="tags" id="solo-travel-tag" value="solo-travel"><label>Solo Travel</label>
                <input type="radio" name="tags" id="roadtrip-tag" value="roadtrips"><label>Roadtrip</label>
                <input type="radio" name="tags" id="hiking-tag" value="hiking"><label>Hiking/Backpacking</label>
                <input type="radio" name="tags" id="camping-tag" value="camping"><label>Camping</label>
                <input type="radio" name="tags" id="other-tag" value="other"><label>Other</label>
            </div>
            <p></p>
            <div id="location">
                <label>Please enter the state and city, if applicable</label><p></p>
                <label>State:</label><input type="text" name="state">
                <label>City:</label><input type="text" name="city">
            </div>
            <p></p>
            <div id="tip-text">
                <label>Enter your tip here:</label>
                <textarea name="tip-text"></textarea>
            </div>
            <p></p>

            <input type="submit">
        </form>
        `);
        }
    });
}


$('.add-tip-button').on('click', showDynamicAddTipForm);