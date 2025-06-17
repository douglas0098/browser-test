const cpfInput = document.getElementById('cpf');
    
    cpfInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Remove todos os caracteres não numéricos
        value = value.replace(/\D/g, '');
        
        // Aplica a máscara conforme o usuário digita
        if (value.length > 0) {
            value = value.replace(/^(\d{3})(\d)/g, '$1.$2');
        }
        if (value.length > 3) {
            value = value.replace(/^(\d{3})\.(\d{3})(\d)/g, '$1.$2.$3');
        }
        if (value.length > 6) {
            value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/g, '$1.$2.$3-$4');
        }
        
        // Limita ao tamanho de um CPF
        if (value.length > 11) {
            value = value.substring(0, 14);
        }
        
        e.target.value = value;
    });