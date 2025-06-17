// assets/js/minimal_bridge.js
// Solução mínima e direta - SEM encoding complexo

console.log('Starting minimal bridge...');

// Global state
window.Bridge = {
    ready: false,
    obj: null
};

// Simple channel setup
function setupChannel() {
    console.log('Setting up channel...');
    
    if (typeof QWebChannel === 'undefined') {
        console.log('QWebChannel not available yet');
        return false;
    }
    
    try {
        new QWebChannel(qt.webChannelTransport, function(channel) {
            console.log('Channel created successfully');
            
            window.Bridge.obj = channel.objects.unifiedBridge;
            window.Bridge.ready = true;
            
            if (window.Bridge.obj && window.Bridge.obj.pageReady) {
                window.Bridge.obj.pageReady();
            }
            
            console.log('Bridge ready!');
            document.dispatchEvent(new Event('bridgeReady'));
        });
        
        return true;
    } catch (e) {
        console.log('Error setting up channel:', e);
        return false;
    }
}

// Try setup repeatedly
function trySetup() {
    if (setupChannel()) {
        console.log('Setup successful');
        return;
    }
    
    setTimeout(trySetup, 200);
}

// API functions
function bridgeLogin(username, password) {
    if (!window.Bridge.ready || !window.Bridge.obj) {
        console.log('Bridge not ready for login');
        return false;
    }
    
    console.log('Calling login:', username);
    window.Bridge.obj.login(username, password);
    return true;
}

function bridgeRegister(username, password, email, name, phone, cpf) {
    if (!window.Bridge.ready || !window.Bridge.obj) {
        console.log('Bridge not ready for register');
        return false;
    }
    
    console.log('Calling register:', username, name);
    window.Bridge.obj.register(username, password, email, name, phone, cpf || '');
    return true;
}

function bridgeGoToLogin() {
    if (window.Bridge.obj && window.Bridge.obj.goToLogin) {
        window.Bridge.obj.goToLogin();
    }
}

function bridgeGoToRegister() {
    if (window.Bridge.obj && window.Bridge.obj.goToRegister) {
        window.Bridge.obj.goToRegister();
    }
}

function bridgeGoToPanel() {
    if (window.Bridge.obj && window.Bridge.obj.goToPanel) {
        window.Bridge.obj.goToPanel();
    }
}

// Global API
window.SimpleBridge = {
    isReady: function() { return window.Bridge.ready; },
    login: bridgeLogin,
    register: bridgeRegister,
    goToLogin: bridgeGoToLogin,
    goToRegister: bridgeGoToRegister,
    goToPanel: bridgeGoToPanel
};

// Python callbacks
function loginSuccess(username, userId) {
    console.log('Login success:', username);
    localStorage.setItem('loggedIn', 'true');
    localStorage.setItem('username', username);
    localStorage.setItem('userId', userId);
    bridgeGoToPanel();
}

function loginError(message) {
    console.log('Login error:', message);
    showError(message);
}

function registerSuccess(username, name) {
    console.log('Register success:', username, name);
    alert('Welcome ' + name + '! Registration successful. Redirecting to login...');
    bridgeGoToLogin();
}

function registerError(message) {
    console.log('Register error:', message);
    showError(message);
}

function showError(message) {
    var errorElement = document.getElementById('error-message') || 
                      document.getElementById('errorMessage');
    
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(function() {
            errorElement.style.display = 'none';
        }, 5000);
    } else {
        alert('Error: ' + message);
    }
}

// Start setup
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', trySetup);
} else {
    trySetup();
}

console.log('Minimal bridge loaded');