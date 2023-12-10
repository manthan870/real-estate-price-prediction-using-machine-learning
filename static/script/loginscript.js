// Function 1: Toggle password visibility
document.addEventListener('DOMContentLoaded', function () {
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

    // Call the function when the page is loaded
    togglePasswordVisibility();
});
function togglePasswordVisibility(inputId) {
    var passwordInput = document.getElementById(inputId);
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

// Function 2: User login
document.addEventListener('DOMContentLoaded', function () {
    function login() {
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

        if (username && password) {
            alert('Logged in as ' + username);

            // Redirect the user to another page
            window.location.href = "/login";
        } else {
            alert('Please enter both username and password');
        }
    }

    // Call the function when the page is loaded
    login();
});

// Function 3: Remove alerts
document.addEventListener('DOMContentLoaded', function () {
    function removeAlerts() {
        var alertMessages = document.querySelectorAll('.alert');
        alertMessages.forEach(function (message) {
            setTimeout(function () {
                message.style.display = 'none';
            }, 10000); // 10 seconds (10000 milliseconds)
        });
    }

    // Call the function when the page is loaded
    removeAlerts();
});
