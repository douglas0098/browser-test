// Dashboard Financeiro - JavaScript
class FinancialDashboard {
    constructor() {
        this.gastos = JSON.parse(localStorage.getItem('gastos')) || [];
        this.pagamentos = this.getPagamentosData();
        this.charts = {};
        this.currentPeriod = 30;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateSummary();
        this.initializeCharts();
        this.updateRecentTransactions();
        this.updateGoals();
        this.updateTopPerformers();
    }

    bindEvents() {
        // Seletores de período
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentPeriod = parseInt(e.target.dataset.period);
                this.updateAllCharts();
                this.updateSummary();
            });
        });

        // Botão de exportar
        const exportBtn = document.querySelector('.export-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportReport());
        }

        // Botão de atualizar
        const refreshBtn = document.querySelector('.refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshData());
        }
    }

    getPagamentosData() {
        // Simular dados de pagamentos - em produção, viria de localStorage ou API
        const pagamentos = [];
        const hoje = new Date();
        
        for (let i = 0; i < 60; i++) {
            const data = new Date(hoje);
            data.setDate(data.getDate() - i);
            
            // Simular alguns pagamentos por dia
            const numPagamentos = Math.floor(Math.random() * 5) + 1;
            
            for (let j = 0; j < numPagamentos; j++) {
                const metodos = ['pix', 'boleto', 'credit', 'debit'];
                const metodo = metodos[Math.floor(Math.random() * metodos.length)];
                
                pagamentos.push({
                    id: `pay_${i}_${j}`,
                    data: data.toISOString().split('T')[0],
                    valor: 99.90,
                    metodo: metodo,
                    status: 'confirmed',
                    usuario: `Usuario ${j + 1}`
                });
            }
        }
        
        return pagamentos;
    }

    updateSummary() {
        const periodo = this.getDateRange(this.currentPeriod);
        
        // Calcular receitas
        const receitasPeriodo = this.pagamentos.filter(p => 
            p.data >= periodo.inicio && p.data <= periodo.fim && p.status === 'confirmed'
        );
        const totalReceitas = receitasPeriodo.reduce((sum, p) => sum + p.valor, 0);
        
        // Calcular gastos
        const gastosPeriodo = this.gastos.filter(g => 
            g.data >= periodo.inicio && g.data <= periodo.fim
        );
        const totalGastos = gastosPeriodo.reduce((sum, g) => sum + g.valor, 0);
        
        // Calcular lucro e margem
        const lucroLiquido = totalReceitas - totalGastos;
        const margemLucro = totalReceitas > 0 ? ((lucroLiquido / totalReceitas) * 100) : 0;
        
        // Atualizar elementos
        document.getElementById('total-revenue').textContent = `R$ ${totalReceitas.toFixed(2).replace('.', ',')}`;
        document.getElementById('total-expenses').textContent = `R$ ${totalGastos.toFixed(2).replace('.', ',')}`;
        document.getElementById('net-profit').textContent = `R$ ${lucroLiquido.toFixed(2).replace('.', ',')}`;
        document.getElementById('profit-margin').textContent = `${margemLucro.toFixed(1)}%`;
        
        // Atualizar tendências (simulado)
        this.updateTrends();
    }

    updateTrends() {
        // Simular cálculos de tendência
        const trends = {
            revenue: { value: 12, positive: true },
            expenses: { value: 8, positive: false },
            profit: { value: 25, positive: true },
            margin: { value: 3, positive: true }
        };

        Object.entries(trends).forEach(([key, trend]) => {
            const element = document.getElementById(`${key}-trend`);
            if (element) {
                const arrow = element.querySelector('.trend-arrow');
                const value = element.querySelector('.trend-value');
                
                arrow.textContent = trend.positive ? '↗' : '↘';
                value.textContent = `${trend.positive ? '+' : ''}${trend.value}%`;
                
                element.className = `summary-trend ${trend.positive ? 'positive' : 'negative'}`;
            }
        });
    }

    initializeCharts() {
        // Verificar se Chart.js está disponível
        if (typeof Chart === 'undefined') {
            this.loadChartJS().then(() => {
                this.createCharts();
            });
        } else {
            this.createCharts();
        }
    }

    loadChartJS() {
        return new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            script.onload = resolve;
            document.head.appendChild(script);
        });
    }

    createCharts() {
        this.createTrendChart();
        this.createExpensePieChart();
        this.createPaymentMethodChart();
        this.createCashFlowChart();
    }

    createTrendChart() {
        const ctx = document.getElementById('trendChart');
        if (!ctx) return;

        const periodo = this.getDateRange(this.currentPeriod);
        const labels = this.getDateLabels(periodo);
        const receitasData = this.getReceitasPorDia(labels);
        const gastosData = this.getGastosPorDia(labels);

        this.charts.trend = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ganhos',
                    data: receitasData,
                    borderColor: 'rgb(39, 174, 96)',
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Gastos',
                    data: gastosData,
                    borderColor: 'rgb(231, 76, 60)',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toFixed(0);
                            }
                        }
                    }
                }
            }
        });
    }

    createExpensePieChart() {
        const ctx = document.getElementById('expensePieChart');
        if (!ctx) return;

        const categorias = this.getGastosPorCategoria();
        const labels = Object.keys(categorias);
        const data = Object.values(categorias);
        const colors = [
            '#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6'
        ];

        this.charts.expensePie = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels.map(l => this.getCategoryName(l)),
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createPaymentMethodChart() {
        const ctx = document.getElementById('paymentMethodChart');
        if (!ctx) return;

        const metodos = this.getPagamentosPorMetodo();
        const labels = Object.keys(metodos);
        const data = Object.values(metodos);

        this.charts.paymentMethod = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels.map(m => this.getMethodName(m)),
                datasets: [{
                    label: 'Valor (R$)',
                    data: data,
                    backgroundColor: [
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(243, 156, 18, 0.8)',
                        'rgba(39, 174, 96, 0.8)'
                    ],
                    borderColor: [
                        'rgba(52, 152, 219, 1)',
                        'rgba(231, 76, 60, 1)',
                        'rgba(243, 156, 18, 1)',
                        'rgba(39, 174, 96, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toFixed(0);
                            }
                        }
                    }
                }
            }
        });
    }

    createCashFlowChart() {
        const ctx = document.getElementById('cashFlowChart');
        if (!ctx) return;

        const periodo = this.getDateRange(this.currentPeriod);
        const labels = this.getDateLabels(periodo);
        const fluxoCaixa = this.getFluxoCaixaAcumulado(labels);

        this.charts.cashFlow = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Fluxo de Caixa',
                    data: fluxoCaixa,
                    borderColor: 'rgb(52, 152, 219)',
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toFixed(0);
                            }
                        }
                    }
                }
            }
        });
    }

    // Métodos auxiliares
    getDateRange(days) {
        const fim = new Date().toISOString().split('T')[0];
        const inicio = new Date();
        inicio.setDate(inicio.getDate() - days);
        return {
            inicio: inicio.toISOString().split('T')[0],
            fim: fim
        };
    }

    getDateLabels(periodo) {
        const labels = [];
        const inicio = new Date(periodo.inicio);
        const fim = new Date(periodo.fim);
        
        while (inicio <= fim) {
            labels.push(inicio.toISOString().split('T')[0]);
            inicio.setDate(inicio.getDate() + 1);
        }
        
        return labels;
    }

    getReceitasPorDia(labels) {
        return labels.map(data => {
            const receitasNaData = this.pagamentos.filter(p => 
                p.data === data && p.status === 'confirmed'
            );
            return receitasNaData.reduce((sum, p) => sum + p.valor, 0);
        });
    }

    getGastosPorDia(labels) {
        return labels.map(data => {
            const gastosNaData = this.gastos.filter(g => g.data === data);
            return gastosNaData.reduce((sum, g) => sum + g.valor, 0);
        });
    }

    getGastosPorCategoria() {
        const categorias = {};
        this.gastos.forEach(gasto => {
            if (!categorias[gasto.categoria]) {
                categorias[gasto.categoria] = 0;
            }
            categorias[gasto.categoria] += gasto.valor;
        });
        return categorias;
    }

    getPagamentosPorMetodo() {
        const metodos = {};
        this.pagamentos
            .filter(p => p.status === 'confirmed')
            .forEach(pagamento => {
                if (!metodos[pagamento.metodo]) {
                    metodos[pagamento.metodo] = 0;
                }
                metodos[pagamento.metodo] += pagamento.valor;
            });
        return metodos;
    }

    getFluxoCaixaAcumulado(labels) {
        let acumulado = 0;
        return labels.map(data => {
            const receitas = this.pagamentos
                .filter(p => p.data === data && p.status === 'confirmed')
                .reduce((sum, p) => sum + p.valor, 0);
            
            const gastos = this.gastos
                .filter(g => g.data === data)
                .reduce((sum, g) => sum + g.valor, 0);
            
            acumulado += (receitas - gastos);
            return acumulado;
        });
    }

    getCategoryName(categoria) {
        const names = {
            infraestrutura: 'Infraestrutura',
            apis: 'APIs',
            licencas: 'Licenças',
            marketing: 'Marketing',
            outros: 'Outros'
        };
        return names[categoria] || categoria;
    }

    getMethodName(metodo) {
        const names = {
            pix: 'PIX',
            boleto: 'Boleto',
            credit: 'Cartão de Crédito',
            debit: 'Cartão de Débito'
        };
        return names[metodo] || metodo;
    }

    updateAllCharts() {
        if (this.charts.trend) {
            const periodo = this.getDateRange(this.currentPeriod);
            const labels = this.getDateLabels(periodo);
            
            this.charts.trend.data.labels = labels;
            this.charts.trend.data.datasets[0].data = this.getReceitasPorDia(labels);
            this.charts.trend.data.datasets[1].data = this.getGastosPorDia(labels);
            this.charts.trend.update();
        }

        if (this.charts.cashFlow) {
            const periodo = this.getDateRange(this.currentPeriod);
            const labels = this.getDateLabels(periodo);
            
            this.charts.cashFlow.data.labels = labels;
            this.charts.cashFlow.data.datasets[0].data = this.getFluxoCaixaAcumulado(labels);
            this.charts.cashFlow.update();
        }
    }

    updateRecentTransactions() {
        // Atualizar transações recentes na interface
        // Esta parte seria integrada com os dados reais
    }

    updateGoals() {
        // Atualizar metas baseadas nos dados reais
        const metaReceita = 25000;
        const receitaAtual = 18500;
        const percentReceita = (receitaAtual / metaReceita) * 100;
        
        // Atualizar barras de progresso dinamicamente
        const progressBars = document.querySelectorAll('.progress-fill');
        if (progressBars.length > 0) {
            progressBars[0].style.width = `${Math.min(percentReceita, 100)}%`;
        }
    }

    updateTopPerformers() {
        const categorias = this.getGastosPorCategoria();
        const sorted = Object.entries(categorias)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 4);
        
        const maxValue = sorted[0]?.[1] || 1;
        
        document.querySelectorAll('.performer-item').forEach((item, index) => {
            if (sorted[index]) {
                const [categoria, valor] = sorted[index];
                const percentage = (valor / maxValue) * 100;
                
                item.querySelector('.performer-name').textContent = this.getCategoryName(categoria);
                item.querySelector('.performer-value').textContent = `R$ ${valor.toFixed(0)}`;
                item.querySelector('.bar-fill').style.width = `${percentage}%`;
            }
        });
    }

    refreshData() {
        // Recarregar dados
        this.gastos = JSON.parse(localStorage.getItem('gastos')) || [];
        this.pagamentos = this.getPagamentosData();
        
        // Atualizar interface
        this.updateSummary();
        this.updateAllCharts();
        this.updateGoals();
        this.updateTopPerformers();
        
        // Feedback visual
        this.showNotification('Dados atualizados com sucesso!', 'success');
    }

    exportReport() {
        const periodo = this.getDateRange(this.currentPeriod);
        const dados = {
            periodo: periodo,
            receitas: this.pagamentos.filter(p => 
                p.data >= periodo.inicio && p.data <= periodo.fim
            ),
            gastos: this.gastos.filter(g => 
                g.data >= periodo.inicio && g.data <= periodo.fim
            ),
            exportDate: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(dados, null, 2)], { 
            type: 'application/json' 
        });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `relatorio_financeiro_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('Relatório exportado com sucesso!', 'success');
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
            zIndex: '9999',
            transform: 'translateX(400px)',
            transition: 'all 0.3s ease'
        });

        if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #27ae60 0%, #229954 100%)';
        }

        document.body.appendChild(notification);
        setTimeout(() => notification.style.transform = 'translateX(0)', 100);
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Inicializar Dashboard
document.addEventListener('DOMContentLoaded', function() {
    let dashboardInstance = null;
    
    const originalShowSection = window.showSection;
    window.showSection = function(sectionId) {
        if (originalShowSection) {
            originalShowSection(sectionId);
        }
        
        if (sectionId === 'dashboard') {
            if (!dashboardInstance) {
                dashboardInstance = new FinancialDashboard();
            } else {
                dashboardInstance.refreshData();
            }
        }
    };
    
    if (document.getElementById('dashboard')?.style.display !== 'none') {
        dashboardInstance = new FinancialDashboard();
    }
});