// assets/js/register_simple.js
// Script super simples para registro

document.addEventListener('DOMContentLoaded', function() {
    console.log("Register page loaded");
    
    var registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleRegister();
        });
    }
});

function handleRegister() {
    var name = document.getElementById('name').value.trim();
    var username = document.getElementById('username').value.trim();
    var password = document.getElementById('ia-password').value;
    var confirmPassword = document.getElementById('ia-confirm-password').value;
    var cpf = document.getElementById('cpf').value.trim();
    var phone = document.getElementById('telefone').value.trim();
    var email = document.getElementById('email').value.trim();
    
    console.log("Register data:", {name: name, username: username, phone: phone, email: email});
    
    // Validations
    if (!name || !username || !password || !confirmPassword || !phone || !email) {
        showError("Please fill all required fields!");
        return;
    }
    
    if (password !== confirmPassword) {
        showError("Passwords do not match!");
        return;
    }
    
    if (password.length < 6) {
        showError("Password must be at least 6 characters!");
        return;
    }
    
    var submitBtn = document.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = "Registering...";
    
    if (window.SimpleBridge && window.SimpleBridge.isReady()) {
        window.SimpleBridge.register(username, password, email, name, phone, cpf);
    } else {
        console.log("Bridge not ready, waiting...");
        document.addEventListener('bridgeReady', function() {
            window.SimpleBridge.register(username, password, email, name, phone, cpf);
        });
    }
}

function showError(message) {
    var errorElement = document.getElementById('errorMessage');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(function() {
            errorElement.style.display = 'none';
        }, 5000);
    }
}