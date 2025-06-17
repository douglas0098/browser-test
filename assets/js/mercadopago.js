// Carrega o SDK do Mercado Pago
const script = document.createElement('script');
script.src = "https://sdk.mercadopago.com/js/v2";
script.type = "text/javascript";
document.body.appendChild(script);

// Configuração do Mercado Pago
script.onload = function() {
    // Inicializa o objeto Mercado Pago com sua chave pública
    const mp = new MercadoPago('YOUR_PUBLIC_KEY', {
        locale: 'pt-BR'
    });
    
    // Inicializa o formulário de cartão
    initCardForm(mp);
    
    // Inicializa os event listeners
    setupEventListeners();
};

// Função para inicializar o formulário de cartão
function initCardForm(mp) {
    // Gera os campos do formulário de cartão
    const cardForm = mp.cardForm({
        amount: "99.90",
        autoMount: true,
        form: {
            id: "form-checkout",
            cardholderName: {
                id: "form-checkout__cardholderName",
                placeholder: "Nome como está no cartão",
            },
            cardholderEmail: {
                id: "form-checkout__email",
                placeholder: "E-mail",
            },
            cardNumber: {
                id: "form-checkout__cardNumber",
                placeholder: "Número do cartão",
            },
            expirationDate: {
                id: "form-checkout__expirationDate",
                placeholder: "MM/YY",
            },
            securityCode: {
                id: "form-checkout__securityCode",
                placeholder: "CVV",
            },
            installments: {
                id: "form-checkout__installments",
                placeholder: "Parcelas",
            },
            identificationType: {
                id: "form-checkout__identificationType",
                placeholder: "Tipo de documento",
            },
            identificationNumber: {
                id: "form-checkout__identificationNumber",
                placeholder: "Número do documento",
            },
            issuer: {
                id: "form-checkout__issuer",
                placeholder: "Banco emissor",
            },
        },
        callbacks: {
            onFormMounted: error => {
                if (error) {
                    console.warn("Form Mounted handling error: ", error);
                    return;
                }
                console.log("Form mounted");
                
                // Após o formulário ser montado, verifique o tipo de cartão selecionado inicialmente
                toggleInstallments();
            },
            onSubmit: event => {
                event.preventDefault();
                
                // Mostra um loader ou indicador de carregamento
                document.getElementById("form-checkout__submit").innerText = "Processando...";
                document.getElementById("form-checkout__submit").disabled = true;
                
                const {
                    paymentMethodId,
                    issuerId,
                    cardholderEmail: email,
                    amount,
                    token,
                    installments,
                    identificationNumber,
                    identificationType,
                } = cardForm.getCardFormData();
                
                // Obter o tipo de cartão selecionado
                const isCredit = document.getElementById('card-credit').checked;
                
                // Verificar se é pagamento recorrente
                const isSubscription = document.getElementById('subscription-checkbox').checked;
                
                // Aqui você faria a chamada para o seu backend que processará o pagamento
                // Esta é apenas uma simulação
                fetch("/processar-pagamento", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        token,
                        issuerId,
                        paymentMethodId,
                        transactionAmount: Number(amount),
                        installments: Number(installments),
                        email,
                        identification: {
                            type: identificationType,
                            number: identificationNumber,
                        },
                        paymentType: isCredit ? 'credit_card' : 'debit_card',
                        isRecurring: isSubscription
                    }),
                })
                .then(response => response.json())
                .then(result => {
                    // Simulando um pagamento bem-sucedido
                    showPaymentResult(true, isSubscription);
                })
                .catch(error => {
                    // Simulando um erro de pagamento
                    showPaymentResult(false);
                });
            },
            onFetching: (resource) => {
                console.log("Fetching resource: ", resource);
                return () => {
                    console.log("Done fetching resource: ", resource);
                };
            },
            onCardTokenReceived: (errorData, token) => {
                if (errorData) {
                    // Mostrar erro no cartão
                    console.error('Token error:', errorData);
                    return;
                }
            },
            onPaymentMethodsReceived: (errorData, methods) => {
                if (errorData) {
                    // Mostrar erro nos métodos de pagamento
                    console.error('Payment methods error:', errorData);
                    return;
                }
            }
        },
    });
}

// Configurar event listeners para a página
function setupEventListeners() {
    // Para alternar entre cartão de crédito e débito
    const creditOption = document.getElementById('card-credit');
    const debitOption = document.getElementById('card-debit');
    
    if (creditOption && debitOption) {
        creditOption.addEventListener('change', toggleInstallments);
        debitOption.addEventListener('change', toggleInstallments);
    }
    
    // Para exibir detalhes da assinatura quando o checkbox é selecionado
    const subscriptionCheckbox = document.getElementById('subscription-checkbox');
    const subscriptionDetails = document.getElementById('subscription-details');
    
    if (subscriptionCheckbox && subscriptionDetails) {
        subscriptionCheckbox.addEventListener('change', function() {
            if (this.checked) {
                subscriptionDetails.style.display = 'block';
                // Atualizar o texto do botão para refletir a assinatura
                document.getElementById('form-checkout__submit').innerText = 'Iniciar assinatura de R$ 99,90/mês';
            } else {
                subscriptionDetails.style.display = 'none';
                // Restaurar texto original do botão
                document.getElementById('form-checkout__submit').innerText = 'Pagar R$ 99,90';
            }
        });
    }
}

// Função para mostrar/ocultar o campo de parcelas baseado no tipo de cartão
function toggleInstallments() {
    const isCredit = document.getElementById('card-credit').checked;
    const installmentsGroup = document.getElementById('installments-group');
    
    if (installmentsGroup) {
        if (isCredit) {
            installmentsGroup.style.display = 'block';
        } else {
            installmentsGroup.style.display = 'none';
        }
    }
}

// Função para mostrar o resultado do pagamento
function showPaymentResult(success, isSubscription = false) {
    const paymentStatus = document.getElementById("payment-status");
    const statusIcon = document.getElementById("payment-status-icon");
    const statusMessage = document.getElementById("payment-status-message");
    const statusDetail = document.getElementById("payment-status-detail");
    
    paymentStatus.style.display = "block";
    
    if (success) {
        statusIcon.innerHTML = "✅";
        
        if (isSubscription) {
            statusMessage.innerText = "Assinatura ativada com sucesso!";
            statusDetail.innerText = "Sua assinatura mensal foi ativada. Você será cobrado automaticamente todo mês e receberá os comprovantes por e-mail.";
        } else {
            statusMessage.innerText = "Pagamento aprovado!";
            statusDetail.innerText = "Seu pagamento foi processado com sucesso. Você receberá uma confirmação no e-mail cadastrado.";
        }
        
        paymentStatus.className = "payment-status success";
    } else {
        statusIcon.innerHTML = "❌";
        statusMessage.innerText = "Pagamento não aprovado";
        statusDetail.innerText = "Houve um problema ao processar seu pagamento. Por favor, verifique os dados do cartão ou tente novamente mais tarde.";
        paymentStatus.className = "payment-status error";
        
        // Reabilita o botão de envio
        const submitButton = document.getElementById("form-checkout__submit");
        submitButton.innerText = "Tentar Novamente";
        submitButton.disabled = false;
    }
}