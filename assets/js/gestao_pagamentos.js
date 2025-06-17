// Gestão de Pagamentos - JavaScript
class GestaoPayments {
    constructor() {
        this.payments = [
            {
                id: 'PAY-001',
                user: { name: 'João Silva', email: 'joao.silva@email.com', avatar: 'JS' },
                value: 99.90,
                method: 'pix',
                date: '2025-06-11 14:30:15',
                status: 'confirmed',
                ip: '192.168.1.100',
                transactionId: 'TXN-ABC123456789',
                gateway: 'Mercado Pago'
            },
            {
                id: 'PAY-002',
                user: { name: 'Maria Souza', email: 'maria.souza@email.com', avatar: 'MS' },
                value: 99.90,
                method: 'boleto',
                date: '2025-06-11 10:15:30',
                status: 'pending',
                ip: '192.168.1.105',
                transactionId: 'TXN-DEF987654321',
                gateway: 'Banco do Brasil'
            },
            {
                id: 'PAY-003',
                user: { name: 'Carlos Ferreira', email: 'carlos.ferreira@email.com', avatar: 'CF' },
                value: 99.90,
                method: 'credit',
                date: '2025-06-10 16:45:22',
                status: 'failed',
                ip: '192.168.1.110',
                transactionId: 'TXN-GHI456789123',
                gateway: 'Mercado Pago'
            },
            {
                id: 'PAY-004',
                user: { name: 'Ana Oliveira', email: 'ana.oliveira@email.com', avatar: 'AO' },
                value: 99.90,
                method: 'pix',
                date: '2025-06-10 08:20:45',
                status: 'refunded',
                ip: '192.168.1.120',
                transactionId: 'TXN-JKL789123456',
                gateway: 'Mercado Pago'
            },
            {
                id: 'PAY-005',
                user: { name: 'Pedro Santos', email: 'pedro.santos@email.com', avatar: 'PS' },
                value: 99.90,
                method: 'debit',
                date: '2025-06-09 19:30:10',
                status: 'confirmed',
                ip: '192.168.1.115',
                transactionId: 'TXN-MNO123456789',
                gateway: 'Cielo'
            },
            {
                id: 'PAY-006',
                user: { name: 'Luciana Costa', email: 'luciana.costa@email.com', avatar: 'LC' },
                value: 99.90,
                method: 'pix',
                date: '2025-06-09 14:15:33',
                status: 'confirmed',
                ip: '192.168.1.125',
                transactionId: 'TXN-PQR456789123',
                gateway: 'Mercado Pago'
            },
            {
                id: 'PAY-007',
                user: { name: 'Roberto Lima', email: 'roberto.lima@email.com', avatar: 'RL' },
                value: 99.90,
                method: 'boleto',
                date: '2025-06-08 11:22:17',
                status: 'cancelled',
                ip: '192.168.1.130',
                transactionId: 'TXN-STU789123456',
                gateway: 'Itaú'
            }
        ];
        
        this.filteredPayments = [...this.payments];
        this.currentPage = 1;
        this.itemsPerPage = 5;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.renderTable();
        this.updateStats();
    }
    
    setupEventListeners() {
        // Pesquisa
        const searchInput = document.getElementById('search-payments');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        }
        
        // Filtros
        const statusFilter = document.getElementById('filter-status');
        const methodFilter = document.getElementById('filter-method');
        const periodFilter = document.getElementById('filter-period');
        
        if (statusFilter) statusFilter.addEventListener('change', () => this.applyFilters());
        if (methodFilter) methodFilter.addEventListener('change', () => this.applyFilters());
        if (periodFilter) periodFilter.addEventListener('change', () => this.applyFilters());
        
        // Botões
        const exportBtn = document.querySelector('.export-button');
        const refreshBtn = document.querySelector('.refresh-button');
        
        if (exportBtn) exportBtn.addEventListener('click', () => this.exportToCSV());
        if (refreshBtn) refreshBtn.addEventListener('click', () => this.refreshData());
        
        // Modal
        const modal = document.getElementById('payment-details-modal');
        const closeModal = document.querySelector('.close-modal');
        
        if (closeModal) {
            closeModal.addEventListener('click', () => {
                if (modal) modal.style.display = 'none';
            });
        }
        
        // Fechar modal clicando fora
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
    
    handleSearch(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        
        if (term === '') {
            this.filteredPayments = [...this.payments];
        } else {
            this.filteredPayments = this.payments.filter(payment => 
                payment.id.toLowerCase().includes(term) ||
                payment.user.name.toLowerCase().includes(term) ||
                payment.user.email.toLowerCase().includes(term) ||
                payment.method.toLowerCase().includes(term) ||
                payment.status.toLowerCase().includes(term)
            );
        }
        
        this.applyFilters();
    }
    
    applyFilters() {
        const statusFilter = document.getElementById('filter-status')?.value || 'all';
        const methodFilter = document.getElementById('filter-method')?.value || 'all';
        const periodFilter = document.getElementById('filter-period')?.value || 'all';
        
        let filtered = [...this.filteredPayments];
        
        // Filtro por status
        if (statusFilter !== 'all') {
            filtered = filtered.filter(payment => payment.status === statusFilter);
        }
        
        // Filtro por método
        if (methodFilter !== 'all') {
            filtered = filtered.filter(payment => payment.method === methodFilter);
        }
        
        // Filtro por período
        if (periodFilter !== 'all') {
            const now = new Date();
            const paymentDate = new Date();
            
            filtered = filtered.filter(payment => {
                const pDate = new Date(payment.date);
                
                switch(periodFilter) {
                    case 'today':
                        return pDate.toDateString() === now.toDateString();
                    case 'yesterday':
                        const yesterday = new Date(now);
                        yesterday.setDate(yesterday.getDate() - 1);
                        return pDate.toDateString() === yesterday.toDateString();
                    case 'week':
                        const weekAgo = new Date(now);
                        weekAgo.setDate(weekAgo.getDate() - 7);
                        return pDate >= weekAgo;
                    case 'month':
                        const monthAgo = new Date(now);
                        monthAgo.setMonth(monthAgo.getMonth() - 1);
                        return pDate >= monthAgo;
                    default:
                        return true;
                }
            });
        }
        
        this.filteredPayments = filtered;
        this.currentPage = 1;
        this.renderTable();
        this.updatePagination();
    }
    
    renderTable() {
        const tbody = document.querySelector('.admin-payments-table tbody');
        if (!tbody) return;
        
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const pageData = this.filteredPayments.slice(startIndex, endIndex);
        
        tbody.innerHTML = '';
        
        if (pageData.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 40px; color: #7f8c8d;">
                        <i>Nenhum pagamento encontrado</i>
                    </td>
                </tr>
            `;
            return;
        }
        
        pageData.forEach(payment => {
            const row = this.createTableRow(payment);
            tbody.appendChild(row);
        });
    }
    
    createTableRow(payment) {
        const row = document.createElement('tr');
        
        const formattedDate = new Date(payment.date).toLocaleString('pt-BR');
        const formattedValue = payment.value.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
        
        row.innerHTML = `
            <td>${payment.id}</td>
            <td>
                <div class="user-payment-info">
                    <span class="user-avatar-small">${payment.user.avatar}</span>
                    <div class="user-details-small">
                        <span class="user-name-small">${payment.user.name}</span>
                        <span class="user-email-small">${payment.user.email}</span>
                    </div>
                </div>
            </td>
            <td class="payment-value">${formattedValue}</td>
            <td>
                <span class="payment-method ${payment.method}">${this.getMethodLabel(payment.method)}</span>
            </td>
            <td>${formattedDate}</td>
            <td>
                <span class="admin-payment-status ${payment.status}">${this.getStatusLabel(payment.status)}</span>
            </td>
            <td>
                <div class="admin-action-buttons">
                    <button class="admin-action-btn view" title="Ver Detalhes" onclick="gestaoPayments.showPaymentDetails('${payment.id}')">👁️</button>
                    ${this.getActionButtons(payment.status, payment.id)}
                </div>
            </td>
        `;
        
        return row;
    }
    
    getMethodLabel(method) {
        const labels = {
            'pix': 'PIX',
            'boleto': 'Boleto',
            'credit': 'Cartão',
            'debit': 'Débito'
        };
        return labels[method] || method;
    }
    
    getStatusLabel(status) {
        const labels = {
            'confirmed': 'Confirmado',
            'pending': 'Pendente',
            'failed': 'Falhou',
            'refunded': 'Reembolsado',
            'cancelled': 'Cancelado'
        };
        return labels[status] || status;
    }
    
    getActionButtons(status, paymentId) {
        switch(status) {
            case 'confirmed':
                return `
                    <button class="admin-action-btn refund" title="Reembolsar" onclick="gestaoPayments.refundPayment('${paymentId}')">💸</button>
                    <button class="admin-action-btn receipt" title="Comprovante" onclick="gestaoPayments.showReceipt('${paymentId}')">📄</button>
                `;
            case 'pending':
                return `
                    <button class="admin-action-btn approve" title="Aprovar" onclick="gestaoPayments.approvePayment('${paymentId}')">✅</button>
                    <button class="admin-action-btn reject" title="Rejeitar" onclick="gestaoPayments.rejectPayment('${paymentId}')">❌</button>
                `;
            case 'failed':
                return `
                    <button class="admin-action-btn retry" title="Tentar Novamente" onclick="gestaoPayments.retryPayment('${paymentId}')">🔄</button>
                    <button class="admin-action-btn contact" title="Contatar" onclick="gestaoPayments.contactUser('${paymentId}')">📞</button>
                `;
            default:
                return `<button class="admin-action-btn receipt" title="Comprovante" onclick="gestaoPayments.showReceipt('${paymentId}')">📄</button>`;
        }
    }
    
    showPaymentDetails(paymentId) {
        const payment = this.payments.find(p => p.id === paymentId);
        if (!payment) return;
        
        const modal = document.getElementById('payment-details-modal');
        const modalContent = modal.querySelector('.payment-modal-content');
        
        modalContent.innerHTML = `
            <span class="close-modal">&times;</span>
            <h4>Detalhes do Pagamento ${payment.id}</h4>
            <div class="payment-details-grid">
                <div class="detail-item">
                    <label>Usuário:</label>
                    <span>${payment.user.name} (${payment.user.email})</span>
                </div>
                <div class="detail-item">
                    <label>Valor:</label>
                    <span>${payment.value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</span>
                </div>
                <div class="detail-item">
                    <label>Método:</label>
                    <span>${this.getMethodLabel(payment.method)}</span>
                </div>
                <div class="detail-item">
                    <label>Status:</label>
                    <span class="admin-payment-status ${payment.status}">${this.getStatusLabel(payment.status)}</span>
                </div>
                <div class="detail-item">
                    <label>Data/Hora:</label>
                    <span>${new Date(payment.date).toLocaleString('pt-BR')}</span>
                </div>
                <div class="detail-item">
                    <label>IP do Cliente:</label>
                    <span>${payment.ip}</span>
                </div>
                <div class="detail-item">
                    <label>ID da Transação:</label>
                    <span>${payment.transactionId}</span>
                </div>
                <div class="detail-item">
                    <label>Gateway:</label>
                    <span>${payment.gateway}</span>
                </div>
            </div>
            <div class="modal-actions">
                <button class="modal-btn approve" onclick="gestaoPayments.approvePayment('${payment.id}')">Aprovar</button>
                <button class="modal-btn refund" onclick="gestaoPayments.refundPayment('${payment.id}')">Reembolsar</button>
                <button class="modal-btn reject" onclick="gestaoPayments.rejectPayment('${payment.id}')">Rejeitar</button>
                <button class="modal-btn cancel" onclick="gestaoPayments.closeModal()">Fechar</button>
            </div>
        `;
        
        // Re-adicionar event listener para o botão de fechar
        modalContent.querySelector('.close-modal').addEventListener('click', () => {
            modal.style.display = 'none';
        });
        
        modal.style.display = 'block';
    }
    
    closeModal() {
        const modal = document.getElementById('payment-details-modal');
        if (modal) modal.style.display = 'none';
    }
    
    exportToCSV() {
        const headers = ['ID', 'Usuário', 'Email', 'Valor', 'Método', 'Data/Hora', 'Status', 'IP', 'ID Transação', 'Gateway'];
        
        let csvContent = headers.join(',') + '\n';
        
        this.filteredPayments.forEach(payment => {
            const row = [
                payment.id,
                `"${payment.user.name}"`,
                payment.user.email,
                payment.value.toFixed(2).replace('.', ','),
                this.getMethodLabel(payment.method),
                `"${new Date(payment.date).toLocaleString('pt-BR')}"`,
                this.getStatusLabel(payment.status),
                payment.ip,
                payment.transactionId,
                `"${payment.gateway}"`
            ];
            csvContent += row.join(',') + '\n';
        });
        
        // Criar e baixar arquivo
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', `pagamentos_${new Date().toISOString().slice(0, 10)}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        
        this.showNotification('Arquivo CSV exportado com sucesso!', 'success');
    }
    
    refreshData() {
        // Simular carregamento
        this.showNotification('Atualizando dados...', 'info');
        
        // Simular delay de requisição
        setTimeout(() => {
            // Aqui você faria uma requisição real para buscar dados atualizados
            // Por enquanto, vamos apenas re-renderizar
            this.renderTable();
            this.updateStats();
            this.showNotification('Dados atualizados com sucesso!', 'success');
        }, 1000);
    }
    
    updateStats() {
        // Simular estatísticas baseadas nos dados filtrados
        const today = new Date().toDateString();
        const todayPayments = this.payments.filter(p => new Date(p.date).toDateString() === today);
        const pendingPayments = this.payments.filter(p => p.status === 'pending');
        const confirmedPayments = this.payments.filter(p => p.status === 'confirmed');
        
        const todayTotal = todayPayments.reduce((sum, p) => sum + p.value, 0);
        const pendingTotal = pendingPayments.reduce((sum, p) => sum + p.value, 0);
        const monthTotal = this.payments.reduce((sum, p) => sum + p.value, 0);
        const successRate = (confirmedPayments.length / this.payments.length) * 100;
        
        // Atualizar cards de estatísticas
        this.updateStatCard(0, todayTotal, todayPayments.length);
        this.updateStatCard(1, pendingTotal, pendingPayments.length);
        this.updateStatCard(2, monthTotal, this.payments.length);
        this.updateStatCard(3, successRate.toFixed(1) + '%', 'dos pagamentos');
    }
    
    updateStatCard(index, value, count) {
        const cards = document.querySelectorAll('.stat-card');
        if (cards[index]) {
            const numberElement = cards[index].querySelector('.stat-number');
            const countElement = cards[index].querySelector('.stat-count');
            
            if (numberElement) {
                if (typeof value === 'number' && index < 3) {
                    numberElement.textContent = value.toLocaleString('pt-BR', {
                        style: 'currency',
                        currency: 'BRL'
                    });
                } else {
                    numberElement.textContent = value;
                }
            }
            
            if (countElement) {
                countElement.textContent = typeof count === 'number' ? `${count} pagamentos` : count;
            }
        }
    }
    
    updatePagination() {
        const totalPages = Math.ceil(this.filteredPayments.length / this.itemsPerPage);
        const pageInfo = document.querySelector('.page-info');
        
        if (pageInfo) {
            pageInfo.textContent = `Página ${this.currentPage} de ${totalPages} (${this.filteredPayments.length} registros)`;
        }
    }
    
    // Métodos para ações dos pagamentos
    approvePayment(paymentId) {
        this.updatePaymentStatus(paymentId, 'confirmed');
        this.showNotification('Pagamento aprovado com sucesso!', 'success');
    }
    
    rejectPayment(paymentId) {
        this.updatePaymentStatus(paymentId, 'failed');
        this.showNotification('Pagamento rejeitado!', 'warning');
    }
    
    refundPayment(paymentId) {
        this.updatePaymentStatus(paymentId, 'refunded');
        this.showNotification('Reembolso processado!', 'info');
    }
    
    retryPayment(paymentId) {
        this.updatePaymentStatus(paymentId, 'pending');
        this.showNotification('Pagamento enviado para nova tentativa!', 'info');
    }
    
    contactUser(paymentId) {
        const payment = this.payments.find(p => p.id === paymentId);
        if (payment) {
            this.showNotification(`Contato enviado para ${payment.user.email}`, 'info');
        }
    }
    
    showReceipt(paymentId) {
        this.showNotification('Comprovante baixado!', 'success');
    }
    
    updatePaymentStatus(paymentId, newStatus) {
        const payment = this.payments.find(p => p.id === paymentId);
        if (payment) {
            payment.status = newStatus;
            this.renderTable();
            this.updateStats();
            this.closeModal();
        }
    }
    
    showNotification(message, type = 'info') {
        // Criar elemento de notificação
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Estilos inline para a notificação
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 6px;
            color: white;
            z-index: 10000;
            font-weight: 500;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideIn 0.3s ease;
        `;
        
        // Cores baseadas no tipo
        const colors = {
            'success': '#27ae60',
            'error': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db'
        };
        
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Adicionar ao body
        document.body.appendChild(notification);
        
        // Remover após 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// CSS adicional para animações de notificação
const notificationStyles = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;

// Adicionar estilos ao head
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Inicializar quando a página carregar
let gestaoPayments;

document.addEventListener('DOMContentLoaded', () => {
    gestaoPayments = new GestaoPayments();
});

// Função global para mostrar seção (se necessário)
if (typeof showSection === 'function') {
    const originalShowSection = showSection;
    showSection = function(sectionId) {
        originalShowSection(sectionId);
        if (sectionId === 'gestao_pagamentos' && !gestaoPayments) {
            gestaoPayments = new GestaoPayments();
        }
    };
}