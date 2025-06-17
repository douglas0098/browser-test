document.addEventListener('DOMContentLoaded', function() {
    // Verificar se já existem datas salvas
    const lastClear = localStorage.getItem('lastCacheClear');
    const autoCleanEnabled = localStorage.getItem('autoCleanEnabled');
    const clearIntervalDays = localStorage.getItem('clearIntervalDays');
    
    // Configurar checkbox de limpeza automática
    if (autoCleanEnabled !== null) {
        document.getElementById('autoClear').checked = autoCleanEnabled === 'true';
    } else {
        localStorage.setItem('autoCleanEnabled', 'true');
    }
    
    // Configurar intervalo de limpeza
    if (clearIntervalDays !== null) {
        document.getElementById('clearInterval').value = clearIntervalDays;
    } else {
        localStorage.setItem('clearIntervalDays', '7');
    }
    
    // Configurar datas
    if (lastClear) {
        const lastClearDate = new Date(parseInt(lastClear));
        document.getElementById('lastClearDate').textContent = formatDate(lastClearDate);
        
        // Calcular próxima data de limpeza
        const interval = parseInt(localStorage.getItem('clearIntervalDays') || '7');
        const nextClearDate = new Date(lastClearDate);
        nextClearDate.setDate(nextClearDate.getDate() + interval);
        document.getElementById('nextClearDate').textContent = formatDate(nextClearDate);
        
        // Verificar se é hora de limpar automaticamente
        if (document.getElementById('autoClear').checked) {
            checkAutoClear();
        }
    }
    
    // Adicionar listeners para mudanças nas configurações
    document.getElementById('autoClear').addEventListener('change', function() {
        localStorage.setItem('autoCleanEnabled', this.checked);
        updateNextClearDate();
    });
    
    document.getElementById('clearInterval').addEventListener('change', function() {
        localStorage.setItem('clearIntervalDays', this.value);
        updateNextClearDate();
    });
});

// Função para formatar data
function formatDate(date) {
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Função para atualizar a próxima data de limpeza
function updateNextClearDate() {
    const lastClear = localStorage.getItem('lastCacheClear');
    
    if (lastClear) {
        const lastClearDate = new Date(parseInt(lastClear));
        const interval = parseInt(document.getElementById('clearInterval').value);
        const nextClearDate = new Date(lastClearDate);
        nextClearDate.setDate(nextClearDate.getDate() + interval);
        document.getElementById('nextClearDate').textContent = formatDate(nextClearDate);
    } else {
        const today = new Date();
        const interval = parseInt(document.getElementById('clearInterval').value);
        const nextClearDate = new Date();
        nextClearDate.setDate(today.getDate() + interval);
        document.getElementById('nextClearDate').textContent = formatDate(nextClearDate);
    }
}

// Função para verificar se é hora de limpar automaticamente
function checkAutoClear() {
    const lastClear = localStorage.getItem('lastCacheClear');
    
    if (lastClear) {
        const lastClearDate = new Date(parseInt(lastClear));
        const interval = parseInt(localStorage.getItem('clearIntervalDays') || '7');
        const today = new Date();
        const nextClearDate = new Date(lastClearDate);
        nextClearDate.setDate(nextClearDate.getDate() + interval);
        
        // Se a data atual é maior que a próxima data de limpeza
        if (today >= nextClearDate) {
            clearAll(true); // Limpar automaticamente
        }
    }
}

// Função para limpar o cache
function clearCache() {
    if (confirm('Tem certeza que deseja limpar o cache do navegador?')) {
        try {
            // Limpar cache usando a API Cache
            if ('caches' in window) {
                caches.keys().then(cacheNames => {
                    return Promise.all(
                        cacheNames.map(cacheName => {
                            return caches.delete(cacheName);
                        })
                    );
                });
            }
            
            // Limpar localStorage (exceto configurações de limpeza)
            const preserveKeys = ['lastCacheClear', 'autoCleanEnabled', 'clearIntervalDays'];
            Object.keys(localStorage).forEach(key => {
                if (!preserveKeys.includes(key)) {
                    localStorage.removeItem(key);
                }
            });
            
            // Limpar sessionStorage
            sessionStorage.clear();
            
            // Atualizar data da última limpeza
            updateLastClearDate();
            
            alert('Cache limpo com sucesso!');
        } catch (error) {
            console.error('Erro ao limpar cache:', error);
            alert('Ocorreu um erro ao limpar o cache. Veja o console para mais detalhes.');
        }
    }
}

// Função para limpar os cookies
function clearCookies() {
    if (confirm('Tem certeza que deseja limpar os cookies do navegador?')) {
        try {
            // Obter todos os cookies e exclui-los
            const cookies = document.cookie.split(';');
            
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i];
                const eqPos = cookie.indexOf('=');
                const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
                document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
            }
            
            // Atualizar data da última limpeza
            updateLastClearDate();
            
            alert('Cookies limpos com sucesso!');
        } catch (error) {
            console.error('Erro ao limpar cookies:', error);
            alert('Ocorreu um erro ao limpar os cookies. Veja o console para mais detalhes.');
        }
    }
}

// Função para limpar tudo
function clearAll(automatic = false) {
    if (automatic || confirm('Tem certeza que deseja limpar todo o cache e cookies do navegador?')) {
        try {
            // Limpar cache
            if ('caches' in window) {
                caches.keys().then(cacheNames => {
                    return Promise.all(
                        cacheNames.map(cacheName => {
                            return caches.delete(cacheName);
                        })
                    );
                });
            }
            
            // Limpar localStorage (exceto configurações de limpeza)
            const preserveKeys = ['lastCacheClear', 'autoCleanEnabled', 'clearIntervalDays'];
            Object.keys(localStorage).forEach(key => {
                if (!preserveKeys.includes(key)) {
                    localStorage.removeItem(key);
                }
            });
            
            // Limpar sessionStorage
            sessionStorage.clear();
            
            // Limpar cookies
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i];
                const eqPos = cookie.indexOf('=');
                const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
                document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
            }
            
            // Atualizar data da última limpeza
            updateLastClearDate();
            
            if (!automatic) {
                alert('Cache e cookies limpos com sucesso!');
            }
        } catch (error) {
            console.error('Erro ao limpar cache e cookies:', error);
            if (!automatic) {
                alert('Ocorreu um erro ao limpar o cache e cookies. Veja o console para mais detalhes.');
            }
        }
    }
}

// Função para atualizar a data da última limpeza
function updateLastClearDate() {
    const now = new Date();
    localStorage.setItem('lastCacheClear', now.getTime().toString());
    document.getElementById('lastClearDate').textContent = formatDate(now);
    
    // Atualizar a próxima data de limpeza
    updateNextClearDate();
}

// Verificar automaticamente a cada 24 horas se é hora de limpar
setInterval(function() {
    if (document.getElementById('autoClear').checked) {
        checkAutoClear();
    }
}, 86400000); // 24 horas em milissegundos

// Também verificar quando a página for carregada
window.addEventListener('load', function() {
    if (document.getElementById('autoClear').checked) {
        checkAutoClear();
    }
});