from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from crud.database_adapter import crud_system

class RegisterWidget(QWidget):
    """Widget nativo PyQt6 para registro - sem JavaScript!"""
    
    # Sinais pythônicos
    register_successful = pyqtSignal(str, str)  # username, name
    switch_to_login = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Cria a interface de registro"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Título
        title = QLabel("Criar Conta")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Formulário
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Nome completo
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite seu nome completo")
        form_layout.addRow("Nome completo:", self.name_input)
        
        # Nome de usuário
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Escolha um nome de usuário")
        form_layout.addRow("Usuário:", self.username_input)
        
        # E-mail
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("seu@email.com")
        form_layout.addRow("E-mail:", self.email_input)
        
        # Telefone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("(11) 99999-9999")
        form_layout.addRow("Telefone:", self.phone_input)
        
        # CPF (opcional)
        self.cpf_input = QLineEdit()
        self.cpf_input.setPlaceholderText("000.000.000-00 (opcional)")
        form_layout.addRow("CPF:", self.cpf_input)
        
        # Senha
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Mínimo 6 caracteres")
        form_layout.addRow("Senha:", self.password_input)
        
        # Confirmar senha
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Digite a senha novamente")
        form_layout.addRow("Confirmar senha:", self.confirm_password_input)
        
        main_layout.addLayout(form_layout)
        
        # Botão de registro
        self.register_button = QPushButton("Criar Conta")
        self.register_button.setMinimumHeight(45)
        self.register_button.clicked.connect(self.handle_register)
        main_layout.addWidget(self.register_button)
        
        # Link para login
        login_layout = QHBoxLayout()
        login_layout.addStretch()
        
        login_label = QLabel("Já tem uma conta?")
        login_layout.addWidget(login_label)
        
        self.login_button = QPushButton("Faça login")
        self.login_button.setFlat(True)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.switch_to_login.emit)
        login_layout.addWidget(self.login_button)
        
        login_layout.addStretch()
        main_layout.addLayout(login_layout)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        # Adicionar máscaras aos campos
        self.setup_input_masks()
    
    def setup_input_masks(self):
        """Configura máscaras de entrada"""
        # Conectar formatação de telefone
        self.phone_input.textChanged.connect(self.format_phone)
        
        # Conectar formatação de CPF
        self.cpf_input.textChanged.connect(self.format_cpf)
    
    def format_phone(self, text):
        """Formata número de telefone"""
        # Remove tudo exceto números
        numbers = ''.join(filter(str.isdigit, text))
        
        # Aplica formatação
        if len(numbers) <= 2:
            formatted = f"({numbers}"
        elif len(numbers) <= 7:
            formatted = f"({numbers[:2]}) {numbers[2:]}"
        elif len(numbers) <= 11:
            formatted = f"({numbers[:2]}) {numbers[2:7]}-{numbers[7:]}"
        else:
            return  # Não altera se já tem 11 dígitos
        
        # Evita recursão infinita
        if formatted != text:
            cursor_pos = self.phone_input.cursorPosition()
            self.phone_input.setText(formatted)
            self.phone_input.setCursorPosition(cursor_pos + (len(formatted) - len(text)))
    
    def format_cpf(self, text):
        """Formata CPF"""
        # Remove tudo exceto números
        numbers = ''.join(filter(str.isdigit, text))
        
        # Aplica formatação
        if len(numbers) <= 3:
            formatted = numbers
        elif len(numbers) <= 6:
            formatted = f"{numbers[:3]}.{numbers[3:]}"
        elif len(numbers) <= 9:
            formatted = f"{numbers[:3]}.{numbers[3:6]}.{numbers[6:]}"
        elif len(numbers) <= 11:
            formatted = f"{numbers[:3]}.{numbers[3:6]}.{numbers[6:9]}-{numbers[9:]}"
        else:
            return  # Não altera se já tem 11 dígitos
        
        # Evita recursão infinita
        if formatted != text:
            cursor_pos = self.cpf_input.cursorPosition()
            self.cpf_input.setText(formatted)
            self.cpf_input.setCursorPosition(cursor_pos + (len(formatted) - len(text)))
    
    def apply_styles(self):
        """Aplica estilos ao widget"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
                min-height: 25px;
                color: black;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
                color: black;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton[flat="true"] {
                background-color: transparent;
                color: #3498db;
                font-weight: normal;
                text-decoration: underline;
            }
        """)
    
    def handle_register(self):
        """Processa o registro - TUDO EM PYTHON!"""
        # Coletar dados
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        cpf = self.cpf_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validações
        if not all([name, username, email, phone, password]):
            QMessageBox.warning(self, "Aviso", "Por favor, preencha todos os campos obrigatórios")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Aviso", "As senhas não coincidem")
            self.confirm_password_input.clear()
            self.confirm_password_input.setFocus()
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Aviso", "A senha deve ter pelo menos 6 caracteres")
            return
        
        # Desabilitar botão
        self.register_button.setEnabled(False)
        self.register_button.setText("Criando conta...")
        
        try:
            # Chamar CRUD diretamente
            success, result = crud_system.users.register_user(
                username=username,
                password=password,
                email=email,
                name=name,
                phone=phone,
                cpf=cpf if cpf else None
            )
            
            if success:
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    f"Conta criada com sucesso!\nBem-vindo(a), {name}!"
                )
                self.register_successful.emit(username, name)
                self.switch_to_login.emit()
            else:
                QMessageBox.critical(self, "Erro", result)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar conta: {str(e)}")
            
        finally:
            self.register_button.setEnabled(True)
            self.register_button.setText("Criar Conta")