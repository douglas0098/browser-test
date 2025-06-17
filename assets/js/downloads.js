// scripts.js para a seção de downloads

// Inicialização da página de downloads
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos na seção de downloads
    if (document.getElementById('downloads')) {
        initDownloadsSection();
    }
});

function initDownloadsSection() {
    // Configurar os listeners dos botões e filtros
    setupSearchAndFilters();
    setupActionButtons();
    
    // Tentar carregar o histórico de downloads
    loadDownloadsHistory();
    
    // Configurar listeners para os botões de configuração
    document.querySelector('.save-button')?.addEventListener('click', saveDownloadSettings);
    document.querySelector('.reset-button')?.addEventListener('click', resetDownloadSettings);
    
    // Listener para o botão de limpar downloads concluídos
    document.querySelector('.storage-text .clear-button')?.addEventListener('click', clearCompletedDownloads);
}

function setupSearchAndFilters() {
    // Busca
    const searchInput = document.getElementById('search-downloads');
    const searchButton = searchInput?.nextElementSibling;
    
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            filterDownloads();
        });
    }
    
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                filterDownloads();
            }
        });
    }
    
    // Filtros de tipo e data
    const filterType = document.getElementById('filter-type');
    const filterDate = document.getElementById('filter-date');
    
    if (filterType) {
        filterType.addEventListener('change', filterDownloads);
    }
    
    if (filterDate) {
        filterDate.addEventListener('change', filterDownloads);
    }
    
    // Botão de limpar filtros
    const clearFiltersBtn = document.getElementById('clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            if (searchInput) searchInput.value = '';
            if (filterType) filterType.value = 'all';
            if (filterDate) filterDate.value = 'all';
            filterDownloads();
        });
    }
}

function filterDownloads() {
    const searchQuery = document.getElementById('search-downloads')?.value.toLowerCase();
    const typeFilter = document.getElementById('filter-type')?.value;
    const dateFilter = document.getElementById('filter-date')?.value;
    
    const rows = document.querySelectorAll('.downloads-table tbody tr');
    
    rows.forEach(row => {
        const fileName = row.querySelector('.file-name')?.textContent.toLowerCase();
        const fileType = row.querySelector('td:nth-child(2)')?.textContent.toLowerCase();
        const fileDate = row.querySelector('td:nth-child(4)')?.textContent; // Data do download
        
        let showRow = true;
        
        // Filtro de busca
        if (searchQuery && fileName && !fileName.includes(searchQuery)) {
            showRow = false;
        }
        
        // Filtro de tipo
        if (typeFilter && typeFilter !== 'all') {
            // Mapear categorias de filtro para os tipos de arquivos
            const typeMatches = {
                'document': ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt'],
                'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'],
                'video': ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'webm'],
                'audio': ['mp3', 'wav', 'ogg', 'flac', 'aac'],
                'application': ['exe', 'msi', 'dmg', 'apk', 'app'],
                'other': ['zip', 'rar', '7z', 'tar', 'gz', 'iso']
            };
            
            // Verificar se o tipo do arquivo corresponde à categoria selecionada
            if (typeMatches[typeFilter] && !typeMatches[typeFilter].some(type => 
                fileType && fileType.includes(type))) {
                showRow = false;
            }
        }
        
        // Filtro de data
        if (dateFilter && dateFilter !== 'all' && fileDate) {
            const today = new Date();
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            
            const lastWeek = new Date(today);
            lastWeek.setDate(lastWeek.getDate() - 7);
            
            const lastMonth = new Date(today);
            lastMonth.setMonth(lastMonth.getMonth() - 1);
            
            const lastYear = new Date(today);
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            
            // Converter string de data para objeto Date
            const parts = fileDate.split(' ')[0].split('/');
            const downloadDate = new Date(parts[2], parts[1] - 1, parts[0]);
            
            switch (dateFilter) {
                case 'today':
                    if (downloadDate.toDateString() !== today.toDateString()) showRow = false;
                    break;
                case 'yesterday':
                    if (downloadDate.toDateString() !== yesterday.toDateString()) showRow = false;
                    break;
                case 'week':
                    if (downloadDate < lastWeek) showRow = false;
                    break;
                case 'month':
                    if (downloadDate < lastMonth) showRow = false;
                    break;
                case 'year':
                    if (downloadDate < lastYear) showRow = false;
                    break;
            }
        }
        
        // Mostrar ou esconder a linha
        row.style.display = showRow ? '' : 'none';
    });
    
    updateFilteredCount();
}

function updateFilteredCount() {
    const totalRows = document.querySelectorAll('.downloads-table tbody tr').length;
    const visibleRows = document.querySelectorAll('.downloads-table tbody tr:not([style*="display: none"])').length;
    
    // Poderia atualizar algum contador na interface, se existir
    console.log(`Mostrando ${visibleRows} de ${totalRows} downloads`);
}

function setupActionButtons() {
    // Delegação de eventos para os botões de ação (para trabalhar com itens dinâmicos)
    document.querySelector('.downloads-table')?.addEventListener('click', function(e) {
        // Botão de abrir arquivo
        if (e.target.classList.contains('open')) {
            const row = e.target.closest('tr');
            const filePath = row.querySelector('.folder-path .path-text').textContent;
            const fileName = row.querySelector('.file-name').textContent;
            openDownloadedFile(filePath, fileName);
        }
        
        // Botão de abrir pasta
        if (e.target.classList.contains('open-folder-btn')) {
            const path = e.target.dataset.path;
            openFolderLocation(path);
        }
        
        // Botão de excluir
        if (e.target.classList.contains('delete')) {
            const row = e.target.closest('tr');
            const fileName = row.querySelector('.file-name').textContent;
            deleteDownload(row, fileName);
        }
        
        // Botão de pausar
        if (e.target.classList.contains('pause')) {
            const row = e.target.closest('tr');
            togglePauseDownload(row);
        }
        
        // Botão de cancelar
        if (e.target.classList.contains('cancel')) {
            const row = e.target.closest('tr');
            cancelDownload(row);
        }
    });
}

function loadDownloadsHistory() {
    // Esta função seria chamada ao inicializar a página
    // Tentativa de comunicação com o Python através da ponte
    try {
        // Verificar se existe a ponte com o Python
        if (window.pyQtApi) {
            console.log('Solicitando histórico de downloads ao Python...');
            // Aqui você chamaria algum método do pyQtApi
            // window.pyQtApi.getDownloadsHistory();
            
            // Como o método específico não está definido, vamos simular recebendo dados
            // Normalmente, o Python retornaria os dados e chamaria uma função como updateDownloadsTable
            setTimeout(() => {
                console.log('Simulando resposta do Python com dados de download');
                
                // Não é necessário fazer nada aqui já que os dados já estão no HTML
                // Na implementação real, os dados viriam do Python e seriam renderizados
            }, 500);
        } else {
            console.error('pyQtApi não está disponível para carregar o histórico de downloads');
            
            // Para testes, podemos tentar novamente após um tempo
            setTimeout(() => {
                if (window.pyQtApi) {
                    console.log('pyQtApi disponível após espera, tentando novamente...');
                    // window.pyQtApi.getDownloadsHistory();
                }
            }, 2000);
        }
    } catch (e) {
        console.error('Erro ao tentar carregar histórico de downloads:', e);
    }
}

function openDownloadedFile(filePath, fileName) {
    console.log(`Abrindo arquivo: ${filePath}/${fileName}`);
    
    try {
        if (window.pyQtApi) {
            // Chamaria um método Python para abrir o arquivo
            // window.pyQtApi.openFile(filePath, fileName);
            console.log('Chamando Python para abrir o arquivo...');
            
            // Na versão real, o Python abrirá o arquivo usando código nativo
            // como subprocess.Popen(['xdg-open', filepath]) no Linux ou 
            // os.startfile(filepath) no Windows
        } else {
            alert(`Ação: Abrir arquivo ${fileName}`);
        }
    } catch (e) {
        console.error('Erro ao tentar abrir arquivo:', e);
        alert(`Não foi possível abrir o arquivo: ${e.message}`);
    }
}

function openFolderLocation(path) {
    console.log(`Abrindo pasta: ${path}`);
    
    try {
        if (window.pyQtApi) {
            // Chamaria um método Python para abrir a pasta
            // window.pyQtApi.openFolder(path);
            console.log('Chamando Python para abrir a pasta...');
            
            // Na versão real, o Python abrirá a pasta no gerenciador de arquivos do sistema
        } else {
            alert(`Ação: Abrir pasta ${path}`);
        }
    } catch (e) {
        console.error('Erro ao tentar abrir pasta:', e);
        alert(`Não foi possível abrir a pasta: ${e.message}`);
    }
}

function deleteDownload(row, fileName) {
    if (confirm(`Tem certeza que deseja excluir ${fileName} do histórico de downloads?`)) {
        console.log(`Excluindo download: ${fileName}`);
        
        try {
            if (window.pyQtApi) {
                // Chamaria um método Python para excluir o download do histórico
                // window.pyQtApi.deleteDownload(fileName);
                console.log('Chamando Python para excluir o download...');
                
                // Simularemos a remoção para visualização
                row.classList.add('removing');
                setTimeout(() => {
                    row.remove();
                    updateStorageInfo();
                }, 500);
            } else {
                // Simulação para testes
                row.classList.add('removing');
                setTimeout(() => {
                    row.remove();
                    updateStorageInfo();
                }, 500);
            }
        } catch (e) {
            console.error('Erro ao tentar excluir download:', e);
            alert(`Não foi possível excluir o download: ${e.message}`);
        }
    }
}

function togglePauseDownload(row) {
    const pauseBtn = row.querySelector('.pause');
    const status = row.querySelector('.download-status');
    
    if (pauseBtn.textContent === 'Pausar') {
        pauseBtn.textContent = 'Retomar';
        pauseBtn.title = 'Retomar download';
        status.textContent = 'Pausado';
        status.className = 'download-status paused';
        
        try {
            if (window.pyQtApi) {
                // window.pyQtApi.pauseDownload(fileName);
                console.log('Chamando Python para pausar o download...');
            }
        } catch (e) {
            console.error('Erro ao pausar download:', e);
        }
    } else {
        pauseBtn.textContent = 'Pausar';
        pauseBtn.title = 'Pausar download';
        status.textContent = 'Em andamento (80%)';
        status.className = 'download-status pending';
        
        try {
            if (window.pyQtApi) {
                // window.pyQtApi.resumeDownload(fileName);
                console.log('Chamando Python para retomar o download...');
            }
        } catch (e) {
            console.error('Erro ao retomar download:', e);
        }
    }
}

function cancelDownload(row) {
    const fileName = row.querySelector('.file-name').textContent;
    
    if (confirm(`Tem certeza que deseja cancelar o download de ${fileName}?`)) {
        console.log(`Cancelando download: ${fileName}`);
        
        try {
            if (window.pyQtApi) {
                // window.pyQtApi.cancelDownload(fileName);
                console.log('Chamando Python para cancelar o download...');
                
                // Simular cancelamento
                row.querySelector('.download-status').textContent = 'Cancelado';
                row.querySelector('.download-status').className = 'download-status error';
                
                // Substituir botões
                const actionBtns = row.querySelector('.action-buttons');
                actionBtns.innerHTML = '<button class="action-button delete" title="Excluir download">Excluir</button>';
            } else {
                // Simulação para testes
                row.querySelector('.download-status').textContent = 'Cancelado';
                row.querySelector('.download-status').className = 'download-status error';
                
                // Substituir botões
                const actionBtns = row.querySelector('.action-buttons');
                actionBtns.innerHTML = '<button class="action-button delete" title="Excluir download">Excluir</button>';
            }
        } catch (e) {
            console.error('Erro ao cancelar download:', e);
            alert(`Não foi possível cancelar o download: ${e.message}`);
        }
    }
}

function saveDownloadSettings() {
    const defaultLocation = document.getElementById('default-location').value;
    const askLocation = document.getElementById('ask-location').checked;
    const autoOpen = document.getElementById('auto-open').checked;
    const downloadLimit = document.getElementById('download-limit').value;
    
    const settings = {
        defaultLocation,
        askLocation,
        autoOpen,
        downloadLimit
    };
    
    console.log('Salvando configurações de download:', settings);
    
    try {
        if (window.pyQtApi) {
            // window.pyQtApi.saveDownloadSettings(JSON.stringify(settings));
            console.log('Chamando Python para salvar configurações...');
            alert('Configurações salvas com sucesso!');
        } else {
            // Simulação para testes
            localStorage.setItem('downloadSettings', JSON.stringify(settings));
            alert('Configurações salvas com sucesso!');
        }
    } catch (e) {
        console.error('Erro ao salvar configurações:', e);
        alert(`Não foi possível salvar as configurações: ${e.message}`);
    }
}

function resetDownloadSettings() {
    // Valores padrão
    document.getElementById('default-location').value = 'C:\\Users\\Joao\\Downloads';
    document.getElementById('ask-location').checked = true;
    document.getElementById('auto-open').checked = false;
    document.getElementById('download-limit').value = '3';
    
    console.log('Restaurando configurações padrão de download');
    
    try {
        if (window.pyQtApi) {
            // window.pyQtApi.resetDownloadSettings();
            console.log('Chamando Python para restaurar configurações padrão...');
            alert('Configurações restauradas com sucesso!');
        } else {
            // Simulação para testes
            localStorage.removeItem('downloadSettings');
            alert('Configurações restauradas com sucesso!');
        }
    } catch (e) {
        console.error('Erro ao restaurar configurações:', e);
        alert(`Não foi possível restaurar as configurações: ${e.message}`);
    }
}

function clearCompletedDownloads() {
    if (confirm('Tem certeza que deseja limpar todos os downloads concluídos?')) {
        console.log('Limpando downloads concluídos');
        
        try {
            if (window.pyQtApi) {
                // window.pyQtApi.clearCompletedDownloads();
                console.log('Chamando Python para limpar downloads concluídos...');
                
                // Simulação para testes
                const completedRows = document.querySelectorAll('.downloads-table tbody tr .download-status.complete');
                completedRows.forEach(status => {
                    const row = status.closest('tr');
                    row.classList.add('removing');
                    setTimeout(() => {
                        row.remove();
                        updateStorageInfo();
                    }, 500);
                });
                
                alert('Downloads concluídos foram limpos com sucesso!');
            } else {
                // Simulação para testes
                const completedRows = document.querySelectorAll('.downloads-table tbody tr .download-status.complete');
                completedRows.forEach(status => {
                    const row = status.closest('tr');
                    row.classList.add('removing');
                    setTimeout(() => {
                        row.remove();
                        updateStorageInfo();
                    }, 500);
                });
                
                alert('Downloads concluídos foram limpos com sucesso!');
            }
        } catch (e) {
            console.error('Erro ao limpar downloads concluídos:', e);
            alert(`Não foi possível limpar os downloads: ${e.message}`);
        }
    }
}

function updateStorageInfo() {
    // Recalcula o espaço usado baseado nos itens visíveis
    // Na versão final, isso viria do Python
    let totalSize = 0;
    document.querySelectorAll('.downloads-table tbody tr:not([style*="display: none"])').forEach(row => {
        const sizeText = row.querySelector('td:nth-child(3)').textContent;
        const size = parseFloat(sizeText.match(/[\d.]+/)[0]);
        const unit = sizeText.match(/[A-Za-z]+/)[0];
        
        // Converter para MB
        switch (unit) {
            case 'KB':
                totalSize += size / 1024;
                break;
            case 'MB':
                totalSize += size;
                break;
            case 'GB':
                totalSize += size * 1024;
                break;
        }
    });
    
    // Atualizar a barra de armazenamento
    const storageBar = document.querySelector('.storage-used');
    const storageText = document.querySelector('.storage-text span');
    
    if (storageBar && storageText) {
        // Arredondar para 1 casa decimal
        totalSize = Math.round(totalSize * 10) / 10;
        
        // Atualizar a barra (considerando 1GB como 100%)
        const percentage = Math.min(totalSize / 10, 100);
        storageBar.style.width = `${percentage}%`;
        
        // Atualizar o texto
        storageText.textContent = `Espaço usado em Downloads: ${totalSize} MB de 1 GB`;
    }
}