document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.getElementById('register-form');
    const emailInput = document.getElementById('email');
    const password = document.getElementById('password');
    const passwordConfirmation = document.getElementById('passwordConfirmation');
  
    form.addEventListener('submit', function(event) {
      event.preventDefault(); 
  
      const emailValue = emailInput.value.trim();
      const emailRegex = /^\S+@\S+\.\S+$/; 
      const passwordValue = password.value;
      const passwordConfirmationValue = passwordConfirmation.value;

      if (passwordValue !== passwordConfirmationValue) {
        alert('Passwords must match.');
        return;
      }
  
      if (!emailRegex.test(emailValue)) {
        alert('Please enter a valid email address.');
        return;
      }

      form.submit();
    });
  });