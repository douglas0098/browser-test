// Gestão de Gastos com Gastos Fixos - JavaScript (VERSÃO CORRIGIDA)
class GestaoGastos {
    constructor() {
        this.gastos = JSON.parse(localStorage.getItem('gastos')) || [];
        this.gastosFixos = JSON.parse(localStorage.getItem('gastosFixos')) || [];
        this.orcamentos = JSON.parse(localStorage.getItem('orcamentos')) || {
            infraestrutura: 5000,
            apis: 3000,
            licencas: 2000,
            marketing: 2500,
            outros: 1500
        };
        this.isDragging = false;
        this.currentModal = null;
        this.offset = { x: 0, y: 0 };
        this.init();
    }

    init() {
        // Garantir que modal está fechado na inicialização
        this.ensureModalIsClosed();
        this.bindEvents();
        this.processRecurringExpenses();
        this.renderDashboard();
        this.renderTable();
        this.renderBudgetOverview();
        this.renderRecurringExpenses();
        this.updateChart();
        
        console.log('✅ GestaoGastos inicializada');
    }

    ensureModalIsClosed() {
        const modal = document.getElementById('expense-modal');
        if (modal) {
            modal.style.display = 'none';
            modal.style.zIndex = '99999';
        }
        document.body.style.overflow = 'auto';
    }

    bindEvents() {
        console.log('🔗 Configurando event listeners...');

        // Aguardar um pouco para garantir que os elementos estão no DOM
        setTimeout(() => {
            // Botão adicionar gasto
            const addBtn = document.querySelector('.add-expense-btn');
            console.log('🔍 Botão adicionar gasto:', addBtn);
            
            if (addBtn) {
                addBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('🔵 Clique no botão adicionar gasto detectado!');
                    this.openModal();
                });
                console.log('✅ Event listener adicionado ao botão adicionar gasto');
            } else {
                console.warn('⚠️ Botão adicionar gasto não encontrado');
            }

            // Botão adicionar gasto fixo
            const addRecurringBtn = document.querySelector('.add-recurring-btn');
            console.log('🔍 Botão adicionar gasto fixo:', addRecurringBtn);
            
            if (addRecurringBtn) {
                addRecurringBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('🔵 Clique no botão adicionar gasto fixo detectado!');
                    this.openModal();
                });
                console.log('✅ Event listener adicionado ao botão adicionar gasto fixo');
            } else {
                console.warn('⚠️ Botão adicionar gasto fixo não encontrado');
            }

            // Modal events
            const modal = document.getElementById('expense-modal');
            const closeBtn = modal?.querySelector('.close-modal');
            const cancelBtn = modal?.querySelector('.cancel-btn');
            const form = document.getElementById('expense-form');

            if (closeBtn) {
                closeBtn.addEventListener('click', () => this.closeModal());
            }
            if (cancelBtn) {
                cancelBtn.addEventListener('click', () => this.closeModal());
            }
            if (form) {
                form.addEventListener('submit', (e) => this.handleSubmit(e));
            }

            // Fechar modal clicando no fundo
            if (modal) {
                modal.addEventListener('click', (e) => {
                    if (e.target === modal && !this.isDragging) {
                        this.closeModal();
                    }
                });
            }

        }, 500); // Aguardar 500ms para garantir que DOM está pronto

        // Resto dos eventos...
        const isRecurringCheckbox = document.getElementById('is-recurring');
        if (isRecurringCheckbox) {
            isRecurringCheckbox.addEventListener('change', (e) => {
                this.toggleRecurringDetails(e.target.checked);
            });
        }

        const recurringDay = document.getElementById('recurring-day');
        if (recurringDay) {
            recurringDay.addEventListener('change', () => this.updateNextRecurringDate());
        }

        // Filtros
        const searchInput = document.getElementById('search-expenses');
        const categoryFilter = document.getElementById('filter-category');
        const periodFilter = document.getElementById('filter-period');

        if (searchInput) searchInput.addEventListener('input', () => this.applyFilters());
        if (categoryFilter) categoryFilter.addEventListener('change', () => this.applyFilters());
        if (periodFilter) periodFilter.addEventListener('change', () => this.applyFilters());

        // Botões de ação da tabela (delegação de eventos)
        document.addEventListener('click', (e) => {
            if (e.target.closest('.action-btn')) {
                const btn = e.target.closest('.action-btn');
                const row = btn.closest('tr');
                const gastoId = row?.dataset.gastoId;

                if (gastoId) {
                    if (btn.classList.contains('view')) {
                        this.viewExpense(gastoId);
                    } else if (btn.classList.contains('edit')) {
                        this.editExpense(gastoId);
                    } else if (btn.classList.contains('delete')) {
                        this.deleteExpense(gastoId);
                    }
                }
            }

            // Ações para gastos fixos
            if (e.target.closest('.recurring-action-btn')) {
                const btn = e.target.closest('.recurring-action-btn');
                const item = btn.closest('.recurring-expense-item');
                const recurringId = item?.dataset.recurringId;

                if (recurringId) {
                    if (btn.classList.contains('edit')) {
                        this.editRecurringExpense(recurringId);
                    } else if (btn.classList.contains('toggle')) {
                        this.toggleRecurringExpense(recurringId);
                    } else if (btn.classList.contains('delete')) {
                        this.deleteRecurringExpense(recurringId);
                    }
                }
            }
        });
    }

    openModal(gastoId = null) {
        console.log('🔵 Tentando abrir modal...', gastoId);

        const modal = document.getElementById('expense-modal');
        if (!modal) {
            console.error('❌ Modal não encontrado no DOM!');
            console.log('🔍 Elementos no DOM:', document.querySelectorAll('[id*="modal"]'));
            return;
        }

        console.log('✅ Modal encontrado:', modal);

        const form = document.getElementById('expense-form');
        const title = modal.querySelector('h4');

        if (gastoId) {
            const gasto = this.gastos.find(g => g.id === gastoId);
            if (gasto) {
                title.textContent = 'Editar Gasto';
                this.fillForm(gasto);
                form.dataset.editId = gastoId;
            }
        } else {
            title.textContent = 'Adicionar Novo Gasto';
            if (form) {
                form.reset();
                delete form.dataset.editId;
                delete form.dataset.editRecurringId;
            }
            
            // Definir data atual
            const dateInput = document.getElementById('expense-date');
            if (dateInput) {
                const today = new Date().toISOString().split('T')[0];
                dateInput.value = today;
            }
            
            // Reset recurring options
            const recurringCheckbox = document.getElementById('is-recurring');
            if (recurringCheckbox) {
                recurringCheckbox.checked = false;
                this.toggleRecurringDetails(false);
            }
        }

        // Mostrar modal com z-index alto
        modal.style.zIndex = '99999';
        modal.style.display = 'flex';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        
        document.body.style.overflow = 'hidden';
        
        // Posicionar modal content
        const modalContent = modal.querySelector('.expense-modal-content');
        if (modalContent) {
            modalContent.style.zIndex = '100000';
            modalContent.style.position = 'fixed';
            
            // Posicionamento seguro
            const minTop = 120;
            const minLeft = 50;
            const maxWidth = Math.min(520, window.innerWidth - 100);
            const maxHeight = Math.min(600, window.innerHeight - 200);
            
            const randomX = Math.random() * (window.innerWidth - maxWidth - 100) + 50;
            const randomY = Math.random() * (window.innerHeight - maxHeight - 200) + 120;
            
            modalContent.style.left = Math.max(minLeft, randomX) + 'px';
            modalContent.style.top = Math.max(minTop, randomY) + 'px';
            modalContent.style.width = maxWidth + 'px';
            modalContent.style.maxHeight = maxHeight + 'px';
            
            // Tornar arrastável
            setTimeout(() => this.makeDraggable(), 100);
        }
        
        // Focar no primeiro campo
        setTimeout(() => {
            const firstInput = document.getElementById('expense-description');
            if (firstInput) {
                firstInput.focus();
            }
        }, 200);

        console.log('✅ Modal aberto com sucesso!');
    }

    closeModal() {
        console.log('🔴 Fechando modal...');

        const modal = document.getElementById('expense-modal');
        if (!modal) return;

        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        
        // Limpar dados do formulário
        const form = document.getElementById('expense-form');
        if (form) {
            form.reset();
            delete form.dataset.editId;
            delete form.dataset.editRecurringId;
        }
        
        // Reset recurring details
        const recurringCheckbox = document.getElementById('is-recurring');
        if (recurringCheckbox) {
            recurringCheckbox.checked = false;
            this.toggleRecurringDetails(false);
        }

        // Reset dragging state
        this.isDragging = false;
        this.currentModal = null;

        console.log('✅ Modal fechado');
    }

    makeDraggable() {
        const modal = document.querySelector('.expense-modal-content');
        if (!modal) return;

        // Adicionar área de arrastar e indicador de posição
        if (!modal.querySelector('.modal-header-drag')) {
            const dragArea = document.createElement('div');
            dragArea.className = 'modal-header-drag';
            modal.insertBefore(dragArea, modal.firstChild);
            
            const positionIndicator = document.createElement('div');
            positionIndicator.className = 'modal-position-indicator';
            positionIndicator.textContent = 'X: 0, Y: 0';
            modal.appendChild(positionIndicator);
        }

        const dragArea = modal.querySelector('.modal-header-drag');

        // Eventos de mouse para arrastar
        dragArea.addEventListener('mousedown', (e) => this.startDrag(e));
        document.addEventListener('mousemove', (e) => this.drag(e));
        document.addEventListener('mouseup', () => this.stopDrag());

        // Eventos de toque para dispositivos móveis
        dragArea.addEventListener('touchstart', (e) => this.startDragTouch(e), { passive: false });
        document.addEventListener('touchmove', (e) => this.dragTouch(e), { passive: false });
        document.addEventListener('touchend', () => this.stopDrag());

        // Duplo clique para centralizar
        modal.addEventListener('dblclick', () => this.centerModal());
    }

    startDrag(e) {
        this.isDragging = true;
        this.currentModal = document.querySelector('.expense-modal-content');
        
        const rect = this.currentModal.getBoundingClientRect();
        this.offset.x = e.clientX - rect.left;
        this.offset.y = e.clientY - rect.top;
        
        this.currentModal.classList.add('dragging');
        this.updatePositionIndicator(rect.left, rect.top);
        
        e.preventDefault();
        e.stopPropagation();
    }

    startDragTouch(e) {
        const touch = e.touches[0];
        this.isDragging = true;
        this.currentModal = document.querySelector('.expense-modal-content');
        
        const rect = this.currentModal.getBoundingClientRect();
        this.offset.x = touch.clientX - rect.left;
        this.offset.y = touch.clientY - rect.top;
        
        this.currentModal.classList.add('dragging');
        this.updatePositionIndicator(rect.left, rect.top);
        
        e.preventDefault();
        e.stopPropagation();
    }

    drag(e) {
        if (!this.isDragging || !this.currentModal) return;

        const x = e.clientX - this.offset.x;
        const y = e.clientY - this.offset.y;
        
        const minTop = 60;
        const minLeft = 10;
        const minRight = 10;
        const minBottom = 10;
        
        const maxX = window.innerWidth - this.currentModal.offsetWidth - minRight;
        const maxY = window.innerHeight - this.currentModal.offsetHeight - minBottom;
        
        const boundedX = Math.max(minLeft, Math.min(x, maxX));
        const boundedY = Math.max(minTop, Math.min(y, maxY));
        
        this.currentModal.style.left = boundedX + 'px';
        this.currentModal.style.top = boundedY + 'px';
        
        this.updatePositionIndicator(boundedX, boundedY);
        
        e.preventDefault();
    }

    dragTouch(e) {
        if (!this.isDragging || !this.currentModal) return;

        const touch = e.touches[0];
        const x = touch.clientX - this.offset.x;
        const y = touch.clientY - this.offset.y;
        
        const minTop = 80;
        const minLeft = 10;
        const minRight = 10;
        const minBottom = 10;
        
        const maxX = window.innerWidth - this.currentModal.offsetWidth - minRight;
        const maxY = window.innerHeight - this.currentModal.offsetHeight - minBottom;
        
        const boundedX = Math.max(minLeft, Math.min(x, maxX));
        const boundedY = Math.max(minTop, Math.min(y, maxY));
        
        this.currentModal.style.left = boundedX + 'px';
        this.currentModal.style.top = boundedY + 'px';
        
        this.updatePositionIndicator(boundedX, boundedY);
        
        e.preventDefault();
    }

    stopDrag() {
        if (!this.isDragging) return;
        
        this.isDragging = false;
        
        if (this.currentModal) {
            this.currentModal.classList.remove('dragging');
            this.currentModal.classList.add('drop-animation');
            
            setTimeout(() => {
                this.currentModal.classList.remove('drop-animation');
            }, 300);
        }
        
        this.currentModal = null;
    }

    updatePositionIndicator(x, y) {
        const positionIndicator = document.querySelector('.modal-position-indicator');
        if (positionIndicator) {
            positionIndicator.textContent = `X: ${Math.round(x)}, Y: ${Math.round(y)}`;
        }
    }

    centerModal() {
        const modal = document.querySelector('.expense-modal-content');
        if (modal) {
            const minTop = 80;
            const centerX = (window.innerWidth - modal.offsetWidth) / 2;
            const centerY = Math.max(minTop, (window.innerHeight - modal.offsetHeight) / 2);
            
            modal.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
            modal.style.left = centerX + 'px';
            modal.style.top = centerY + 'px';
            
            setTimeout(() => {
                modal.style.transition = '';
            }, 500);
        }
    }

    // Resto dos métodos permanecem iguais...
    fillForm(gasto) {
        document.getElementById('expense-description').value = gasto.descricao;
        document.getElementById('expense-category').value = gasto.categoria;
        document.getElementById('expense-amount').value = gasto.valor;
        document.getElementById('expense-date').value = gasto.data;
        document.getElementById('expense-responsible').value = gasto.responsavel;
        document.getElementById('expense-notes').value = gasto.observacoes || '';
    }

    toggleRecurringDetails(show) {
        const details = document.getElementById('recurring-details');
        if (details) {
            details.style.display = show ? 'block' : 'none';
            if (show) {
                this.updateNextRecurringDate();
            }
        }
    }

    updateNextRecurringDate() {
        const daySelect = document.getElementById('recurring-day');
        const nextDateInput = document.getElementById('recurring-next-date');
        
        if (!daySelect || !nextDateInput) return;
        
        const day = parseInt(daySelect.value);
        const nextDate = new Date();
        
        if (day === 30) {
            nextDate.setMonth(nextDate.getMonth() + 1, 0);
        } else {
            if (nextDate.getDate() > day) {
                nextDate.setMonth(nextDate.getMonth() + 1);
            }
            nextDate.setDate(day);
        }
        
        nextDateInput.value = nextDate.toISOString().split('T')[0];
    }

    handleSubmit(e) {
        e.preventDefault();
        
        const form = e.target;
        const editId = form.dataset.editId;
        const editRecurringId = form.dataset.editRecurringId;
        const isRecurring = document.getElementById('is-recurring').checked;
        
        const gastoData = {
            id: editId || 'gasto_' + Date.now(),
            descricao: document.getElementById('expense-description').value,
            categoria: document.getElementById('expense-category').value,
            valor: parseFloat(document.getElementById('expense-amount').value),
            data: document.getElementById('expense-date').value,
            responsavel: document.getElementById('expense-responsible').value,
            observacoes: document.getElementById('expense-notes').value,
            status: 'approved',
            criadoEm: editId ? this.gastos.find(g => g.id === editId)?.criadoEm : new Date().toISOString()
        };

        if (editRecurringId) {
            const index = this.gastosFixos.findIndex(gf => gf.id === editRecurringId);
            if (index !== -1) {
                this.gastosFixos[index] = {
                    ...this.gastosFixos[index],
                    ...gastoData,
                    recurringDay: parseInt(document.getElementById('recurring-day').value),
                    duration: document.getElementById('recurring-duration').value,
                    nextDate: document.getElementById('recurring-next-date').value
                };
                this.showNotification('Gasto fixo atualizado com sucesso!', 'success');
            }
        } else if (isRecurring && !editId) {
            const recurringData = {
                id: 'recurring_' + Date.now(),
                ...gastoData,
                recurringDay: parseInt(document.getElementById('recurring-day').value),
                duration: document.getElementById('recurring-duration').value,
                nextDate: document.getElementById('recurring-next-date').value,
                active: true,
                createdAt: new Date().toISOString()
            };
            
            this.gastosFixos.push(recurringData);
            this.showNotification('Gasto fixo cadastrado com sucesso!', 'success');
        } else {
            if (editId) {
                const index = this.gastos.findIndex(g => g.id === editId);
                if (index !== -1) {
                    this.gastos[index] = gastoData;
                    this.showNotification('Gasto atualizado com sucesso!', 'success');
                }
            } else {
                this.gastos.push(gastoData);
                this.showNotification('Gasto adicionado com sucesso!', 'success');
            }
        }

        this.saveToStorage();
        this.renderDashboard();
        this.renderTable();
        this.renderBudgetOverview();
        this.renderRecurringExpenses();
        this.updateChart();
        this.closeModal();
    }

    // Adicionar outros métodos necessários...
    processRecurringExpenses() {
        // Implementação completa aqui...
    }

    renderDashboard() {
        // Implementação completa aqui...
    }

    renderTable() {
        const tbody = document.querySelector('.expenses-table tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (this.gastos.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="7" style="text-align: center; padding: 40px; color: #7f8c8d;">
                    <div>
                        <div style="font-size: 48px; margin-bottom: 20px;">📊</div>
                        <h5>Nenhum gasto cadastrado</h5>
                        <p>Clique em "Adicionar Gasto" para começar</p>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
            return;
        }

        // Resto da implementação...
    }

    renderBudgetOverview() {
        // Implementação aqui...
    }

    renderRecurringExpenses() {
        // Implementação aqui...
    }

    updateChart() {
        // Implementação aqui...
    }

    applyFilters() {
        // Implementação aqui...
    }

    deleteExpense(gastoId) {
        if (confirm('Tem certeza que deseja excluir este gasto?')) {
            this.gastos = this.gastos.filter(g => g.id !== gastoId);
            this.saveToStorage();
            this.renderDashboard();
            this.renderTable();
            this.renderBudgetOverview();
            this.updateChart();
            this.showNotification('Gasto excluído com sucesso!', 'success');
        }
    }

    editExpense(gastoId) {
        this.openModal(gastoId);
    }

    viewExpense(gastoId) {
        const gasto = this.gastos.find(g => g.id === gastoId);
        if (gasto) {
            const isRecurring = gasto.recurringId ? ' (Gerado automaticamente)' : '';
            alert(`
Descrição: ${gasto.descricao}
Categoria: ${gasto.categoria}
Valor: R$ ${gasto.valor.toFixed(2)}
Data: ${new Date(gasto.data).toLocaleDateString('pt-BR')}
Responsável: ${gasto.responsavel}
Observações: ${gasto.observacoes || 'Nenhuma'}
Status: ${gasto.status}${isRecurring}
            `);
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '600',
            zIndex: '999999',
            transform: 'translateX(400px)',
            transition: 'all 0.3s ease'
        });

        if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #27ae60 0%, #229954 100%)';
        } else if (type === 'error') {
            notification.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
        } else {
            notification.style.background = 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)';
        }

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    saveToStorage() {
        localStorage.setItem('gastos', JSON.stringify(this.gastos));
        localStorage.setItem('gastosFixos', JSON.stringify(this.gastosFixos));
        localStorage.setItem('orcamentos', JSON.stringify(this.orcamentos));
    }
}

// Função global para compatibilidade
function openModal() {
    console.log('📞 Função global openModal() chamada');
    if (window.gestaoGastosInstance) {
        window.gestaoGastosInstance.openModal();
    } else {
        console.warn('⚠️ gestaoGastosInstance não encontrada');
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM carregado, preparando GestaoGastos...');
    
    let gestaoGastosInstance = null;
    
    const originalShowSection = window.showSection;
    window.showSection = function(sectionId) {
        console.log(`📄 Mostrando seção: ${sectionId}`);
        
        if (originalShowSection) {
            originalShowSection(sectionId);
        }
        
        if (sectionId === 'gestao_gastos') {
            if (!gestaoGastosInstance) {
                console.log('🔄 Inicializando GestaoGastos...');
                gestaoGastosInstance = new GestaoGastos();
                window.gestaoGastosInstance = gestaoGastosInstance;
                console.log('✅ GestaoGastos inicializada');
            }
        }
    };
    
    // Verificar se seção já está ativa
    const gestaoGastosSection = document.getElementById('gestao_gastos');
    if (gestaoGastosSection && (gestaoGastosSection.style.display !== 'none' || gestaoGastosSection.classList.contains('active'))) {
        console.log('🔄 Seção gestão_gastos já está ativa, inicializando...');
        gestaoGastosInstance = new GestaoGastos();
        window.gestaoGastosInstance = gestaoGastosInstance;
    }
});

// Função global para abrir modal (REMOVER para evitar abertura automática)
// function openModal() {
//     if (window.gestaoGastosInstance) {
//         window.gestaoGastosInstance.openModal();
//     }
// }

// Inicializar quando a seção for mostrada (SEM abrir modal automaticamente)
document.addEventListener('DOMContentLoaded', function() {
    let gestaoGastosInstance = null;
    
    // Verificar se já existe a função showSection, senão criar
    const originalShowSection = window.showSection;
    window.showSection = function(sectionId) {
        if (originalShowSection) {
            originalShowSection(sectionId);
        }
        
        if (sectionId === 'gestao_gastos') {
            if (!gestaoGastosInstance) {
                gestaoGastosInstance = new GestaoGastos();
                window.gestaoGastosInstance = gestaoGastosInstance;
                console.log('✅ GestaoGastos inicializada SEM abrir modal');
            }
        }
    };
    
    // Se a seção já estiver visível no carregamento (SEM abrir modal)
    const gestaoGastosSection = document.getElementById('gestao_gastos');
    if (gestaoGastosSection && gestaoGastosSection.classList.contains('active')) {
        gestaoGastosInstance = new GestaoGastos();
        window.gestaoGastosInstance = gestaoGastosInstance;
        console.log('✅ GestaoGastos inicializada no carregamento SEM abrir modal');
    }
});

// Função global para abrir modal (para compatibilidade com onclick)
function openModal() {
    if (window.gestaoGastosInstance) {
        window.gestaoGastosInstance.openModal();
    }
}

// Inicializar quando a seção for mostrada
document.addEventListener('DOMContentLoaded', function() {
    let gestaoGastosInstance = null;
    
    // Verificar se já existe a função showSection, senão criar
    const originalShowSection = window.showSection;
    window.showSection = function(sectionId) {
        if (originalShowSection) {
            originalShowSection(sectionId);
        }
        
        if (sectionId === 'gestao_gastos') {
            if (!gestaoGastosInstance) {
                gestaoGastosInstance = new GestaoGastos();
                window.gestaoGastosInstance = gestaoGastosInstance; // Tornar global
            }
        }
    };
    
    // Se a seção já estiver visível no carregamento
    if (document.getElementById('gestao_gastos')?.style.display !== 'none') {
        gestaoGastosInstance = new GestaoGastos();
        window.gestaoGastosInstance = gestaoGastosInstance;
    }
});