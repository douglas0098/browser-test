// Funcionalidade para a geração de boleto
document.addEventListener('DOMContentLoaded', function() {
    // Formulário de Boleto
    const boletoForm = document.getElementById('form-boleto');
    
    if (boletoForm) {
        // Evento de submit do formulário
        boletoForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Mostrar loading
            const boletoLoading = document.getElementById('boleto-loading');
            boletoLoading.style.display = 'flex';
            
            // Obter dados do formulário
            const formData = {
                name: document.getElementById('boleto-name').value,
                email: document.getElementById('boleto-email').value,
                cpf: document.getElementById('boleto-cpf').value.replace(/\D/g, ''),
                phone: document.getElementById('boleto-telefone').value.replace(/\D/g, ''),
                zipCode: document.getElementById('boleto-cep').value.replace(/\D/g, ''),
                address: document.getElementById('boleto-endereco').value,
                city: document.getElementById('boleto-cidade').value,
                state: document.getElementById('boleto-estado').value,
                amount: 99.90,
                description: "Assinatura UP Browser"
            };
            
            // Gerar boleto via Mercado Pago (simulação)
            // Na implementação real, você enviaria esses dados para seu backend
            // que faria a integração com a API do Mercado Pago
            generateMercadoPagoBoleto(formData)
                .then(boletoData => {
                    // Esconder loading
                    boletoLoading.style.display = 'none';
                    
                    // Mostrar resultado do boleto
                    displayBoletoResult(boletoData);
                })
                .catch(error => {
                    // Esconder loading
                    boletoLoading.style.display = 'none';
                    
                    // Mostrar erro
                    alert('Erro ao gerar boleto: ' + error.message);
                    console.error('Erro ao gerar boleto:', error);
                });
        });
        
        // Adicionar máscaras aos campos
        if (typeof IMask !== 'undefined') {
            // CPF mask
            IMask(document.getElementById('boleto-cpf'), {
                mask: '000.000.000-00'
            });
            
            // Telefone mask
            IMask(document.getElementById('boleto-telefone'), {
                mask: '(00) 00000-0000'
            });
            
            // CEP mask
            IMask(document.getElementById('boleto-cep'), {
                mask: '00000-000'
            });
        }
        
        // Auto-preenchimento de endereço pelo CEP
        const cepInput = document.getElementById('boleto-cep');
        if (cepInput) {
            cepInput.addEventListener('blur', function() {
                const cep = this.value.replace(/\D/g, '');
                
                if (cep.length === 8) {
                    fetch(`https://viacep.com.br/ws/${cep}/json/`)
                        .then(response => response.json())
                        .then(data => {
                            if (!data.erro) {
                                document.getElementById('boleto-endereco').value = `${data.logradouro}, `;
                                document.getElementById('boleto-cidade').value = data.localidade;
                                document.getElementById('boleto-estado').value = data.uf;
                            }
                        })
                        .catch(error => console.error('Erro ao buscar CEP:', error));
                }
            });
        }
    }
    
    // Configurar botões de cópia
    const copyButtons = document.querySelectorAll('.copy-button');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const copyId = this.getAttribute('data-copy');
            const copyElement = document.getElementById(copyId);
            
            copyElement.select();
            document.execCommand('copy');
            
            // Feedback visual
            const originalText = this.innerText;
            this.innerText = 'Copiado!';
            
            setTimeout(() => {
                this.innerText = originalText;
            }, 2000);
        });
    });
    
    // Botão de enviar por email
    const emailButton = document.getElementById('boleto-email-btn');
    if (emailButton) {
        emailButton.addEventListener('click', function() {
            const email = document.getElementById('boleto-email').value;
            
            // Simulação de envio por email
            setTimeout(() => {
                alert(`Boleto enviado para o email: ${email}`);
            }, 1000);
        });
    }
});

// Função para simular a geração de boleto do Mercado Pago
// Na implementação real, isso seria feito pelo seu backend
function generateMercadoPagoBoleto(formData) {
    return fetch('/api/gerar-boleto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao gerar boleto');
        }
        return response.json();
    });
}

// Função para exibir o resultado do boleto
function displayBoletoResult(boletoData) {
    // Exibir área de resultado
    const boletoResult = document.getElementById('boleto-result');
    boletoResult.style.display = 'block';
    
    // Preencher dados
    document.getElementById('boleto-vencimento').value = boletoData.dueDate;
    document.getElementById('boleto-barcode').value = boletoData.barcode;
    
    // Configurar link do PDF
    const pdfLink = document.getElementById('boleto-pdf-link');
    pdfLink.href = boletoData.pdfUrl;
    
    // Esconder formulário
    document.getElementById('form-boleto').style.display = 'none';
}