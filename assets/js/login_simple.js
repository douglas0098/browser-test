// assets/js/login_simple.js
// Script super simples para login

document.addEventListener('DOMContentLoaded', function() {
    console.log("Login page loaded");
    
    var loginBtn = document.getElementById('login-btn');
    var registerLink = document.getElementById('register-link');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogin();
        });
    }
    
    if (registerLink) {
        registerLink.addEventListener('click', function(e) {
            e.preventDefault();
            handleRegister();
        });
    }
});

function handleLogin() {
    var username = document.getElementById('username').value.trim();
    var password = document.getElementById('ia-password').value;
    
    if (!username || !password) {
        showError("Please fill all fields!");
        return;
    }
    
    console.log("Attempting login:", username);
    
    var loginBtn = document.getElementById('login-btn');
    loginBtn.disabled = true;
    loginBtn.textContent = "Logging in...";
    
    if (window.SimpleBridge && window.SimpleBridge.isReady()) {
        window.SimpleBridge.login(username, password);
    } else {
        console.log("Bridge not ready, waiting...");
        document.addEventListener('bridgeReady', function() {
            window.SimpleBridge.login(username, password);
        });
    }
}

function handleRegister() {
    if (window.SimpleBridge && window.SimpleBridge.isReady()) {
        window.SimpleBridge.goToRegister();
    } else {
        window.location.href = 'register.html';
    }
}

function showError(message) {
    var errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(function() {
            errorElement.style.display = 'none';
        }, 5000);
    }
}