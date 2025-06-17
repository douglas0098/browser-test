function togglePassword(fieldId) {
    const passwordField = document.getElementById(fieldId);
    const eyeIcon = passwordField.parentElement.querySelector('.eye-icon');
    const eyeOffIcon = passwordField.parentElement.querySelector('.eye-off-icon');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcon.style.display = 'none';
        eyeOffIcon.style.display = 'inline';
    } else {
        passwordField.type = 'password';
        eyeIcon.style.display = 'inline';
        eyeOffIcon.style.display = 'none';
    }
}