from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from crud.database_adapter import crud_system

class LoginWidget(QWidget):
    """Widget nativo PyQt6 para login - sem JavaScript!"""
    
    # Sinais para comunicação pythônica
    login_successful = pyqtSignal(str, str)  # user_id, username
    switch_to_register = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Cria a interface de login"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo/Título
        title = QLabel("UP Browser")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Faça login para continuar")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Campo de usuário
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário ou E-mail")
        self.username_input.setMinimumHeight(40)
        layout.addWidget(self.username_input)
        
        # Campo de senha
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        layout.addWidget(self.password_input)
        
        # Checkbox "Lembrar-me"
        self.remember_checkbox = QCheckBox("Lembrar-me")
        layout.addWidget(self.remember_checkbox)
        
        # Botão de login
        self.login_button = QPushButton("Entrar")
        self.login_button.setMinimumHeight(45)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setDefault(True)  # Enter key triggers login
        layout.addWidget(self.login_button)
        
        # Link para registro
        register_layout = QHBoxLayout()
        register_layout.addStretch()
        
        register_label = QLabel("Não possui conta?")
        register_layout.addWidget(register_label)
        
        self.register_button = QPushButton("Cadastre-se")
        self.register_button.setFlat(True)
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.switch_to_register.emit)
        register_layout.addWidget(self.register_button)
        
        register_layout.addStretch()
        layout.addLayout(register_layout)
        
        # Adicionar espaço no final
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Conectar Enter key nos campos
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def apply_styles(self):
        """Aplica estilos CSS ao widget"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            
            QLabel {
                color: #ffffff;
            }
            
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
                color: black;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
                color: black;
            }
            
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:pressed {
                background-color: #004085;
            }
            
            QPushButton[flat="true"] {
                background-color: transparent;
                color: #007bff;
                font-weight: normal;
                text-decoration: underline;
            }
            
            QPushButton[flat="true"]:hover {
                color: #0056b3;
            }
            
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
            }
        """)
    
    def handle_login(self):
        """Processa o login - TUDO EM PYTHON!"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # Validações
        if not username:
            QMessageBox.warning(self, "Aviso", "Por favor, digite seu usuário ou e-mail")
            self.username_input.setFocus()
            return
            
        if not password:
            QMessageBox.warning(self, "Aviso", "Por favor, digite sua senha")
            self.password_input.setFocus()
            return
        
        # Desabilitar botão durante o processo
        self.login_button.setEnabled(False)
        self.login_button.setText("Verificando...")
        
        try:
            # Chamar CRUD diretamente - sem JavaScript!
            success, result = crud_system.users.verify_login(username, password)
            
            if success:
                # Login bem-sucedido
                self.login_successful.emit(result, username)
                
                # Limpar campos se não for para lembrar
                if not self.remember_checkbox.isChecked():
                    self.username_input.clear()
                    self.password_input.clear()
            else:
                # Login falhou
                QMessageBox.critical(self, "Erro de Login", result)
                self.password_input.clear()
                self.password_input.setFocus()
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao processar login: {str(e)}")
            
        finally:
            # Reabilitar botão
            self.login_button.setEnabled(True)
            self.login_button.setText("Entrar")