// assets/js/bridge/bridge_injector.js
(function () {
    if (window.pyQtApi) {
        console.log('pyQtApi já existe, não é necessário recriar');
        return;
    }

    console.log('Verificando disponibilidade de pyQtBridge...');

    function createApi() {
        if (window.pyQtBridge) {
            console.log('pyQtBridge encontrado, criando API');
            window.pyQtApi = {
                verifyLogin: function (username, password) {
                    console.log('Chamando verifyLogin com:', username);
                    window.pyQtBridge.verifyLogin(username, password);
                },
                registerUser: function (username, password, email, cpf) {
                    console.log('Chamando registerUser com:', username, email);
                    // Se CPF foi fornecido, usar método com 4 argumentos
                    if (cpf !== undefined && cpf !== null && cpf !== '') {
                        console.log('Usando registerUserWithCPF (4 args)');
                        window.pyQtBridge.registerUserWithCPF(username, password, email, cpf);
                    } else {
                        console.log('Usando registerUser (3 args)');
                        window.pyQtBridge.registerUser(username, password, email);
                    }
                },
                openRegisterPage: function () {
                    window.pyQtBridge.openRegisterPage();
                },
                openLoginPage: function () {
                    window.pyQtBridge.openLoginPage();
                }
            };
            console.log('pyQtApi criado com sucesso');
            return true;
        }
        return false;
    }

    // Tenta criar a API imediatamente
    if (!createApi()) {
        console.log('pyQtBridge não disponível ainda, configurando timer...');
        let attempts = 0;
        let intervalId = setInterval(function () {
            attempts++;
            if (createApi() || attempts > 10) {
                clearInterval(intervalId);
                console.log('Tentativas de criar API:', attempts, 'Sucesso:', !!window.pyQtApi);
            }
        }, 500);
    }
})();