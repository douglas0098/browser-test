function filtrarProxies() {
    const input = document.getElementById('buscar-ia');
    const filter = input.value.toUpperCase();
    const table = document.getElementById('proxy-table');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < cells.length - 1; j++) {
            const cellText = cells[j].textContent || cells[j].innerText;
            if (cellText.toUpperCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }
        
        rows[i].style.display = found ? '' : 'none';
    }
}

// Função para editar um proxy
function editProxy(button) {
    const row = button.closest('tr');
    const proxyName = row.cells[0].innerText;
    document.getElementById('boleto-name').value = proxyName;
    // Scroll para o formulário
    document.getElementById('novo-proxy').scrollIntoView({ behavior: 'smooth' });
}

// Função para excluir um proxy
function deleteProxy(button) {
    if (confirm('Tem certeza que deseja excluir este proxy?')) {
        const row = button.closest('tr');
        row.remove();
    }
}

// Função para usar um proxy específico da tabela
function useProxy(button) {
    const row = button.closest('tr');
    const proxyName = row.cells[0].innerText;
    
    // Selecionar automaticamente este proxy no dropdown
    const select = document.getElementById('proxy-select');
    
    for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].text === proxyName) {
            select.selectedIndex = i;
            break;
        }
    }
    
    // Scroll para a seção de acesso
    document.querySelector('.proxy-access-section').scrollIntoView({ behavior: 'smooth' });
}

// Função para acessar site via proxy seguro
function accessViaSafeProxy() {
    const url = document.getElementById('site-url').value;
    const proxy = document.getElementById('proxy-select').value;
    const mode = document.getElementById('access-mode').value;
    
    if (!url || !proxy) {
        alert('Por favor, preencha a URL e selecione um proxy.');
        return;
    }
    
    // Criar modal para mostrar o processo
    const modal = document.createElement('div');
    modal.className = 'proxy-modal';
    modal.innerHTML = `
        <div class="proxy-modal-content">
            <h3>Preparando acesso seguro via proxy</h3>
            <div id="proxy-status">Configurando conexão segura...</div>
            <div class="loader"></div>
            <div id="proxy-details">
                <p><strong>Site:</strong> ${url}</p>
                <p><strong>Proxy:</strong> ${document.getElementById('proxy-select').options[document.getElementById('proxy-select').selectedIndex].text}</p>
                <p><strong>Modo:</strong> ${document.getElementById('access-mode').options[document.getElementById('access-mode').selectedIndex].text}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    // Simular o processo de configuração do proxy
    setTimeout(() => {
        document.getElementById('proxy-status').textContent = 'Mascarando identidade do navegador...';
        
        setTimeout(() => {
            document.getElementById('proxy-status').textContent = 'Configurando anti-detecção de login duplo...';
            
            setTimeout(() => {
                document.getElementById('proxy-status').textContent = 'Estabelecendo conexão segura...';
                
                setTimeout(() => {
                    // Abrir o site em uma nova janela/aba
                    window.open(url, '_blank');
                    
                    // Atualizar o modal
                    document.getElementById('proxy-status').textContent = 'Conexão estabelecida com sucesso!';
                    document.querySelector('.loader').style.display = 'none';
                    
                    const closeButton = document.createElement('button');
                    closeButton.textContent = 'Fechar';
                    closeButton.className = 'access-button';
                    closeButton.style.marginTop = '20px';
                    closeButton.onclick = () => {
                        modal.remove();
                    };
                    
                    document.querySelector('.proxy-modal-content').appendChild(closeButton);
                    
                }, 1500);
            }, 1000);
        }, 1000);
    }, 1000);
}

// Função para salvar um novo proxy
function applySalvarProxy() {
    const proxyName = document.getElementById('boleto-name').value;
    
    if (!proxyName) {
        alert('Por favor, insira um proxy válido.');
        return;
    }
    
    // Criar nova linha na tabela
    const table = document.getElementById('proxy-table');
    const newRow = table.insertRow(-1);
    
    // Inserir células
    const cell1 = newRow.insertCell(0);
    const cell2 = newRow.insertCell(1);
    const cell3 = newRow.insertCell(2);
    const cell4 = newRow.insertCell(3);
    
    // Adicionar conteúdo às células
    cell1.textContent = proxyName;
    cell2.textContent = '-';
    cell3.innerHTML = '<span class="status-vazio">Vazio</span>';
    cell4.innerHTML = `
        <button class="action-button edit" onclick="editProxy(this)">Editar</button>
        <button class="action-button delete" onclick="deleteProxy(this)">Excluir</button>
        <button class="action-button use" onclick="useProxy(this)">Usar</button>
    `;
    
    // Adicionar ao dropdown de seleção
    const select = document.getElementById('proxy-select');
    const option = document.createElement('option');
    option.text = proxyName;
    option.value = 'proxy' + (select.options.length);
    select.add(option);
    
    // Limpar o campo de entrada
    document.getElementById('boleto-name').value = '';
    
    // Evitar o comportamento padrão do formulário
    return false;
}