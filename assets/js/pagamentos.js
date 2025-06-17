// Script para gerenciar as seções
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar a primeira seção por padrão
    document.getElementById('perfil').classList.add('active');
    
    // Adicionar funcionalidade às abas de pagamento
    const paymentTabs = document.querySelectorAll('.payment-tab');
    paymentTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remover classe ativa de todas as abas
            paymentTabs.forEach(t => t.classList.remove('active'));
            // Adicionar classe ativa à aba clicada
            this.classList.add('active');
            
            // Esconder todos os conteúdos
            const contents = document.querySelectorAll('.payment-tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Mostrar o conteúdo correspondente
            const tabId = this.getAttribute('data-tab');
            document.getElementById(`${tabId}-content`).classList.add('active');
        });
    });
    
    // Funcionalidade para copiar texto
    const copyButtons = document.querySelectorAll('.copy-button');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const fieldId = this.getAttribute('data-copy');
            const inputField = document.getElementById(fieldId);
            
            // Selecionar o texto
            inputField.select();
            inputField.setSelectionRange(0, 99999); // Para dispositivos móveis
            
            // Copiar o texto
            document.execCommand('copy');
            
            // Feedback visual
            const originalText = this.textContent;
            this.textContent = 'Copiado!';
            this.style.backgroundColor = '#2ecc71';
            
            // Restaurar o texto original após 2 segundos
            setTimeout(() => {
                this.textContent = originalText;
                this.style.backgroundColor = '';
            }, 2000);
        });
    });
    
    // Modal para adicionar/editar usuário
    const modal = document.getElementById('user-modal');
    const addUserBtn = document.getElementById('add-user-btn');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.cancel-button');
    
    // Abrir modal ao clicar em adicionar usuário
    if (addUserBtn) {
        addUserBtn.addEventListener('click', function() {
            modal.style.display = 'block';
            // Limpar formulário
            document.getElementById('user-form').reset();
        });
    }
    
    // Abrir modal ao clicar em editar usuário
    const editButtons = document.querySelectorAll('.action-button.edit');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const name = row.cells[0].textContent;
            const email = row.cells[1].textContent;
            const group = row.querySelector('.group-select').value;
            const status = row.cells[3].querySelector('.status').classList.contains('active') ? 'active' : 'inactive';
            
            // Preencher formulário com dados do usuário
            document.getElementById('user-name').value = name;
            document.getElementById('user-email').value = email;
            document.getElementById('user-group').value = group;
            document.getElementById('user-status').value = status;
            
            // Mostrar modal
            modal.style.display = 'block';
        });
    });
    
    // Fechar modal
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    // Fechar modal ao clicar fora dele
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Envio do formulário de usuário
    const userForm = document.getElementById('user-form');
    if (userForm) {
        userForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Simular salvamento (em um sistema real, enviaria para o servidor)
            alert('Usuário salvo com sucesso!');
            
            // Fechar modal
            modal.style.display = 'none';
        });
    }
    
    // Funcionalidade de exclusão de usuário
    const deleteButtons = document.querySelectorAll('.action-button.delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const name = row.cells[0].textContent;
            
            if (confirm(`Tem certeza que deseja excluir o usuário ${name}?`)) {
                // Em um sistema real, enviaria a exclusão para o servidor
                row.remove();
                alert('Usuário excluído com sucesso!');
            }
        });
    });
    
    // Função para limpar cache
    
    
    // Função para aplicar configurações de antidetecção
    window.applyAntiDetectionSettings = function() {
        // Simular aplicação das configurações
        alert('Configurações de antidetecção aplicadas com sucesso!');
    };
    
    // Implementação da busca de usuários
    const searchInput = document.getElementById('search-users');
    const searchButton = document.querySelector('.search-button');
    
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', function() {
            searchUsers();
        });
        
        // Busca também ao pressionar Enter
        searchInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                searchUsers();
            }
        });
    }
    
    function searchUsers() {
        const searchTerm = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll('.user-table tbody tr');
        
        rows.forEach(row => {
            const name = row.cells[0].textContent.toLowerCase();
            const email = row.cells[1].textContent.toLowerCase();
            const group = row.querySelector('.group-select').options[row.querySelector('.group-select').selectedIndex].text.toLowerCase();
            
            if (name.includes(searchTerm) || email.includes(searchTerm) || group.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    
    // Gerenciamento dos grupos de usuários
    const groupSelects = document.querySelectorAll('.group-select');
    groupSelects.forEach(select => {
        // Salvar o valor original para detectar mudanças
        select.dataset.originalValue = select.value;
        
        select.addEventListener('change', function() {
            const row = this.closest('tr');
            const userName = row.cells[0].textContent;
            const newGroup = this.options[this.selectedIndex].text;
            const oldGroup = this.options[select.dataset.originalValue].text;
            
            // Confirmar a mudança de grupo
            const confirmed = confirm(`Deseja alterar o grupo de ${userName} de '${oldGroup}' para '${newGroup}'?`);
            
            if (confirmed) {
                // Atualizar o valor original após confirmar
                this.dataset.originalValue = this.value;
                alert(`Usuário ${userName} movido para o grupo ${newGroup} com sucesso!`);
            } else {
                // Reverter para o valor original se não confirmado
                this.value = this.dataset.originalValue;
            }
        });
    });
    
    // Salvar alterações de usuários
    const saveUsersBtn = document.getElementById('save-users-btn');
    if (saveUsersBtn) {
        saveUsersBtn.addEventListener('click', function() {
            // Em uma aplicação real, enviaria as alterações para o servidor
            alert('Alterações salvas com sucesso!');
        });
    }
    
    // Funcionalidade para boleto
    const downloadButton = document.querySelector('.download-button');
    if (downloadButton) {
        downloadButton.addEventListener('click', function() {
            // Simular download do boleto
            alert('Download do boleto iniciado!');
        });
    }
    
    const emailButton = document.querySelector('.email-button');
    if (emailButton) {
        emailButton.addEventListener('click', function() {
            // Simular envio de email com boleto
            const email = prompt('Digite seu email para receber o boleto:');
            if (email) {
                alert(`Boleto enviado para ${email} com sucesso!`);
            }
        });
    }
});

// Função para mostrar seções
function showSection(sectionId) {
    // Esconder todas as seções
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Mostrar a seção selecionada
    document.getElementById(sectionId).classList.add('active');
    
    // Destacar botão do menu correspondente
    const menuButtons = document.querySelectorAll('.menu button');
    menuButtons.forEach(button => {
        if (button.getAttribute('onclick').includes(sectionId)) {
            button.style.backgroundColor = '#2980b9';
        } else {
            button.style.backgroundColor = '#34495e';
        }
    });
}