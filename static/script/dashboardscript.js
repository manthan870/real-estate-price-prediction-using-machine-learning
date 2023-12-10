

document.getElementById('passwordChangeForm').addEventListener('submit', function(e) {
e.preventDefault();

const oldPassword = document.getElementById('oldPassword');
const newPassword = document.getElementById('newPassword');
const confirmPassword = document.getElementById('confirmPassword');

let formIsValid = true;

if (oldPassword.value.length < 8) {
    alert('The password should be at least 8 characters long.');
    formIsValid = false;
    return;
}

if (newPassword.value.length < 8) {
    alert('The password should be at least 8 characters long.');
    formIsValid = false;
    return;
}

if (newPassword.value !== confirmPassword.value) {
    alert('The new password and confirm password fields should match.');
    formIsValid = false;
    return;
}


// Reset the form to clear the input fields
e.target.reset();


});


document.querySelectorAll('.toggle-password').forEach(button => {
button.addEventListener('click', (event) => {
    event.preventDefault();
    
    const passwordField = event.target.closest('.input-group').querySelector('input[type="password"], input[type="text"]');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        event.target.classList.remove('fa-eye');
        event.target.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        event.target.classList.remove('fa-eye-slash');
        event.target.classList.add('fa-eye');
    }
});
});


function goBack() {
    window.history.back();
}
$(document).ready(function() {
    console.log("Document is ready");

    $("#changePasswordButton").click(function(e) {
        console.log("Change password button clicked");
        e.preventDefault();
    });
});

