document.addEventListener('DOMContentLoaded', function() {
    // Input focus effects
    const inputs = document.querySelectorAll('.input-field input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentNode.querySelector('.focus-line').style.width = '100%';
        });
        
        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.parentNode.querySelector('.focus-line').style.width = '0';
            }
        });
    });

    // Form submission
    const form = document.querySelector('.auth-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add your form submission logic here
            console.log('Form submitted');
        });
    }
});