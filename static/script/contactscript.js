document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent the default form submission

    // Check if the form is valid:
    if (this.checkValidity()) {
        alert('Your message has been sent!');
        window.location.href = 'index.html'; 
    }
});

// This code is to trigger form validation when the submit button is clicked
document.getElementById('submitButton').addEventListener('click', function() {
    document.getElementById('contactForm').requestSubmit(); // this will trigger form submission event
});
