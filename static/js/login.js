"use strict";

console.log('Connected to JS file')

const username = $('#login-username-input').val()
const password = $('#login-password-input').val()

console.log(username)
console.log(password)

const checkPassword = (evt) => {
    evt.preventDefault()
    alert('Prevent default is working')
}

$('login-submit-input').on('click', checkPassword)