let channelAttempts = 0;

function setupChannel() {
    try {
        if (typeof QWebChannel === 'undefined') {
            console.log('QWebChannel ainda não disponível, tentativa ' + channelAttempts);
            if (channelAttempts < 10) {
                channelAttempts++;
                setTimeout(setupChannel, 500);
            }
            return;
        }

        console.log('QWebChannel disponível, configurando ponte...');

        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.pyQtBridge = channel.objects.pyQtBridge;

            window.pyQtApi = {
                verifyLogin: function(username, password) {
                    if (window.pyQtBridge) {
                        window.pyQtBridge.verifyLogin(username, password);
                    }
                },
                registerUser: function(username, password, email) {
                    if (window.pyQtBridge) {
                        window.pyQtBridge.registerUser(username, password, email);
                    }
                },
                openRegisterPage: function() {
                    if (window.pyQtBridge) {
                        window.pyQtBridge.openRegisterPage();
                    }
                },
                openLoginPage: function() {
                    if (window.pyQtBridge) {
                        window.pyQtBridge.openLoginPage();
                    }
                }
            };

            console.log('Ponte PyQt configurada com sucesso!');
        });
    } catch (e) {
        console.error('Erro ao configurar QWebChannel:', e);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    setupChannel();
});

if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setupChannel();
}
