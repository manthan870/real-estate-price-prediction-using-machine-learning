function togglePasswordVisibility() {
    var passwordInput = document.getElementById('password');
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

function createAccount() {
var username = document.getElementById('signupUsername').value;
var name = document.getElementById('name').value;
var email = document.getElementById('email').value;
var password = document.getElementById('password').value;
var confirmPassword = document.getElementById('confirmPassword').value;

if (!name.match(/^[a-zA-Z\s]+$/)) {
alert('Name should only contain characters.');
return;
}

var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
if (!email.match(emailRegex)) {
alert('Please enter a valid email address.');
return;
}

if (password !== confirmPassword) {
alert('Password and Confirm Password should match.');
return;
}

alert('Account Created for ' + username + '!');

// Redirect the user to another page
window.location.href = "user";
}
