// Verifica se o QWebChannel está disponível
if (typeof QWebChannel !== 'undefined') {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyQtBridge = channel.objects.pyQtBridge;
        console.log('WebChannel initialized successfully');

        // Cria o objeto pyQtApi para compatibilidade
        window.pyQtApi = {
            verifyLogin: function(username, password) {
                if (window.pyQtBridge) {
                    return window.pyQtBridge.verifyLogin(username, password);
                }
                console.error('pyQtBridge not available');
                return false;
            },
            registerUser: function(username, password, email) {
                if (window.pyQtBridge) {
                    return window.pyQtBridge.registerUser(username, password, email);
                }
                console.error('pyQtBridge not available');
                return false;
            },
            openRegisterPage: function() {
                if (window.pyQtBridge) {
                    return window.pyQtBridge.openRegisterPage();
                }
                console.error('pyQtBridge not available');
                return false;
            },
            openLoginPage: function() {
                if (window.pyQtBridge) {
                    return window.pyQtBridge.openLoginPage();
                }
                console.error('pyQtBridge not available');
                return false;
            }
        };

        // Dispara evento de sucesso
        document.dispatchEvent(new Event('webChannelReady'));
    });
} else {
    console.error('QWebChannel not available');
    // Dispara evento de falha
    document.dispatchEvent(new Event('webChannelFailed'));
}
