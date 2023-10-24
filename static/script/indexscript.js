document.addEventListener('DOMContentLoaded', function () {
    let additionalSection = document.getElementById('additional-section');
    additionalSection.style.opacity = 0;
    additionalSection.style.transform = "translateY(50px)";
    window.addEventListener('scroll', function() {
        let position = additionalSection.getBoundingClientRect().top;
        let windowHeight = window.innerHeight;
        if (position < windowHeight) {
            additionalSection.style.opacity = 1;
            additionalSection.style.transform = "translateY(0)";
            additionalSection.style.transition = "all 1s";
            additionalSection.style.animation = "fade-in-left 2s";
            additionalSection.style.boxShadow = "0 0 20px rgba(0, 0, 0, 0.2)";
        }
    });
});