# Lógica da janela principal (QMainWindow)

import os
import traceback
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QPoint, pyqtSignal
from PyQt6.QtGui import QMouseEvent

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QAction as QActionGui
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMenu, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

from core.widgets.login_widget import LoginWidget
from core.widgets.register_widget import RegisterWidget
from core.tabs import DraggableTabWidget
from crud.crud_manager import crud_system
from database.sqlalchemy_config import db_config
from utils.html_utils import ensure_login_page_exists
from utils.json_utils import load_language_names, load_translations
from utils.style_utils import load_stylesheet


class TranslatorPopup(QDialog):
    """Pop-up arrastável com Google Tradutor"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Google Tradutor")
        self.setFixedSize(500, 600)
        self.setModal(False)  # Permite interação com a janela principal
        
        # Variáveis para arrastar
        self.drag_position = QPoint()
        
        # Remove a barra de título padrão para criar uma personalizada
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        """Configura a interface do pop-up"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Barra de título personalizada
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(30)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: #34495e;
                border-bottom: 1px solid #2c3e50;
            }
        """)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 5, 5, 5)
        
        # Título
        title_label = QLabel("Google Tradutor")
        title_label.setStyleSheet("color: white; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Botão fechar
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                border-radius: 3px;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        layout.addWidget(self.title_bar)
        
        # WebView com Google Tradutor
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://translate.google.com"))
        layout.addWidget(self.web_view)
        
    def setup_styles(self):
        """Aplica estilos ao pop-up"""
        self.setStyleSheet("""
            QDialog {
                background-color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 8px;
            }
        """)
        
    def mousePressEvent(self, event: QMouseEvent):
        """Inicia o arraste quando clica na barra de título"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Verifica se clicou na barra de título
            if event.position().y() <= 30:  # Altura da barra de título
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        """Move a janela durante o arraste"""
        if event.buttons() == Qt.MouseButton.LeftButton and not self.drag_position.isNull():
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Finaliza o arraste"""
        self.drag_position = QPoint()


class ChromeClone(QMainWindow):
    # -------------------------------
    # 🛠️ Método construtor
    # -------------------------------
    def __init__(self, parent=None, url=None):
        try:
            super().__init__(parent)

            # Inicializar o sistema CRUD
            self.crud = crud_system

            if self.crud.is_connected():
                print('✅ Sistema CRUD carregado e conectado!')
            else:
                print('⚠️ Sistema CRUD carregado mas sem conexão com BD')

            self.current_language = "pt_BR"
            self.translations = load_translations()
            self.language_names = load_language_names()

            self.current_user = None

            self.setup_window()
            self.setup_navigation_bar()
            self.setup_tabs()
            self.setup_sidebar_menu()

            self.show_login_page()

        except Exception as e:
            print(f"ERRO CRÍTICO durante inicialização do ChromeClone: {e}")
            traceback.print_exc()
            raise
    
    def show_login_page(self):
        """Mostra o widget de login nativo"""
        # Criar widget de login
        login_widget = LoginWidget()
        
        # Conectar sinais
        login_widget.login_successful.connect(self.on_login_successful)
        login_widget.switch_to_register.connect(self.show_register_page)
        
        # Limpar abas e adicionar widget
        self.clear_all_tabs()
        index = self.tabs.addTab(login_widget, "Login")
        self.tabs.setCurrentIndex(index)
        
        # Desabilitar navegação durante login
        self.nav_bar.setEnabled(False)
        self.menu_button.setEnabled(False)
    
    def show_register_page(self):
        """Mostra o widget de registro nativo"""
        # Criar widget de registro
        register_widget = RegisterWidget()
        
        # Conectar sinais
        register_widget.register_successful.connect(self.on_register_successful)
        register_widget.switch_to_login.connect(self.show_login_page)
        
        # Limpar abas e adicionar widget
        self.clear_all_tabs()
        index = self.tabs.addTab(register_widget, "Criar Conta")
        self.tabs.setCurrentIndex(index)
    
    def on_login_successful(self, user_id, username):
        """Callback quando login é bem-sucedido"""
        print(f"✅ Login bem-sucedido: {username} (ID: {user_id})")
        
        # Armazenar usuário atual
        self.current_user = {
            'id': user_id,
            'username': username
        }
        
        # Habilitar navegação
        self.nav_bar.setEnabled(True)
        self.menu_button.setEnabled(True)
        
        # Carregar painel principal
        self.show_main_panel()
    
    def on_register_successful(self, username, name):
        """Callback quando registro é bem-sucedido"""
        print(f"✅ Registro bem-sucedido: {username} ({name})")
        
        # Voltar para login
        self.show_login_page()
    
    def show_main_panel(self):
        """Carrega o painel principal (HTML estático)"""
        # Limpar abas
        self.clear_all_tabs()
        
        # Carregar painel HTML (sem pontes JS!)
        panel_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "html", "painel.html"
        ).replace("\\", "/")
        
        self.add_new_tab(f"file:///{panel_path}")
    
    def clear_all_tabs(self):
        """Remove todas as abas"""
        while self.tabs.count() > 0:
            self.tabs.removeTab(0)
    
    def add_new_tab(self, url):
        """Versão simplificada sem pontes JS"""
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        
        # Conectar sinais básicos
        browser.urlChanged.connect(
            lambda qurl: self.url_bar.setText(qurl.toString())
        )
        
        index = self.tabs.addTab(browser, self.get_translation("new_tab"))
        self.tabs.setCurrentIndex(index)
        
        return browser

    # -------------------------------
    # ⚙️ Métodos auxiliares
    # -------------------------------
    def open_login_page(self):
        """Abrir página de login"""
        login_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "html", "login.html"
        ).replace("\\", "/")

        # Garante que existe pelo menos uma aba
        if self.tabs.count() == 0:
            self.add_new_tab(f"file:///{login_path}")
        else:
            self.load_url_from_text(f"file:///{login_path}")
    
    def open_register_page(self):
        """Abrir página de registro"""
        register_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "html", "register.html"
        ).replace("\\", "/")

        # Garante que existe pelo menos uma aba
        if self.tabs.count() == 0:
            self.add_new_tab(f"file:///{register_path}")
        else:
            self.load_url_from_text(f"file:///{register_path}")
    
    def open_panel_page(self):
        """Abrir página do painel"""
        panel_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "html", "painel.html"
        ).replace("\\", "/")
        
        # Garante que existe pelo menos uma aba
        if self.tabs.count() == 0:
            self.add_new_tab(f"file:///{panel_path}")
        else:
            self.load_url_from_text(f"file:///{panel_path}")

    def setup_window(self):
        self.setWindowTitle(self.get_translation("browser_title"))
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #2c3e50;")

        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

    def setup_navigation_bar(self):
        self.nav_bar = QWidget()
        self.nav_layout = QHBoxLayout()
        self.nav_bar.setLayout(self.nav_layout)
        self.nav_layout.setContentsMargins(8, 6, 8, 6)
        self.nav_layout.setSpacing(8)

        self.nav_bar.setStyleSheet(load_stylesheet("nav_bar.css"))

        self.back_btn = QPushButton("◀")
        self.back_btn.setToolTip("Voltar")
        self.back_btn.clicked.connect(lambda: self.go_back())

        self.forward_btn = QPushButton("▶")
        self.forward_btn.setToolTip("Avançar")
        self.forward_btn.clicked.connect(lambda: self.go_forward())

        self.reload_btn = QPushButton("↻")
        self.reload_btn.setToolTip("Atualizar")
        self.reload_btn.clicked.connect(lambda: self.reload_page())

        self.home_btn = QPushButton("⌂")
        self.home_btn.setToolTip("Página Inicial")

        painel_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "assets",
            "html",
            "painel.html",
        )
        painel_path = painel_path.replace("\\", "/")
        self.home_btn.clicked.connect(
            lambda: self.load_url_from_text(f"file:///{painel_path}")
        )

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText(self.get_translation("search_placeholder"))
        self.url_bar.returnPressed.connect(self.load_url)
        self.url_bar.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        # NOVO: Botão Tradutor
        self.translator_btn = QPushButton("🌐 Tradutor")
        self.translator_btn.setToolTip("Abrir Google Tradutor")
        self.translator_btn.clicked.connect(self.open_translator_popup)
        self.translator_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)

        self.menu_button = QPushButton("☰")
        self.menu_button.setToolTip("Menu")
        self.menu_button.clicked.connect(self.toggle_menu)

        # Adiciona todos os widgets na ordem correta
        for widget in [
            self.back_btn,
            self.forward_btn,
            self.reload_btn,
            self.home_btn,
            self.url_bar,
            self.translator_btn,  # NOVO: Botão tradutor entre url_bar e menu
            self.menu_button,
        ]:
            self.nav_layout.addWidget(widget)

        self.main_layout.addWidget(self.nav_bar)

    def setup_tabs(self):
        self.horizontal_layout = QHBoxLayout()
        self.main_layout.addLayout(self.horizontal_layout)

        self.tabs = DraggableTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabDetached.connect(self.detach_tab)

        self.tabs.setCornerWidget(
            self.create_new_tab_button(), Qt.Corner.TopRightCorner
        )

        self.horizontal_layout.addWidget(self.tabs)

        self.tabs.setStyleSheet("""
    QTabBar::tab {
        color: #ffffff;  
    }
    
    QTabBar::tab:selected {
        font-weight: bold;
    }
""")

    def show_settings_widget(self):
        """Mostra o widget de configurações nativo"""
        from core.widgets.settings_widget import SettingsWidget

        # Criar widget
        settings_widget = SettingsWidget()

        # Conectar sinais
        settings_widget.settings_changed.connect(self.apply_settings)
        settings_widget.theme_changed.connect(self.change_theme)

        # Adicionar como nova aba
        index = self.tabs.addTab(settings_widget, "⚙️ Configurações")
        self.tabs.setCurrentIndex(index)

        # Esconder menu
        self.menu_widget.setVisible(False)

    def apply_settings(self, settings):
        """Aplica as configurações ao navegador"""
        # Aplicar tema
        if settings["appearance"]["theme"] == "dark":
            self.setStyleSheet("background-color: #2c3e50;")
        elif settings["appearance"]["theme"] == "light":
            self.setStyleSheet("background-color: #f0f0f0;")

        # Outras configurações seriam aplicadas aqui
        print(f"Configurações aplicadas: {settings}")

    def change_theme(self, theme):
        """Muda o tema do navegador"""
        # Implementar mudança de tema
        pass

    def show_notifications_widget(self):
        """Mostra o widget de notificações nativo"""
        from core.widgets.notifications_widget import NotificationsWidget
        
        # Criar widget
        notifications_widget = NotificationsWidget()
        
        # Conectar sinais
        notifications_widget.notification_clicked.connect(self.handle_notification_click)
        
        # Adicionar como nova aba
        index = self.tabs.addTab(notifications_widget, "🔔 Notificações")
        self.tabs.setCurrentIndex(index)
        
        # Esconder menu
        self.menu_widget.setVisible(False)
        
    def handle_notification_click(self, notification_data):
        """Processa clique em notificação"""
        print(f"Notificação clicada: {notification_data}")
        
        # Aqui você pode implementar ações específicas para cada tipo de notificação
        if notification_data.get('title') == 'Atualização disponível':
            # Abrir página de atualizações
            pass
    def show_rewards_widget(self):
        """Mostra o widget de recompensas nativo"""
        from core.widgets.rewards_widget import RewardsWidget

        # Criar widget
        rewards_widget = RewardsWidget()

        # Adicionar como nova aba
        index = self.tabs.addTab(rewards_widget, "⭐ Recompensas")
        self.tabs.setCurrentIndex(index)

        # Esconder menu
        self.menu_widget.setVisible(False)
    
    def setup_sidebar_menu(self):
        """Configura o menu lateral com handlers funcionais"""
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_widget)
        self.menu_widget.setFixedWidth(200)
        self.menu_widget.setVisible(False)
        self.menu_widget.setStyleSheet(load_stylesheet("menu_widget.css"))

        self.menu_layout.setContentsMargins(10, 15, 10, 15)
        self.menu_layout.setSpacing(8)

        # Título do menu
        self.menu_title = QLabel(self.get_translation("menu"))
        self.menu_title.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            padding: 5px;
            border-bottom: 1px solid #3498db;
        """)
        self.menu_layout.addWidget(self.menu_title)

        # Itens do menu - AGORA COM HANDLERS CORRETOS
        menu_items = [
            ("⚙️", "settings", self.show_settings_widget),      # Novo handler
            ("🔔", "notifications", self.show_notifications_widget),  # Novo handler
            ("⭐", "rewards", self.show_rewards_widget),        # Novo handler
            ("🌐", "language", self.show_language_menu),        # Mantém existente
            ("↩️", "exit", self.exit_application),             # Mantém existente
        ]

        for icon, key, handler in menu_items:
            btn = QPushButton(f"{icon}  {self.get_translation(key)}")
            btn.clicked.connect(handler)
            self.menu_layout.addWidget(btn)

        # Espaçador
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.menu_layout.addWidget(spacer)

        self.horizontal_layout.addWidget(self.menu_widget)


    def load_initial_page(self, url):
        if url:
            self.add_new_tab(url)
        else:
            login_page = ensure_login_page_exists()
            self.add_new_tab(f"file:///{login_page}")

    # -------------------------------
    # 🧭 Navegação
    # -------------------------------
    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith(("http", "file", "about")):
            url = "https://" + url
        if self.tabs.currentWidget():
            self.tabs.currentWidget().setUrl(QUrl(url))

    def go_back(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().back()

    def go_forward(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().forward()

    def reload_page(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().reload()

    # -------------------------------
    # 📑 Abas
    # -------------------------------
    def add_new_tab(self, url):
        """Versão super simplificada"""
        try:
            browser = QWebEngineView()
            page = browser.page()
            
            # Configurar WebChannel ANTES de tudo
            channel = QWebChannel(page)
            channel.registerObject("unifiedBridge", self.unified_bridge)
            page.setWebChannel(channel)
            
            # Hook para injetar script DEPOIS que página carregar
            page.loadFinished.connect(lambda success: self.inject_minimal_bridge(page) if success else None)
            
            # Carregar URL
            browser.setUrl(QUrl(url))
            
            # Adicionar aba
            index = self.tabs.addTab(browser, self.get_translation("new_tab"))
            self.tabs.setCurrentIndex(index)
            
            return browser
            
        except Exception as e:
            print(f"❌ Erro ao criar aba: {e}")
            return None
    
    def inject_minimal_bridge(self, page):
        """Injetar script mínimo com QWebChannel garantido"""
        try:
            print("🔧 Injetando ponte mínima...")
            
            # Passo 1: Garantir QWebChannel
            qwebchannel_guarantee = '''
                console.log("Ensuring QWebChannel...");
                if (typeof QWebChannel === 'undefined') {
                    console.log("Loading QWebChannel script...");
                    var script = document.createElement('script');
                    script.src = 'qrc:///qtwebchannel/qwebchannel.js';
                    script.type = 'text/javascript';
                    document.head.appendChild(script);
                } else {
                    console.log("QWebChannel already available");
                }
            '''
            
            page.runJavaScript(qwebchannel_guarantee)
            
            # Passo 2: Aguardar e carregar script principal
            QTimer.singleShot(1000, lambda: self._inject_main_script(page))
            
        except Exception as e:
            print(f"❌ Erro na injeção: {e}")
    
    def _inject_main_script(self, page):
        """Carregar script principal"""
        try:
            script_path = os.path.join(
                os.path.dirname(__file__), "..", "assets", "js", "minimal_bridge.js"
            )
            
            if not os.path.exists(script_path):
                print(f"❌ Script mínimo não encontrado: {script_path}")
                return
                
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            page.runJavaScript(script_content)
            print("✅ Ponte mínima injetada")
            
        except Exception as e:
            print(f"❌ Erro ao carregar script: {e}")
    
        def inject_simple_bridge(self, page):
            """Injetar script simplificado e limpo"""
            try:
                # Carregar o novo script limpo
                script_path = os.path.join(
                    os.path.dirname(__file__), "..", "assets", "js", "clean_bridge_loader.js"
                )
    
                if not os.path.exists(script_path):
                    print(f"❌ Script não encontrado: {script_path}")
                    return
    
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_content = f.read()
    
                # Injetar o script
                page.runJavaScript(script_content)
                print("✅ Ponte unificada limpa injetada")
    
            except Exception as e:
                print(f"❌ Erro ao injetar script limpo: {e}")
                import traceback
                traceback.print_exc()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def detach_tab(self, index, drop_pos, web_view):
        """Cria uma nova janela quando uma aba é arrastada para fora"""
        try:
            # Verifica se o índice é válido
            if index < 0 or index >= self.tabs.count():
                print(f"Índice de aba inválido: {index}")
                return

            # Obtém o texto da aba
            tab_text = self.tabs.tabText(index)

            # Armazena o widget da aba para não ser destruído quando removermos a aba
            web_view = self.tabs.widget(index)
            if not web_view:
                print("Não foi possível obter o widget da aba")
                return

            # Evita que o widget seja destruído quando a aba for removida
            web_view.setParent(None)

            # Remove a aba da janela atual
            self.tabs.removeTab(index)

            # Cria uma nova instância do navegador
            new_window = ChromeClone(None)

            # Adiciona o widget da web à nova janela
            new_window.add_existing_tab(web_view, tab_text)

            # Posiciona a nova janela perto de onde a aba foi solta
            new_window.move(drop_pos.x() - 100, drop_pos.y() - 50)
            new_window.resize(self.size())  # Mantém o mesmo tamanho da janela original

            # Mostra a nova janela e traz para a frente
            new_window.show()
            new_window.activateWindow()

            # Se não sobrou nenhuma aba na janela atual, adiciona uma aba vazia
            if self.tabs.count() == 0:
                self.add_new_tab("about:blank")

            print(f"Aba destacada com sucesso: {tab_text}")

        except Exception as e:
            print(f"Erro ao destacar aba: {e}")
            traceback.print_exc()
            # Garante que sempre haja uma aba disponível
            if self.tabs.count() == 0:
                self.add_new_tab("about:blank")

    def create_new_tab_button(self):
        """Cria um botão de nova aba para ser adicionado ao canto do widget de abas"""
        NovaPagina = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "assets",
            "html",
            "painel.html",
        ).replace("\\", "/")

        new_tab_btn = QPushButton("+")
        new_tab_btn.setToolTip(self.get_translation("new_tab"))
        new_tab_btn.clicked.connect(lambda: self.add_new_tab(f"file:///{NovaPagina}"))

        # Estilo para combinar com o restante da interface
        new_tab_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                margin: 2px;
                font-weight: bold;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """
        )

        return new_tab_btn

    def add_existing_tab(self, web_view, tab_title=None):
        """Adiciona uma vista web existente como uma nova aba"""
        try:
            if tab_title is None:
                tab_title = self.get_translation("new_tab")

            index = self.tabs.addTab(web_view, tab_title)

            # Conecta o sinal loadFinished
            web_view.loadFinished.connect(self.on_page_loaded)

            # Configura o canal de comunicação para a aba
            self.create_web_channel(web_view)

            # Seleciona automaticamente a nova aba
            self.tabs.setCurrentIndex(index)
            return index
        except Exception as e:
            print(f"Erro ao adicionar aba existente: {e}")
            traceback.print_exc()
            return -1

    # -------------------------------
    # 🎛️ Menu lateral
    # -------------------------------
    def toggle_menu(self):
        # Alterna a visibilidade do menu lateral
        self.menu_widget.setVisible(not self.menu_widget.isVisible())

    def open_settings(self):
        settings_page = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "assets",
            "html",
            "settings.html",
        ).replace("\\", "/")

        # Verificar e criar o arquivo settings.html caso não exista
        if not os.path.isfile(settings_page):
            settings_dir = os.path.dirname(settings_page)
            os.makedirs(settings_dir, exist_ok=True)

            with open(settings_page, "w", encoding="utf-8") as f:
                f.write(
                    """<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Configurações</title>
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            background-color: #f0f0f0;
                            margin: 0;
                            padding: 20px;
                        }
                        h1 { color: #2c3e50; }
                        .settings-container {
                            background-color: white;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                            max-width: 800px;
                            margin: 0 auto;
                        }
                        .setting-group {
                            margin-bottom: 20px;
                            padding-bottom: 20px;
                            border-bottom: 1px solid #eee;
                        }
                        h2 {
                            color: #3498db;
                            font-size: 18px;
                        }
                        label {
                            display: block;
                            margin: 10px 0 5px;
                            font-weight: bold;
                        }
                        select, input {
                            width: 100%;
                            padding: 8px;
                            border: 1px solid #ddd;
                            border-radius: 4px;
                            box-sizing: border-box;
                            margin-bottom: 10px;
                        }
                        button {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            padding: 10px 15px;
                            border-radius: 4px;
                            cursor: pointer;
                        }
                        button:hover {
                            background-color: #2980b9;
                        }
                    </style>
                </head>
                <body>
                    <div class="settings-container">
                        <h1>Configurações</h1>
                        
                        <div class="setting-group">
                            <h2>Aparência</h2>
                            <label for="theme">Tema:</label>
                            <select id="theme">
                                <option value="light">Claro</option>
                                <option value="dark" selected>Escuro</option>
                                <option value="system">Sistema</option>
                            </select>
                            
                            <label for="font-size">Tamanho da fonte:</label>
                            <select id="font-size">
                                <option value="small">Pequeno</option>
                                <option value="medium" selected>Médio</option>
                                <option value="large">Grande</option>
                            </select>
                        </div>
                        
                        <div class="setting-group">
                            <h2>Privacidade e Segurança</h2>
                            <label>
                                <input type="checkbox" id="do-not-track" checked> 
                                Ativar "Não Rastrear"
                            </label>
                            <br>
                            <label>
                                <input type="checkbox" id="block-cookies"> 
                                Bloquear cookies de terceiros
                            </label>
                            <br>
                            <label>
                                <input type="checkbox" id="block-popups" checked> 
                                Bloquear pop-ups
                            </label>
                        </div>
                        
                        <div class="setting-group">
                            <h2>Página Inicial</h2>
                            <label for="homepage">URL da página inicial:</label>
                            <input type="text" id="homepage" value="file:///assets/html/painel.html">
                        </div>
                        
                        <div class="setting-group">
                            <h2>Pesquisa</h2>
                            <label for="search-engine">Mecanismo de pesquisa padrão:</label>
                            <select id="search-engine">
                                <option value="google" selected>Google</option>
                                <option value="bing">Bing</option>
                                <option value="duckduckgo">DuckDuckGo</option>
                                <option value="ecosia">Ecosia</option>
                            </select>
                        </div>
                        
                        <button id="save-settings">Salvar Configurações</button>
                    </div>
                    
                    <script>
                        document.getElementById('save-settings').addEventListener('click', function() {
                            alert('Configurações salvas com sucesso!');
                        });
                    </script>
                </body>
                </html>"""
                )
            print(f"Arquivo criado: {settings_page}")

        self.add_new_tab(f"file:///{settings_page}")
        self.tabs.setCurrentIndex(
            self.tabs.count() - 1
        )  # Muda para a aba de configurações imediatamente
        # Esconde o menu após a seleção
        self.menu_widget.setVisible(False)

    def show_notifications(self):
        print("Mostrar notificações")  # Implementar lógica para mostrar notificações
        # Esconde o menu após a seleção
        self.menu_widget.setVisible(False)

    def show_rewards(self):
        print("Mostrar recompensas")  # Implementar lógica para mostrar recompensas
        # Esconde o menu após a seleção
        self.menu_widget.setVisible(False)

    # -------------------------------
    # 🌍 Idiomas
    # -------------------------------
    def get_translation(self, key):
        """Recupera a tradução para uma chave específica no idioma atual"""
        return self.translations.get(self.current_language, {}).get(key, key)

    def show_language_menu(self):
        """Exibe menu de seleção de idioma"""
        language_menu = QMenu(self)

        # Adiciona opções de idioma ao menu
        for lang_code, lang_name in self.language_names.items():
            action = QActionGui(lang_name, self)
            action.triggered.connect(
                lambda checked, lc=lang_code: self.change_language(lc)
            )
            # Marca o idioma atual
            if lang_code == self.current_language:
                action.setCheckable(True)
                action.setChecked(True)
            language_menu.addAction(action)

        # Exibe o menu abaixo do botão de idioma
        language_menu.exec(
            self.language_btn.mapToGlobal(self.language_btn.rect().bottomLeft())
        )

    def change_language(self, lang_code):
        """Muda o idioma da interface e traduz as páginas"""
        if lang_code == self.current_language:
            return

        # Salva URL atual antes de traduzir
        current_url = None
        if self.tabs.currentWidget():
            current_url = self.tabs.currentWidget().url().toString()

            # Se já estiver em uma página traduzida pelo Google, obtém a URL original
            if "translate.google.com/translate" in current_url:
                try:
                    # Extrai a URL original da URL de tradução do Google
                    import urllib.parse

                    params = dict(
                        urllib.parse.parse_qsl(urllib.parse.urlsplit(current_url).query)
                    )
                    if "u" in params:
                        current_url = params["u"]
                except Exception as e:
                    print(f"Erro ao extrair URL original: {e}")

        # Atualiza o idioma atual
        self.current_language = lang_code

        # Atualiza os textos da interface
        self.setWindowTitle(self.get_translation("browser_title"))
        self.url_bar.setPlaceholderText(self.get_translation("search_placeholder"))
        self.menu_title.setText(self.get_translation("menu"))
        self.settings_btn.setText(f"⚙️  {self.get_translation('settings_page')}")
        self.notifications_btn.setText(f"🔔  {self.get_translation('notifications')}")
        self.rewards_btn.setText(f"⭐  {self.get_translation('rewards')}")
        self.download_btn.setText(
            f"📥  {self.get_translation('download')}"
        )  # Nova opção de Download
        self.language_btn.setText(f"🌐  {self.get_translation('language')}")
        self.exit_btn.setText(f"↩️  {self.get_translation('exit')}")

        # Atualiza os nomes das abas
        for i in range(self.tabs.count()):
            self.tabs.setTabText(i, self.get_translation("new_tab"))

        # Se temos uma URL válida, recarrega a página para traduzir
        if current_url and not current_url.startswith(("about:", "chrome:", "file:")):
            # Traduz a página atual se possível
            self.translate_current_page()

        print(f"Idioma alterado para: {self.language_names[lang_code]}")

    def translate_current_page(self):
        """Traduz o conteúdo da página atual usando tradução local para arquivos locais e Google Translate para sites"""
        # Mapeamento de códigos de idioma para códigos que o Google Translate aceita
        google_lang_codes = {"pt_BR": "pt", "pt_PT": "pt", "en": "en", "es": "es"}

        # Verifica se há widget atual e obtém a URL
        if not self.tabs.currentWidget():
            return

        current_url = self.tabs.currentWidget().url().toString()
        target_lang = google_lang_codes.get(self.current_language, "en")

        # Para páginas locais (file://), usamos JavaScript para traduzir diretamente
        if current_url.startswith("file://"):
            # Injetar tradução direta para páginas locais
            # Vamos usar a API JavaScript do Google Translate
            script = f"""
            (function() {{
                // Este script traduz páginas locais
                try {{
                    // Adicionar o elemento de tradução do Google
                    var gtElem = document.createElement('div');
                    gtElem.id = 'google_translate_element';
                    gtElem.style.position = 'fixed';
                    gtElem.style.bottom = '0';
                    gtElem.style.right = '0';
                    gtElem.style.zIndex = '9999';
                    document.body.appendChild(gtElem);
                    
                    // Adicionar o script de tradução do Google
                    var script = document.createElement('script');
                    script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
                    
                    // Definir a função de inicialização
                    window.googleTranslateElementInit = function() {{
                        new google.translate.TranslateElement({{
                            pageLanguage: 'auto',
                            includedLanguages: '{target_lang}',
                            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
                            autoDisplay: false
                        }}, 'google_translate_element');
                        
                        // Selecionar o idioma automaticamente
                        setTimeout(function() {{
                            // Encontrar e clicar no seletor de idioma
                            var selectElement = document.querySelector('.goog-te-combo');
                            if (selectElement) {{
                                selectElement.value = '{target_lang}';
                                selectElement.dispatchEvent(new Event('change'));
                            }}
                            
                            // Ocultar o widget de tradução após selecionar o idioma
                            setTimeout(function() {{
                                var translateWidget = document.getElementById('google_translate_element');
                                if (translateWidget) {{
                                    translateWidget.style.display = 'none';
                                }}
                            }}, 1000);
                        }}, 1000);
                    }};
                    
                    // Adicionar o script ao documento
                    document.body.appendChild(script);
                    
                }} catch (e) {{
                    console.error('Erro ao traduzir página local:', e);
                }}
            }})();
            """

            # Executar o script JavaScript
            self.tabs.currentWidget().page().runJavaScript(script)

            # Executar novamente após um pequeno atraso para garantir que funcione
            QTimer.singleShot(
                3000, lambda: self.tabs.currentWidget().page().runJavaScript(script)
            )

        # Para páginas about: ou chrome:, ignoramos a tradução
        elif current_url.startswith(("about:", "chrome:")):
            return

        # Para páginas da web normais, usamos o redirecionamento para o Google Translate
        elif not current_url.startswith("https://translate.google.com"):
            # URL de tradução do Google (traduz a página inteira)
            translate_url = f"https://translate.google.com/translate?sl=auto&tl={target_lang}&u={current_url}"

            # Carrega a URL de tradução
            self.tabs.currentWidget().setUrl(QUrl(translate_url))

    # -------------------------------
    # 🔐 Sessão
    # -------------------------------
    def exit_application(self):
        # Esconde o menu e sai da aplicação
        self.menu_widget.setVisible(False)
        QApplication.quit()  # Sair da aplicação

        # inicio da parte do Dowloads

        # inicio da parte do Dowloads

    def open_translator_popup(self):
        """Abre o pop-up do Google Tradutor"""
        try:
            # Verifica se já existe um pop-up aberto
            if hasattr(self, 'translator_popup') and self.translator_popup.isVisible():
                # Se já estiver aberto, traz para frente
                self.translator_popup.raise_()
                self.translator_popup.activateWindow()
                return
                
            # Cria novo pop-up
            self.translator_popup = TranslatorPopup(self)
            
            # Posiciona o pop-up no centro da janela principal
            parent_geo = self.geometry()
            popup_width = 500
            popup_height = 600
            
            x = parent_geo.x() + (parent_geo.width() - popup_width) // 2
            y = parent_geo.y() + (parent_geo.height() - popup_height) // 2
            
            self.translator_popup.move(x, y)
            
            # Mostra o pop-up
            self.translator_popup.show()
            self.translator_popup.raise_()
            self.translator_popup.activateWindow()
            
            print("Pop-up do Google Tradutor aberto com sucesso!")
            
        except Exception as e:
            print(f"Erro ao abrir pop-up do tradutor: {e}")
            traceback.print_exc()



   