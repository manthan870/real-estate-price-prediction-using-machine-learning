var passwordVisible = false;

function togglePasswordVisibility() {
    var passwordInput = document.getElementById('password');
    var toggleIcon = document.getElementById('toggleIcon');

    if (!passwordVisible) {
        passwordInput.setAttribute('type', 'text');
        toggleIcon.innerHTML = '&#x1f576;';
    } else {
        passwordInput.setAttribute('type', 'password');
        toggleIcon.innerHTML = '&#x1f441;';
    }
    passwordVisible = !passwordVisible;
}

function login() {
var username = document.getElementById('username').value;
var password = document.getElementById('password').value;

if (username && password) {
alert('Logged in as ' + username);

// Redirect the user to another page
window.location.href = "user.html";

} else {
alert('Please enter both username and password');
}
}
