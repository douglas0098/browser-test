from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QStackedWidget,
                             QFrame, QScrollArea, QFormLayout, QLineEdit,
                             QComboBox, QCheckBox, QTextEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QProgressBar,
                             QSpinBox, QDateEdit, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QPalette, QColor
import json
import os

class SettingsWidget(QWidget):
    """Widget de configurações com aparência similar ao HTML fornecido"""
    
    # Sinais
    settings_changed = pyqtSignal(dict)
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_section = "perfil"
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Cria a interface principal com sidebar + conteúdo"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Área de conteúdo
        self.content_area = self.create_content_area()
        main_layout.addWidget(self.content_area, 1)
        
        self.setLayout(main_layout)
    
    def create_sidebar(self):
        """Cria a sidebar com menu de navegação"""
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header da sidebar
        header = QLabel("Configurações")
        header.setObjectName("sidebar-header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Menu items
        self.menu_buttons = {}
        menu_items = [
            ("perfil", "Perfil"),
            ("downloads", "Downloads"),
            ("nova_ia", "Nova IA"),
            ("usuario", "Usuário"),
            ("pagamentos", "Pagamentos"),
            ("gestao_pg", "Gestão de Pagamentos"),
            ("gestao_gastos", "Gestão de Gastos"),
            ("dashboard", "Dashboard"),
            ("cache", "Cache"),
            ("proxy", "Proxy"),
            ("antidetecao", "Anti-detecção")
        ]
        
        for section_id, section_name in menu_items:
            btn = QPushButton(section_name)
            btn.setObjectName("menu-button")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, sid=section_id: self.show_section(sid))
            layout.addWidget(btn)
            self.menu_buttons[section_id] = btn
        
        # Ativar primeira seção
        self.menu_buttons["perfil"].setChecked(True)
        
        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar
    
    def create_content_area(self):
        """Cria a área de conteúdo com todas as seções"""
        self.stacked_widget = QStackedWidget()
        
        # Criar todas as seções
        sections = {
            "perfil": self.create_perfil_section(),
            "downloads": self.create_downloads_section(),
            "nova_ia": self.create_nova_ia_section(),
            "usuario": self.create_usuario_section(),
            "pagamentos": self.create_pagamentos_section(),
            "gestao_pg": self.create_gestao_pg_section(),
            "gestao_gastos": self.create_gestao_gastos_section(),
            "dashboard": self.create_dashboard_section(),
            "cache": self.create_cache_section(),
            "proxy": self.create_proxy_section(),
            "antidetecao": self.create_antidetecao_section()
        }
        
        for section_id, widget in sections.items():
            self.stacked_widget.addWidget(widget)
            setattr(self, f"section_{section_id}", widget)
        
        return self.stacked_widget
    
    def show_section(self, section_id):
        """Mostra a seção selecionada"""
        # Atualizar botões
        for btn_id, btn in self.menu_buttons.items():
            btn.setChecked(btn_id == section_id)
        
        # Mostrar seção
        section_widget = getattr(self, f"section_{section_id}")
        self.stacked_widget.setCurrentWidget(section_widget)
        self.current_section = section_id
    
    def create_perfil_section(self):
        """Cria seção de perfil"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Perfil")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        # Área de perfil
        profile_frame = QFrame()
        profile_frame.setObjectName("profile-frame")
        profile_layout = QHBoxLayout()
        
        # Avatar placeholder
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(120, 120)
        avatar_frame.setObjectName("avatar-placeholder")
        avatar_layout = QVBoxLayout()
        
        avatar_initials = QLabel("JS")
        avatar_initials.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_initials.setObjectName("avatar-initials")
        avatar_layout.addWidget(avatar_initials)
        
        change_avatar_btn = QPushButton("Alterar Foto")
        change_avatar_btn.setObjectName("change-avatar-btn")
        avatar_layout.addWidget(change_avatar_btn)
        
        avatar_frame.setLayout(avatar_layout)
        profile_layout.addWidget(avatar_frame)
        
        # Dados do perfil
        form_layout = QFormLayout()
        
        self.profile_name = QLineEdit("João Silva")
        form_layout.addRow("Nome:", self.profile_name)
        
        self.profile_email = QLineEdit("joao.silva@email.com")
        form_layout.addRow("Email:", self.profile_email)
        
        self.profile_type = QLineEdit("Administrador")
        self.profile_type.setReadOnly(True)
        form_layout.addRow("Tipo de Conta:", self.profile_type)
        
        self.profile_created = QLineEdit("15/01/2023")
        self.profile_created.setReadOnly(True)
        form_layout.addRow("Conta criada em:", self.profile_created)
        
        password_layout = QHBoxLayout()
        self.profile_password = QLineEdit("********")
        self.profile_password.setEchoMode(QLineEdit.EchoMode.Password)
        change_password_btn = QPushButton("Alterar Senha")
        password_layout.addWidget(self.profile_password)
        password_layout.addWidget(change_password_btn)
        form_layout.addRow("Senha:", password_layout)
        
        profile_layout.addLayout(form_layout)
        profile_frame.setLayout(profile_layout)
        layout.addWidget(profile_frame)
        
        # Botão salvar
        save_btn = QPushButton("Salvar Alterações")
        save_btn.setObjectName("save-button")
        layout.addWidget(save_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_downloads_section(self):
        """Cria seção de downloads"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Downloads")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Gerencie seus downloads e acesse os arquivos baixados.")
        layout.addWidget(description)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Pesquisar downloads...")
        filter_layout.addWidget(search_input)
        
        filter_type = QComboBox()
        filter_type.addItems(["Todos os tipos", "Documentos", "Imagens", "Vídeos", "Áudios"])
        filter_layout.addWidget(filter_type)
        
        filter_date = QComboBox()
        filter_date.addItems(["Qualquer data", "Hoje", "Ontem", "Última semana"])
        filter_layout.addWidget(filter_date)
        
        layout.addLayout(filter_layout)
        
        # Tabela de downloads
        downloads_table = QTableWidget(5, 7)
        downloads_table.setHorizontalHeaderLabels([
            "Nome", "Tipo", "Tamanho", "Data", "Origem", "Pasta", "Status"
        ])
        
        # Dados de exemplo
        sample_data = [
            ["relatorio_financeiro.pdf", "PDF", "2.5 MB", "22/04/2025 14:30", "www.empresa.com.br", "Downloads", "Completo"],
            ["logo_empresa.png", "Imagem", "758 KB", "20/04/2025 10:15", "www.recursos.com", "Pictures", "Completo"],
            ["tutorial_python.mp4", "Vídeo", "245 MB", "18/04/2025 16:45", "www.cursos-online.com", "Videos", "Completo"]
        ]
        
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                downloads_table.setItem(row, col, QTableWidgetItem(value))
        
        downloads_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(downloads_table)
        
        # Configurações
        config_group = QGroupBox("Configurações de Download")
        config_layout = QFormLayout()
        
        location_input = QLineEdit("C:\\Users\\Usuario\\Downloads")
        config_layout.addRow("Local padrão:", location_input)
        
        ask_location_check = QCheckBox("Perguntar onde salvar antes de baixar")
        ask_location_check.setChecked(True)
        config_layout.addRow(ask_location_check)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_nova_ia_section(self):
        """Cria seção de nova IA"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Adicionar nova IA")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Preencha o formulário abaixo para adicionar um novo perfil de IA ao sistema.")
        layout.addWidget(description)
        
        # Formulário
        form_layout = QFormLayout()
        
        ia_nome = QLineEdit()
        ia_nome.setPlaceholderText("Digite o nome da IA")
        form_layout.addRow("Nome da IA:", ia_nome)
        
        ia_link = QLineEdit()
        ia_link.setPlaceholderText("https://exemplo.com/ia")
        form_layout.addRow("Link da IA:", ia_link)
        
        ia_user = QLineEdit()
        ia_user.setPlaceholderText("Usuário da IA...")
        form_layout.addRow("Usuário da IA:", ia_user)
        
        ia_password = QLineEdit()
        ia_password.setPlaceholderText("Senha...")
        ia_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Senha da IA:", ia_password)
        
        # Categorias
        categories_layout = QVBoxLayout()
        categoria_input = QLineEdit()
        categoria_input.setPlaceholderText("Categoria 1")
        categories_layout.addWidget(categoria_input)
        
        add_categoria_btn = QPushButton("Adicionar Categoria")
        categories_layout.addWidget(add_categoria_btn)
        
        form_layout.addRow("Categorias:", categories_layout)
        
        ia_observacoes = QTextEdit()
        ia_observacoes.setPlaceholderText("Informações adicionais sobre a IA (opcional)")
        ia_observacoes.setMaximumHeight(100)
        form_layout.addRow("Observações:", ia_observacoes)
        
        proxy_select = QComboBox()
        proxy_select.addItems([
            "185.14.238.40:29891:jnVKAN6F:m726EadY",
            "185.14.238.40:29892:tlXIAaAR:NtZ9zSM"
        ])
        form_layout.addRow("Configuração de Proxy:", proxy_select)
        
        layout.addLayout(form_layout)
        
        # Botões
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar IA")
        save_btn.setObjectName("save-button")
        clear_btn = QPushButton("Limpar Dados")
        clear_btn.setObjectName("cancel-button")
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        layout.addLayout(button_layout)
        
        # Lista de IAs cadastradas
        preview_group = QGroupBox("Lista de IAs Cadastradas")
        preview_layout = QVBoxLayout()
        
        search_ia = QLineEdit()
        search_ia.setPlaceholderText("Buscar IA...")
        preview_layout.addWidget(search_ia)
        
        ia_table = QTableWidget(3, 4)
        ia_table.setHorizontalHeaderLabels(["Nome", "Categorias", "Link", "Ações"])
        
        # Dados de exemplo
        ia_data = [
            ["ChatGPT", "Conversação, Texto, Educação", "https://chat.openai.com"],
            ["DALL-E", "Imagem, Criação, Arte", "https://openai.com/dall-e"],
            ["Claude", "Conversação, Texto, Assistente", "https://claude.ai"]
        ]
        
        for row, data in enumerate(ia_data):
            for col, value in enumerate(data):
                ia_table.setItem(row, col, QTableWidgetItem(value))
            
            # Botões de ação
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            edit_btn = QPushButton("Editar")
            delete_btn = QPushButton("Excluir")
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_widget.setLayout(action_layout)
            ia_table.setCellWidget(row, 3, action_widget)
        
        preview_layout.addWidget(ia_table)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_usuario_section(self):
        """Cria seção de usuário"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Gerenciamento de Usuários")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        # Busca
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Pesquisar usuários...")
        search_btn = QPushButton("Buscar")
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)
        
        # Tabela de usuários
        user_table = QTableWidget(4, 5)
        user_table.setHorizontalHeaderLabels(["Nome", "Email", "Grupo", "Status", "Ações"])
        
        # Dados de exemplo
        user_data = [
            ["João Silva", "joao.silva@email.com", "Administrador", "Ativo"],
            ["Maria Souza", "maria.souza@email.com", "Equipe de trabalho", "Ativo"],
            ["Carlos Ferreira", "carlos.ferreira@email.com", "Membro", "Inativo"],
            ["Ana Oliveira", "ana.oliveira@email.com", "Convidado", "Ativo"]
        ]
        
        for row, data in enumerate(user_data):
            for col, value in enumerate(data):
                if col == 2:  # Coluna de grupo
                    combo = QComboBox()
                    combo.addItems(["Administrador", "Equipe de trabalho", "Membro", "Convidado", "Avulso"])
                    combo.setCurrentText(value)
                    user_table.setCellWidget(row, col, combo)
                else:
                    user_table.setItem(row, col, QTableWidgetItem(value))
            
            # Botões de ação
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            edit_btn = QPushButton("Editar")
            delete_btn = QPushButton("Excluir")
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_widget.setLayout(action_layout)
            user_table.setCellWidget(row, 4, action_widget)
        
        layout.addWidget(user_table)
        
        # Botões de ação
        action_layout = QHBoxLayout()
        add_user_btn = QPushButton("Adicionar Usuário")
        save_users_btn = QPushButton("Salvar Alterações")
        action_layout.addWidget(add_user_btn)
        action_layout.addWidget(save_users_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_pagamentos_section(self):
        """Cria seção de pagamentos"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Pagamentos")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        # Opções de pagamento
        payment_group = QGroupBox("Escolha a forma de pagamento:")
        payment_layout = QVBoxLayout()
        
        # Tabs de pagamento
        tab_layout = QHBoxLayout()
        pix_btn = QPushButton("PIX")
        pix_btn.setCheckable(True)
        pix_btn.setChecked(True)
        boleto_btn = QPushButton("Boleto")
        boleto_btn.setCheckable(True)
        cartao_btn = QPushButton("Cartão")
        cartao_btn.setCheckable(True)
        
        tab_layout.addWidget(pix_btn)
        tab_layout.addWidget(boleto_btn)
        tab_layout.addWidget(cartao_btn)
        tab_layout.addStretch()
        payment_layout.addLayout(tab_layout)
        
        # Conteúdo PIX
        pix_frame = QFrame()
        pix_layout = QHBoxLayout()
        
        # QR Code placeholder
        qr_frame = QFrame()
        qr_frame.setFixedSize(200, 200)
        qr_frame.setObjectName("qrcode-placeholder")
        qr_label = QLabel("QR CODE")
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_layout_inner = QVBoxLayout()
        qr_layout_inner.addWidget(qr_label)
        qr_frame.setLayout(qr_layout_inner)
        pix_layout.addWidget(qr_frame)
        
        # Informações PIX
        pix_info_layout = QFormLayout()
        
        pix_key = QLineEdit("browser123@dominio.com")
        pix_key.setReadOnly(True)
        pix_info_layout.addRow("Chave PIX:", pix_key)
        
        pix_name = QLineEdit("Browser Software LTDA")
        pix_name.setReadOnly(True)
        pix_info_layout.addRow("Nome:", pix_name)
        
        pix_value = QLineEdit("R$ 99,90")
        pix_value.setReadOnly(True)
        pix_info_layout.addRow("Valor:", pix_value)
        
        pix_layout.addLayout(pix_info_layout)
        pix_frame.setLayout(pix_layout)
        payment_layout.addWidget(pix_frame)
        
        payment_group.setLayout(payment_layout)
        layout.addWidget(payment_group)
        
        # Histórico de pagamentos
        history_group = QGroupBox("Histórico de Pagamentos")
        history_layout = QVBoxLayout()
        
        payment_table = QTableWidget(3, 5)
        payment_table.setHorizontalHeaderLabels(["Data", "Descrição", "Valor", "Método", "Status"])
        
        payment_data = [
            ["05/03/2025", "Assinatura Premium", "R$ 99,90", "PIX", "Confirmado"],
            ["05/02/2025", "Assinatura Premium", "R$ 99,90", "Boleto", "Confirmado"],
            ["05/01/2025", "Assinatura Premium", "R$ 99,90", "PIX", "Confirmado"]
        ]
        
        for row, data in enumerate(payment_data):
            for col, value in enumerate(data):
                payment_table.setItem(row, col, QTableWidgetItem(value))
        
        history_layout.addWidget(payment_table)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_gestao_pg_section(self):
        """Cria seção de gestão de pagamentos"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Gestão de Pagamentos")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Gerencie todos os pagamentos dos usuários do sistema.")
        layout.addWidget(description)
        
        # Estatísticas
        stats_layout = QHBoxLayout()
        
        stats_data = [
            ("Pagamentos Hoje", "R$ 1.247,30", "12 pagamentos"),
            ("Pendentes", "R$ 599,70", "6 pagamentos"),
            ("Este Mês", "R$ 15.890,40", "158 pagamentos"),
            ("Taxa de Sucesso", "94.2%", "dos pagamentos")
        ]
        
        for title_text, number, subtitle in stats_data:
            stat_card = QFrame()
            stat_card.setObjectName("stat-card")
            stat_layout = QVBoxLayout()
            
            stat_title = QLabel(title_text)
            stat_title.setObjectName("stat-title")
            stat_layout.addWidget(stat_title)
            
            stat_number = QLabel(number)
            stat_number.setObjectName("stat-number")
            stat_layout.addWidget(stat_number)
            
            stat_subtitle = QLabel(subtitle)
            stat_subtitle.setObjectName("stat-subtitle")
            stat_layout.addWidget(stat_subtitle)
            
            stat_card.setLayout(stat_layout)
            stats_layout.addWidget(stat_card)
        
        layout.addLayout(stats_layout)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        search_payments = QLineEdit()
        search_payments.setPlaceholderText("Buscar por usuário, email ou ID...")
        filter_layout.addWidget(search_payments)
        
        status_filter = QComboBox()
        status_filter.addItems(["Todos os Status", "Confirmado", "Pendente", "Falhou"])
        filter_layout.addWidget(status_filter)
        
        method_filter = QComboBox()
        method_filter.addItems(["Todos os Métodos", "PIX", "Boleto", "Cartão"])
        filter_layout.addWidget(method_filter)
        
        layout.addLayout(filter_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_gestao_gastos_section(self):
        """Cria seção de gestão de gastos"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Gestão de Gastos")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Controle e analise todos os gastos do sistema.")
        layout.addWidget(description)
        
        # Dashboard de estatísticas
        stats_layout = QHBoxLayout()
        
        stats_data = [
            ("Gastos Hoje", "R$ 847,30", "↗ +12%"),
            ("Gastos Este Mês", "R$ 12.890,40", "↘ -5%"),
            ("Orçamento Restante", "R$ 7.109,60", "64% usado"),
            ("Maior Gasto", "R$ 2.450,00", "Infraestrutura")
        ]
        
        for title_text, value, trend in stats_data:
            stat_card = QFrame()
            stat_card.setObjectName("expense-stat-card")
            stat_layout = QVBoxLayout()
            
            stat_title = QLabel(title_text)
            stat_layout.addWidget(stat_title)
            
            stat_value = QLabel(value)
            stat_layout.addWidget(stat_value)
            
            stat_trend = QLabel(trend)
            stat_layout.addWidget(stat_trend)
            
            stat_card.setLayout(stat_layout)
            stats_layout.addWidget(stat_card)
        
        layout.addLayout(stats_layout)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        search_expenses = QLineEdit()
        search_expenses.setPlaceholderText("Buscar gastos...")
        filter_layout.addWidget(search_expenses)
        
        category_filter = QComboBox()
        category_filter.addItems(["Todas as Categorias", "Infraestrutura", "Licenças", "APIs"])
        filter_layout.addWidget(category_filter)
        
        add_expense_btn = QPushButton("+ Adicionar Gasto")
        filter_layout.addWidget(add_expense_btn)
        
        layout.addLayout(filter_layout)
        
        # Tabela de gastos
        expenses_table = QTableWidget(3, 7)
        expenses_table.setHorizontalHeaderLabels([
            "Data", "Descrição", "Categoria", "Valor", "Responsável", "Status", "Ações"
        ])
        
        expense_data = [
            ["12/06/2025", "Servidor AWS - Instância t3.large", "Infraestrutura", "R$ 450,00", "João Silva", "Aprovado"],
            ["11/06/2025", "OpenAI API Credits", "APIs", "R$ 890,50", "Maria Souza", "Pendente"],
            ["10/06/2025", "Licença Adobe Creative Suite", "Licenças", "R$ 280,00", "Carlos Ferreira", "Aprovado"]
        ]
        
        for row, data in enumerate(expense_data):
            for col, value in enumerate(data):
                expenses_table.setItem(row, col, QTableWidgetItem(value))
        
        layout.addWidget(expenses_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_dashboard_section(self):
        """Cria seção de dashboard"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Dashboard Financeiro")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Visão completa dos ganhos e gastos com análises visuais.")
        layout.addWidget(description)
        
        # Cards de resumo
        summary_layout = QHBoxLayout()
        
        summary_data = [
            ("RECEITA TOTAL", "R$ 0,00", "+12%"),
            ("GASTOS TOTAL", "R$ 0,00", "-8%"),
            ("LUCRO LÍQUIDO", "R$ 0,00", "+25%"),
            ("MARGEM DE LUCRO", "0%", "+3%")
        ]
        
        for title_text, value, trend in summary_data:
            summary_card = QFrame()
            summary_card.setObjectName("summary-card")
            summary_card_layout = QVBoxLayout()
            
            card_title = QLabel(title_text)
            card_title.setObjectName("summary-title")
            summary_card_layout.addWidget(card_title)
            
            card_value = QLabel(value)
            card_value.setObjectName("summary-value")
            summary_card_layout.addWidget(card_value)
            
            card_trend = QLabel(trend)
            card_trend.setObjectName("summary-trend")
            summary_card_layout.addWidget(card_trend)
            
            summary_card.setLayout(summary_card_layout)
            summary_layout.addWidget(summary_card)
        
        layout.addLayout(summary_layout)
        
        # Controles do dashboard
        controls_layout = QHBoxLayout()
        
        period_buttons = QHBoxLayout()
        for period in ["7 dias", "30 dias", "3 meses", "1 ano"]:
            btn = QPushButton(period)
            btn.setCheckable(True)
            if period == "30 dias":
                btn.setChecked(True)
            period_buttons.addWidget(btn)
        
        controls_layout.addLayout(period_buttons)
        controls_layout.addStretch()
        
        export_btn = QPushButton("📊 Exportar Relatório")
        refresh_btn = QPushButton("🔄 Atualizar")
        controls_layout.addWidget(export_btn)
        controls_layout.addWidget(refresh_btn)
        
        layout.addLayout(controls_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_cache_section(self):
        """Cria seção de cache"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Cache")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Gerencie o cache e cookies do navegador.")
        layout.addWidget(description)
        
        # Configurações de cache
        cache_group = QGroupBox("Configurações de Cache")
        cache_layout = QFormLayout()
        
        auto_clear = QCheckBox("Limpeza automática")
        auto_clear.setChecked(True)
        cache_layout.addRow(auto_clear)
        
        clear_interval = QComboBox()
        clear_interval.addItems(["1 dia", "3 dias", "7 dias", "14 dias", "30 dias"])
        clear_interval.setCurrentText("7 dias")
        cache_layout.addRow("Intervalo de limpeza:", clear_interval)
        
        last_clear = QLabel("Nunca")
        cache_layout.addRow("Última limpeza:", last_clear)
        
        next_clear = QLabel("Em 7 dias")
        cache_layout.addRow("Próxima limpeza:", next_clear)
        
        cache_group.setLayout(cache_layout)
        layout.addWidget(cache_group)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        
        clear_cache_btn = QPushButton("Limpar Cache")
        clear_cookies_btn = QPushButton("Limpar Cookies")
        clear_all_btn = QPushButton("Limpar Tudo")
        
        button_layout.addWidget(clear_cache_btn)
        button_layout.addWidget(clear_cookies_btn)
        button_layout.addWidget(clear_all_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_proxy_section(self):
        """Cria seção de proxy"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Adicionar novo Proxy")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Preencha o formulário abaixo para adicionar um novo proxy.")
        layout.addWidget(description)
        
        # Formulário de proxy
        form_layout = QFormLayout()
        
        proxy_input = QLineEdit()
        proxy_input.setPlaceholderText("Digite ou cole o proxy aqui...")
        form_layout.addRow("Proxy:", proxy_input)
        
        layout.addLayout(form_layout)
        
        save_proxy_btn = QPushButton("Salvar Proxy")
        save_proxy_btn.setObjectName("save-button")
        layout.addWidget(save_proxy_btn)
        
        # Seção de acesso via proxy
        access_group = QGroupBox("Acessar site via Proxy")
        access_layout = QFormLayout()
        
        site_url = QLineEdit()
        site_url.setPlaceholderText("https://exemplo.com")
        access_layout.addRow("URL do site:", site_url)
        
        proxy_select = QComboBox()
        proxy_select.addItems(["-- Selecione um Proxy --", "Proxy 1", "Proxy 2", "Proxy 3"])
        access_layout.addRow("Selecione o Proxy:", proxy_select)
        
        access_mode = QComboBox()
        access_mode.addItems(["Anônimo (sem cookies)", "Mascarado (com cookies alternativos)", "Rotação de IP"])
        access_layout.addRow("Modo de Acesso:", access_mode)
        
        prevent_fingerprinting = QCheckBox("Prevenir fingerprinting do navegador")
        prevent_fingerprinting.setChecked(True)
        access_layout.addRow(prevent_fingerprinting)
        
        prevent_double_login = QCheckBox("Evitar detecção de login duplo")
        prevent_double_login.setChecked(True)
        access_layout.addRow(prevent_double_login)
        
        access_group.setLayout(access_layout)
        layout.addWidget(access_group)
        
        access_btn = QPushButton("Acessar via Proxy")
        layout.addWidget(access_btn)
        
        # Lista de proxies
        proxy_list_group = QGroupBox("Lista de Proxies cadastrados")
        proxy_list_layout = QVBoxLayout()
        
        search_proxy = QLineEdit()
        search_proxy.setPlaceholderText("Buscar Proxy...")
        proxy_list_layout.addWidget(search_proxy)
        
        proxy_table = QTableWidget(5, 4)
        proxy_table.setHorizontalHeaderLabels(["Proxy", "IA Utilizando", "Status", "Ações"])
        
        proxy_data = [
            ["Proxy 1", "ChatGPT", "Em uso"],
            ["Proxy 2", "DALL-E", "Em uso"],
            ["Proxy 3", "Claude", "Em uso"],
            ["Proxy 4", "-", "Vazio"],
            ["Proxy 5", "Gemini", "Em uso"]
        ]
        
        for row, data in enumerate(proxy_data):
            for col, value in enumerate(data):
                proxy_table.setItem(row, col, QTableWidgetItem(value))
        
        proxy_list_layout.addWidget(proxy_table)
        proxy_list_group.setLayout(proxy_list_layout)
        layout.addWidget(proxy_list_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_antidetecao_section(self):
        """Cria seção de anti-detecção"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Antidetecção")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        description = QLabel("Configure as opções de antidetecção.")
        layout.addWidget(description)
        
        # Configurações
        form_layout = QFormLayout()
        
        user_agent = QLineEdit()
        user_agent.setPlaceholderText("Digite um novo User-Agent")
        form_layout.addRow("User-Agent:", user_agent)
        
        resolution = QLineEdit()
        resolution.setPlaceholderText("1920x1080")
        form_layout.addRow("Resolução da Tela:", resolution)
        
        disable_js = QCheckBox("Desativar JavaScript")
        form_layout.addRow("Desativar JavaScript:", disable_js)
        
        disable_webrtc = QCheckBox("Desativar WebRTC")
        form_layout.addRow("Desativar WebRTC:", disable_webrtc)
        
        timezone = QLineEdit()
        timezone.setPlaceholderText("Ex: UTC-3")
        form_layout.addRow("Fuso Horário:", timezone)
        
        language = QLineEdit()
        language.setPlaceholderText("Ex: pt-BR")
        form_layout.addRow("Idioma do Navegador:", language)
        
        gpu = QCheckBox("Desativar Aceleração de GPU")
        form_layout.addRow("Desativar GPU:", gpu)
        
        do_not_track = QCheckBox("Ativar Do Not Track")
        form_layout.addRow("Do Not Track:", do_not_track)
        
        layout.addLayout(form_layout)
        
        apply_btn = QPushButton("Aplicar Configurações")
        apply_btn.setObjectName("save-button")
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def apply_styles(self):
        """Aplica os estilos CSS"""
        self.setStyleSheet("""
            /* Estilos gerais */
            QWidget {
                background-color: #f4f4f4;
                color: #333;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            
            /* Sidebar */
            QFrame#sidebar {
                background-color: #2c3e50;
                color: white;
                border-right: 1px solid #34495e;
            }
            
            QLabel#sidebar-header {
                background-color: #34495e;
                color: white;
                padding: 20px;
                font-size: 18px;
                font-weight: bold;
                border-bottom: 1px solid #2c3e50;
            }
            
            QPushButton#menu-button {
                background-color: #34495e;
                color: white;
                border: none;
                text-align: left;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 0px;
            }
            
            QPushButton#menu-button:hover {
                background-color: #2980b9;
            }
            
            QPushButton#menu-button:checked {
                background-color: #2980b9;
                border-left: 4px solid white;
            }
            
            /* Títulos de seção */
            QLabel#section-title {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
                margin-bottom: 20px;
            }
            
            /* Cards de estatísticas */
            QFrame#stat-card,
            QFrame#expense-stat-card,
            QFrame#summary-card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 20px;
                border-radius: 12px;
                margin: 5px;
            }
            
            QLabel#stat-title,
            QLabel#summary-title {
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 10px;
            }
            
            QLabel#stat-number,
            QLabel#summary-value {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            QLabel#stat-subtitle,
            QLabel#summary-trend {
                font-size: 12px;
                opacity: 0.8;
            }
            
            /* Perfil */
            QFrame#profile-frame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                margin: 10px 0;
            }
            
            QFrame#avatar-placeholder {
                background-color: #3498db;
                border-radius: 60px;
                color: white;
            }
            
            QLabel#avatar-initials {
                font-size: 48px;
                font-weight: bold;
                color: white;
            }
            
            QPushButton#change-avatar-btn {
                background-color: #34495e;
                color: white;
                border: 1px solid #ddd;
                padding: 5px 10px;
                border-radius: 3px;
                margin-top: 10px;
            }
            
            /* QR Code placeholder */
            QFrame#qrcode-placeholder {
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            
            /* Botões */
            QPushButton#save-button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 16px;
            }
            
            QPushButton#save-button:hover {
                background-color: #2980b9;
            }
            
            QPushButton#cancel-button {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton#cancel-button:hover {
                background-color: #c0392b;
            }
            
            /* Inputs */
            QLineEdit, QTextEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #3498db;
                outline: none;
            }
            
            QLineEdit:read-only {
                background-color: #f9f9f9;
                color: #666;
            }
            
            /* Tabelas */
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                gridline-color: #f0f0f0;
                selection-background-color: #e8f4f8;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            
            /* GroupBox */
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: white;
            }
            
            /* CheckBox */
            QCheckBox {
                spacing: 8px;
                color: #333;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
            }
            
            QCheckBox::indicator:checked:before {
                content: "✓";
                color: white;
                font-weight: bold;
            }
        """)

    def save_settings(self):
        """Salva as configurações"""
        # Implementar salvamento das configurações
        print("Configurações salvas!")
        self.settings_changed.emit({})

    def load_settings(self):
        """Carrega configurações salvas"""
        # Implementar carregamento das configurações
        pass