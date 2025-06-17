// Código de gestão de usuários logados com detecção de dispositivo e IP

document.addEventListener('DOMContentLoaded', function() {
    // Gerenciar as abas de perfil
    const profileTabs = document.querySelectorAll('.profile-tab');
    const profileContents = document.querySelectorAll('.profile-tab-content');
    
    profileTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remover classe active de todas as abas
            profileTabs.forEach(t => t.classList.remove('active'));
            profileContents.forEach(c => c.classList.remove('active'));
            
            // Adicionar classe active à aba clicada
            tab.classList.add('active');
            
            // Mostrar o conteúdo correspondente
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Função para obter informações do dispositivo
    async function getDeviceInfo() {
        try {
            // Obter endereço IP público
            const ipResponse = await fetch('https://api.ipify.org?format=json');
            const ipData = await ipResponse.json();
            const publicIP = ipData.ip;

            // Obter detalhes do dispositivo
            const platform = navigator.platform;
            const deviceName = getUserDeviceName();

            return {
                publicIP,
                platform,
                deviceName
            };
        } catch (error) {
            console.error('Erro ao obter informações do dispositivo:', error);
            return {
                publicIP: 'Não foi possível recuperar',
                platform: navigator.platform,
                deviceName: getUserDeviceName()
            };
        }
    }

    // Função para gerar nome descritivo do dispositivo
    function getUserDeviceName() {
        const platform = navigator.platform;

        // Verificar Windows
        if (platform.indexOf('Win') > -1) {
            return 'Windows PC';
        }

        // Verificar Mac
        if (platform.indexOf('Mac') > -1) {
            return 'Mac Computer';
        }

        // Verificar Linux
        if (platform.indexOf('Linux') > -1) {
            return 'Linux PC';
        }

        // Detecção de dispositivos móveis
        if (platform.indexOf('Android') > -1) return 'Android Device';
        if (platform.indexOf('iPhone') > -1) return 'iPhone';
        if (platform.indexOf('iPad') > -1) return 'iPad';

        return platform || 'Dispositivo Desconhecido';
    }
    
    // Botão de atualizar lista de usuários logados
    const refreshButton = document.querySelector('.refresh-button');
    if (refreshButton) {
        refreshButton.addEventListener('click', () => {
            updateLoggedUsersList();
        });
    }
    
    // Função para atualizar lista de usuários logados com informações do dispositivo
    async function updateLoggedUsersList() {
        try {
            const deviceInfo = await getDeviceInfo();

            // Atualizar a linha da tabela com informações do dispositivo
            const currentUserRow = document.querySelector('.logged-users-table tbody tr');
            if (currentUserRow) {
                // Atualizar coluna do dispositivo
                const deviceColumn = currentUserRow.querySelector('td:nth-child(2)');
                deviceColumn.textContent = deviceInfo.deviceName;

                // Atualizar coluna de IP
                const ipColumn = currentUserRow.querySelector('td:nth-child(3)');
                ipColumn.textContent = deviceInfo.publicIP;
            }

            alert('Lista de usuários atualizada com sucesso!');
        } catch (error) {
            console.error('Erro ao atualizar lista de usuários:', error);
            alert('Erro ao atualizar lista de usuários.');
        }
    }
    
    // Botões de desconectar usuário
    const disconnectButtons = document.querySelectorAll('.action-button.disconnect');
    disconnectButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const userRow = e.target.closest('tr');
            const userName = userRow.querySelector('.user-name').textContent;
            
            if (confirm(`Tem certeza que deseja desconectar o usuário ${userName}?`)) {
                // Aqui você adicionaria a lógica para desconectar o usuário
                // Por enquanto, apenas removeremos a linha da tabela para demonstração
                userRow.remove();
                alert(`Usuário ${userName} desconectado com sucesso.`);
            }
        });
    });
    
    // Botões de detalhes de sessão
    const detailButtons = document.querySelectorAll('.action-button.view-details');
    detailButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const userRow = e.target.closest('tr');
            const userName = userRow.querySelector('.user-name').textContent;
            
            showUserSessionDetails(userName);
        });
    });
    
    // Filtro de pesquisa de usuários
    const searchInput = document.getElementById('search-users');
    if (searchInput) {
        searchInput.addEventListener('input', filterUsers);
    }
    
    // Filtro de perfil
    const profileFilter = document.getElementById('filter-profile');
    if (profileFilter) {
        profileFilter.addEventListener('change', filterUsers);
    }
    
    // Atualizar tempo online periodicamente
    setInterval(updateOnlineTimes, 60000); // Atualiza a cada minuto

    // Chamar recuperação de informações do dispositivo ao carregar a página
    getDeviceInfo().then(deviceInfo => {
        console.log('Informações do Dispositivo:', deviceInfo);
        // Opcional: enviar para backend para registro
    });
});

// Função para filtrar usuários baseado na pesquisa e no filtro de perfil
function filterUsers() {
    const searchTerm = document.getElementById('search-users').value.toLowerCase();
    const profileFilter = document.getElementById('filter-profile').value;
    
    const userRows = document.querySelectorAll('.logged-users-table tbody tr');
    
    userRows.forEach(row => {
        const userName = row.querySelector('.user-name').textContent.toLowerCase();
        const userRole = row.querySelector('.user-role').textContent.toLowerCase();
        
        const matchesSearch = userName.includes(searchTerm);
        const matchesProfile = profileFilter === 'all' || 
                              (profileFilter === 'admin' && userRole.includes('administrador')) ||
                              (profileFilter === 'equipe' && userRole.includes('equipe')) ||
                              (profileFilter === 'membro' && userRole.includes('membro'));
        
        if (matchesSearch && matchesProfile) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Função para simular a atualização da lista de usuários logados
function updateLoggedUsersList() {
    // Aqui você faria uma requisição para o servidor para obter a lista atualizada
    // Por enquanto, apenas simularemos uma atualização visual
    
    const onlineTimeElements = document.querySelectorAll('.online-time span:nth-child(2)');
    onlineTimeElements.forEach(element => {
        if (element.textContent.includes('min')) {
            // Adicionar alguns minutos ao tempo online
            const currentTime = element.textContent;
            const timeRegex = /(\d+)h (\d+)min/;
            const match = currentTime.match(timeRegex);
            
            if (match) {
                let hours = parseInt(match[1]);
                let minutes = parseInt(match[2]) + Math.floor(Math.random() * 5) + 1;
                
                if (minutes >= 60) {
                    hours++;
                    minutes -= 60;
                }
                
                element.textContent = `${hours}h ${minutes}min`;
            }
        }
    });
    
    alert('Lista de usuários atualizada com sucesso!');
}

// Função para mostrar detalhes da sessão de um usuário
function showUserSessionDetails(userName) {
    // Aqui você implementaria a lógica para mostrar um modal ou expandir detalhes
    // Por enquanto, apenas mostraremos um alerta
    alert(`Detalhes da sessão para ${userName}:\n- Última ação: Visualizou relatórios\n- Atividades: 15 páginas visitadas\n- Hora de início: 08:30\n- Última atividade: 11:30`);
}

// Função para atualizar os tempos online
function updateOnlineTimes() {
    const activeUsers = document.querySelectorAll('.online-indicator.active');
    
    activeUsers.forEach(indicator => {
        const timeElement = indicator.nextElementSibling;
        const currentTime = timeElement.textContent;
        const timeRegex = /(\d+)h (\d+)min/;
        const match = currentTime.match(timeRegex);
        
        if (match) {
            let hours = parseInt(match[1]);
            let minutes = parseInt(match[2]) + 1;
            
            if (minutes >= 60) {
                hours++;
                minutes = 0;
            }
            
            timeElement.textContent = `${hours}h ${minutes}min`;
        }
    });
}