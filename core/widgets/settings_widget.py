from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QFormLayout, QSpinBox, QTabWidget,
                             QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import json
import os

class SettingsWidget(QWidget):
    """Widget nativo de configurações do navegador"""
    
    # Sinais
    settings_changed = pyqtSignal(dict)
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()
        self.setup_ui()
        self.apply_styles()
        
    def load_settings(self):
        """Carrega configurações salvas"""
        settings_file = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "user_settings.json"
        )
        
        default_settings = {
            "appearance": {
                "theme": "dark",
                "font_size": "medium"
            },
            "privacy": {
                "do_not_track": True,
                "block_third_party_cookies": False,
                "block_popups": True
            },
            "homepage": "file:///assets/html/painel.html",
            "search_engine": "google",
            "downloads": {
                "location": os.path.expanduser("~/Downloads"),
                "ask_before_download": True
            },
            "language": "pt_BR"
        }
        
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # Merge com configurações padrão
                    for key in default_settings:
                        if key in saved_settings:
                            if isinstance(default_settings[key], dict):
                                default_settings[key].update(saved_settings[key])
                            else:
                                default_settings[key] = saved_settings[key]
            return default_settings
        except:
            return default_settings
    
    def setup_ui(self):
        """Cria a interface de configurações"""
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Configurações")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabs de configurações
        self.tabs = QTabWidget()
        
        # Aba Aparência
        self.tabs.addTab(self.create_appearance_tab(), "🎨 Aparência")
        
        # Aba Privacidade
        self.tabs.addTab(self.create_privacy_tab(), "🔒 Privacidade")
        
        # Aba Navegação
        self.tabs.addTab(self.create_navigation_tab(), "🌐 Navegação")
        
        # Aba Downloads
        self.tabs.addTab(self.create_downloads_tab(), "📥 Downloads")
        
        # Aba Avançado
        self.tabs.addTab(self.create_advanced_tab(), "⚙️ Avançado")
        
        layout.addWidget(self.tabs)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.save_button = QPushButton("Salvar Configurações")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        self.reset_button = QPushButton("Restaurar Padrões")
        self.reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def create_appearance_tab(self):
        """Cria aba de aparência"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Grupo Tema
        theme_group = QGroupBox("Tema")
        theme_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Claro", "Escuro", "Sistema"])
        current_theme = {"light": 0, "dark": 1, "system": 2}.get(
            self.settings["appearance"]["theme"], 1
        )
        self.theme_combo.setCurrentIndex(current_theme)
        theme_layout.addRow("Tema:", self.theme_combo)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Grupo Fonte
        font_group = QGroupBox("Fonte")
        font_layout = QFormLayout()
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Pequeno", "Médio", "Grande"])
        current_size = {"small": 0, "medium": 1, "large": 2}.get(
            self.settings["appearance"]["font_size"], 1
        )
        self.font_size_combo.setCurrentIndex(current_size)
        font_layout.addRow("Tamanho:", self.font_size_combo)
        
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(50, 200)
        self.zoom_spin.setValue(100)
        self.zoom_spin.setSuffix("%")
        font_layout.addRow("Zoom padrão:", self.zoom_spin)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # Personalização
        custom_group = QGroupBox("Personalização")
        custom_layout = QVBoxLayout()
        
        self.show_bookmarks_check = QCheckBox("Mostrar barra de favoritos")
        self.show_bookmarks_check.setChecked(True)
        custom_layout.addWidget(self.show_bookmarks_check)
        
        self.show_home_button_check = QCheckBox("Mostrar botão página inicial")
        self.show_home_button_check.setChecked(True)
        custom_layout.addWidget(self.show_home_button_check)
        
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_privacy_tab(self):
        """Cria aba de privacidade"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Rastreamento
        tracking_group = QGroupBox("Rastreamento")
        tracking_layout = QVBoxLayout()
        
        self.do_not_track_check = QCheckBox("Enviar solicitação 'Não Rastrear'")
        self.do_not_track_check.setChecked(
            self.settings["privacy"]["do_not_track"]
        )
        tracking_layout.addWidget(self.do_not_track_check)
        
        tracking_group.setLayout(tracking_layout)
        layout.addWidget(tracking_group)
        
        # Cookies
        cookies_group = QGroupBox("Cookies")
        cookies_layout = QVBoxLayout()
        
        self.block_third_party_check = QCheckBox("Bloquear cookies de terceiros")
        self.block_third_party_check.setChecked(
            self.settings["privacy"]["block_third_party_cookies"]
        )
        cookies_layout.addWidget(self.block_third_party_check)
        
        self.clear_cookies_button = QPushButton("Limpar cookies e dados")
        self.clear_cookies_button.clicked.connect(self.clear_browsing_data)
        cookies_layout.addWidget(self.clear_cookies_button)
        
        cookies_group.setLayout(cookies_layout)
        layout.addWidget(cookies_group)
        
        # Pop-ups
        popup_group = QGroupBox("Pop-ups e redirecionamentos")
        popup_layout = QVBoxLayout()
        
        self.block_popups_check = QCheckBox("Bloquear pop-ups")
        self.block_popups_check.setChecked(
            self.settings["privacy"]["block_popups"]
        )
        popup_layout.addWidget(self.block_popups_check)
        
        popup_group.setLayout(popup_layout)
        layout.addWidget(popup_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_navigation_tab(self):
        """Cria aba de navegação"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Página inicial
        home_group = QGroupBox("Página Inicial")
        home_layout = QFormLayout()
        
        self.homepage_input = QLineEdit(self.settings["homepage"])
        home_layout.addRow("URL:", self.homepage_input)
        
        home_group.setLayout(home_layout)
        layout.addWidget(home_group)
        
        # Mecanismo de busca
        search_group = QGroupBox("Mecanismo de Busca")
        search_layout = QFormLayout()
        
        self.search_engine_combo = QComboBox()
        self.search_engine_combo.addItems([
            "Google", "Bing", "DuckDuckGo", "Yahoo", "Ecosia"
        ])
        engines = {"google": 0, "bing": 1, "duckduckgo": 2, "yahoo": 3, "ecosia": 4}
        self.search_engine_combo.setCurrentIndex(
            engines.get(self.settings["search_engine"], 0)
        )
        search_layout.addRow("Padrão:", self.search_engine_combo)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Abas
        tabs_group = QGroupBox("Abas")
        tabs_layout = QVBoxLayout()
        
        self.restore_tabs_check = QCheckBox("Restaurar abas ao iniciar")
        tabs_layout.addWidget(self.restore_tabs_check)
        
        self.warn_on_close_check = QCheckBox("Avisar ao fechar múltiplas abas")
        self.warn_on_close_check.setChecked(True)
        tabs_layout.addWidget(self.warn_on_close_check)
        
        tabs_group.setLayout(tabs_layout)
        layout.addWidget(tabs_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_downloads_tab(self):
        """Cria aba de downloads"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Local de download
        location_group = QGroupBox("Local de Download")
        location_layout = QHBoxLayout()
        
        self.download_location_input = QLineEdit(
            self.settings["downloads"]["location"]
        )
        location_layout.addWidget(self.download_location_input)
        
        self.browse_button = QPushButton("Procurar...")
        self.browse_button.clicked.connect(self.browse_download_location)
        location_layout.addWidget(self.browse_button)
        
        location_group.setLayout(location_layout)
        layout.addWidget(location_group)
        
        # Opções de download
        options_group = QGroupBox("Opções")
        options_layout = QVBoxLayout()
        
        self.ask_download_check = QCheckBox("Perguntar onde salvar cada arquivo")
        self.ask_download_check.setChecked(
            self.settings["downloads"]["ask_before_download"]
        )
        options_layout.addWidget(self.ask_download_check)
        
        self.open_pdf_check = QCheckBox("Abrir PDFs no navegador")
        self.open_pdf_check.setChecked(True)
        options_layout.addWidget(self.open_pdf_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_advanced_tab(self):
        """Cria aba avançada"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Cache
        cache_group = QGroupBox("Cache e Dados")
        cache_layout = QVBoxLayout()
        
        cache_info = QLabel("Cache pode acelerar o carregamento de páginas visitadas.")
        cache_info.setWordWrap(True)
        cache_layout.addWidget(cache_info)
        
        clear_cache_button = QPushButton("Limpar Cache")
        clear_cache_button.clicked.connect(self.clear_cache)
        cache_layout.addWidget(clear_cache_button)
        
        cache_group.setLayout(cache_layout)
        layout.addWidget(cache_group)
        
        # Hardware
        hardware_group = QGroupBox("Aceleração de Hardware")
        hardware_layout = QVBoxLayout()
        
        self.hardware_accel_check = QCheckBox("Usar aceleração de hardware quando disponível")
        self.hardware_accel_check.setChecked(True)
        hardware_layout.addWidget(self.hardware_accel_check)
        
        hardware_group.setLayout(hardware_layout)
        layout.addWidget(hardware_group)
        
        # Proxy
        proxy_group = QGroupBox("Configurações de Proxy")
        proxy_layout = QFormLayout()
        
        self.proxy_combo = QComboBox()
        self.proxy_combo.addItems([
            "Sem proxy", 
            "Usar configurações do sistema", 
            "Configuração manual"
        ])
        proxy_layout.addRow("Tipo:", self.proxy_combo)
        
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def apply_styles(self):
        """Aplica estilos ao widget"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-size: 14px;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QLineEdit, QComboBox, QSpinBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            
            QCheckBox {
                spacing: 8px;
            }
            
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 15px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3498db;
            }
        """)
    
    def save_settings(self):
        """Salva as configurações"""
        # Coletar valores atuais
        self.settings["appearance"]["theme"] = ["light", "dark", "system"][
            self.theme_combo.currentIndex()
        ]
        self.settings["appearance"]["font_size"] = ["small", "medium", "large"][
            self.font_size_combo.currentIndex()
        ]
        
        self.settings["privacy"]["do_not_track"] = self.do_not_track_check.isChecked()
        self.settings["privacy"]["block_third_party_cookies"] = self.block_third_party_check.isChecked()
        self.settings["privacy"]["block_popups"] = self.block_popups_check.isChecked()
        
        self.settings["homepage"] = self.homepage_input.text()
        self.settings["search_engine"] = ["google", "bing", "duckduckgo", "yahoo", "ecosia"][
            self.search_engine_combo.currentIndex()
        ]
        
        self.settings["downloads"]["location"] = self.download_location_input.text()
        self.settings["downloads"]["ask_before_download"] = self.ask_download_check.isChecked()
        
        # Salvar em arquivo
        config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")
        os.makedirs(config_dir, exist_ok=True)
        
        settings_file = os.path.join(config_dir, "user_settings.json")
        
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            
            # Emitir sinal de mudança
            self.settings_changed.emit(self.settings)
            
            # Mostrar confirmação
            QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configurações: {str(e)}")
    
    def reset_settings(self):
        """Restaura configurações padrão"""
        reply = QMessageBox.question(
            self, 
            "Confirmar",
            "Tem certeza que deseja restaurar as configurações padrão?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Recarregar configurações padrão
            self.settings = {
                "appearance": {
                    "theme": "dark",
                    "font_size": "medium"
                },
                "privacy": {
                    "do_not_track": True,
                    "block_third_party_cookies": False,
                    "block_popups": True
                },
                "homepage": "file:///assets/html/painel.html",
                "search_engine": "google",
                "downloads": {
                    "location": os.path.expanduser("~/Downloads"),
                    "ask_before_download": True
                },
                "language": "pt_BR"
            }
            
            # Atualizar UI
            self.theme_combo.setCurrentIndex(1)
            self.font_size_combo.setCurrentIndex(1)
            self.do_not_track_check.setChecked(True)
            self.block_third_party_check.setChecked(False)
            self.block_popups_check.setChecked(True)
            self.homepage_input.setText("file:///assets/html/painel.html")
            self.search_engine_combo.setCurrentIndex(0)
            self.download_location_input.setText(os.path.expanduser("~/Downloads"))
            self.ask_download_check.setChecked(True)
            
            QMessageBox.information(self, "Sucesso", "Configurações restauradas!")
    
    def browse_download_location(self):
        """Abre diálogo para escolher pasta de download"""
        from PyQt6.QtWidgets import QFileDialog
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Escolher pasta de downloads",
            self.download_location_input.text()
        )
        
        if folder:
            self.download_location_input.setText(folder)
    
    def clear_browsing_data(self):
        """Limpa dados de navegação"""
        reply = QMessageBox.question(
            self,
            "Limpar dados",
            "Isso irá limpar todos os cookies e dados de sites. Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Aqui você implementaria a limpeza real
            QMessageBox.information(self, "Sucesso", "Dados de navegação limpos!")
    
    def clear_cache(self):
        """Limpa o cache"""
        reply = QMessageBox.question(
            self,
            "Limpar cache",
            "Isso irá limpar todo o cache do navegador. Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Aqui você implementaria a limpeza real
            QMessageBox.information(self, "Sucesso", "Cache limpo com sucesso!")