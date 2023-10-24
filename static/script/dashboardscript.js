document.addEventListener('DOMContentLoaded', (event) => {
    const savedPicture = localStorage.getItem('profilePicture');
    if (savedPicture) {
        document.getElementById('profilePicture').src = savedPicture;
    }
});

$('.custom-file-input').on('change', function() {
    var fileName = $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass("selected").html(fileName);
});

document.getElementById('passwordChangeForm').addEventListener('submit', function(e) {
e.preventDefault();

const newPassword = document.getElementById('newPassword');
const confirmPassword = document.getElementById('confirmPassword');
const passwordChangeAlert = document.getElementById('passwordChangeAlert');

let formIsValid = true;

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

if (formIsValid) {
passwordChangeAlert.style.display = 'block';
passwordChangeAlert.classList.add('show');

// Reset the form to clear the input fields
e.target.reset();

// Hide the success alert after 10 seconds
setTimeout(function() {
    passwordChangeAlert.classList.remove('show');
}, 10000); // 10 seconds = 10000 milliseconds
}

});

document.getElementById('pictureChangeForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const pictureChangeAlert = document.getElementById('pictureChangeAlert');
    const fileInput = document.getElementById('customFile');
    const profilePicture = document.getElementById('profilePicture');

    if (fileInput.files && fileInput.files[0]) {
const reader = new FileReader();

reader.onload = function(e) {
    const imageDataUrl = e.target.result;
    localStorage.setItem('profilePicture', imageDataUrl); // save to local storage
    profilePicture.src = imageDataUrl; // update the image
}

reader.readAsDataURL(fileInput.files[0]);

pictureChangeAlert.style.display = 'block';
pictureChangeAlert.classList.add('show');

// Hide the success alert after 10 seconds
setTimeout(function() {
    pictureChangeAlert.classList.remove('show');
}, 10000); // 10 seconds = 10000 milliseconds

// Reset the file input field and label
fileInput.value = ""; // Reset the input
$('.custom-file-label').html("Choose file"); // Reset the label
}



    pictureChangeAlert.style.display = 'block';
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

