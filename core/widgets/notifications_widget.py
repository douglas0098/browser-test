from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QListWidget, QListWidgetItem,
                             QFrame, QCheckBox, QButtonGroup, QRadioButton)
from PyQt6.QtCore import Qt, pyqtSignal, QDateTime, QTimer
from PyQt6.QtGui import QFont, QIcon
from typing import List, Dict
from datetime import datetime

class NotificationItem(QFrame):
    """Item individual de notificação"""
    
    clicked = pyqtSignal(str)  # notification_id
    dismissed = pyqtSignal(str)  # notification_id
    
    def __init__(self, notification_data: dict):
        super().__init__()
        self.notification_id = notification_data.get('id', '')
        self.data = notification_data
        self.setup_ui()
        
    def setup_ui(self):
        """Cria UI do item de notificação"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }
            QFrame:hover {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Ícone
        icon_label = QLabel(self.data.get('icon', '🔔'))
        icon_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon_label)
        
        # Conteúdo
        content_layout = QVBoxLayout()
        
        # Título
        title_label = QLabel(self.data.get('title', 'Notificação'))
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        content_layout.addWidget(title_label)
        
        # Mensagem
        message_label = QLabel(self.data.get('message', ''))
        message_label.setWordWrap(True)
        message_label.setStyleSheet("color: #666;")
        content_layout.addWidget(message_label)
        
        # Timestamp
        timestamp = self.data.get('timestamp', datetime.now())
        time_label = QLabel(self.format_time(timestamp))
        time_label.setStyleSheet("color: #999; font-size: 12px;")
        content_layout.addWidget(time_label)
        
        layout.addLayout(content_layout)
        layout.addStretch()
        
        # Botão fechar
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
                font-size: 16px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #333;
            }
        """)
        close_btn.clicked.connect(lambda: self.dismissed.emit(self.notification_id))
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
        # Tornar clicável
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def format_time(self, timestamp):
        """Formata o timestamp para exibição"""
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"Há {diff.days} dia{'s' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"Há {hours} hora{'s' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"Há {minutes} minuto{'s' if minutes > 1 else ''}"
        else:
            return "Agora mesmo"
    
    def mousePressEvent(self, event):
        """Detecta clique no item"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.notification_id)


class NotificationsWidget(QWidget):
    """Widget principal de notificações"""
    
    notification_clicked = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.notifications = []
        self.setup_ui()
        self.load_notifications()
        
        # Timer para atualizar timestamps
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_timestamps)
        self.update_timer.start(60000)  # Atualiza a cada minuto
        
    def setup_ui(self):
        """Cria interface de notificações"""
        layout = QVBoxLayout()
        
        # Cabeçalho
        header_layout = QHBoxLayout()
        
        title = QLabel("Notificações")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Contador
        self.count_label = QLabel("0 notificações")
        self.count_label.setStyleSheet("color: #666;")
        header_layout.addWidget(self.count_label)
        
        # Botão marcar todas como lidas
        self.mark_all_btn = QPushButton("Marcar todas como lidas")
        self.mark_all_btn.clicked.connect(self.mark_all_read)
        header_layout.addWidget(self.mark_all_btn)
        
        layout.addLayout(header_layout)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("Mostrar:")
        filter_layout.addWidget(filter_label)
        
        self.filter_group = QButtonGroup()
        
        self.all_radio = QRadioButton("Todas")
        self.all_radio.setChecked(True)
        self.filter_group.addButton(self.all_radio, 0)
        filter_layout.addWidget(self.all_radio)
        
        self.unread_radio = QRadioButton("Não lidas")
        self.filter_group.addButton(self.unread_radio, 1)
        filter_layout.addWidget(self.unread_radio)
        
        self.important_radio = QRadioButton("Importantes")
        self.filter_group.addButton(self.important_radio, 2)
        filter_layout.addWidget(self.important_radio)
        
        self.filter_group.buttonClicked.connect(self.filter_changed)
        
        filter_layout.addStretch()
        
        # Configurações de notificação
        self.enable_notifications_check = QCheckBox("Ativar notificações")
        self.enable_notifications_check.setChecked(True)
        filter_layout.addWidget(self.enable_notifications_check)
        
        layout.addLayout(filter_layout)
        
        # Lista de notificações
        self.notifications_list = QVBoxLayout()
        self.notifications_list.setSpacing(5)
        
        # Container com scroll
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.notifications_list)
        
        from PyQt6.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8f9fa;
            }
        """)
        
        layout.addWidget(scroll_area)
        
        # Mensagem quando não há notificações
        self.empty_label = QLabel("Nenhuma notificação no momento")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: #999;
            font-size: 16px;
            padding: 40px;
        """)
        self.notifications_list.addWidget(self.empty_label)
        
        self.setLayout(layout)
        
        # Aplicar estilos
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QRadioButton {
                spacing: 8px;
                color: #333;
            }
            
            QCheckBox {
                spacing: 8px;
                color: #333;
            }
        """)
    
    def load_notifications(self):
        """Carrega notificações (simulado)"""
        # Notificações de exemplo
        sample_notifications = [
            {
                'id': '1',
                'icon': '🎉',
                'title': 'Bem-vindo ao UP Browser!',
                'message': 'Obrigado por usar nosso navegador. Explore todas as funcionalidades disponíveis.',
                'timestamp': datetime.now(),
                'read': False,
                'important': True
            },
            {
                'id': '2',
                'icon': '🔄',
                'title': 'Atualização disponível',
                'message': 'Uma nova versão do UP Browser está disponível. Clique para atualizar.',
                'timestamp': datetime.now(),
                'read': False,
                'important': True
            },
            {
                'id': '3',
                'icon': '🛡️',
                'title': 'Proteção ativada',
                'message': 'O bloqueio de rastreadores está ativo e protegendo sua privacidade.',
                'timestamp': datetime.now(),
                'read': True,
                'important': False
            }
        ]
        
        self.notifications = sample_notifications
        self.refresh_list()
    
    def refresh_list(self):
        """Atualiza a lista de notificações"""
        # Limpar lista atual
        while self.notifications_list.count():
            child = self.notifications_list.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Filtrar notificações
        filtered = self.get_filtered_notifications()
        
        # Atualizar contador
        unread_count = sum(1 for n in self.notifications if not n.get('read', False))
        total_count = len(self.notifications)
        self.count_label.setText(f"{unread_count} não lidas de {total_count}")
        
        # Adicionar notificações
        if filtered:
            for notification in filtered:
                item = NotificationItem(notification)
                item.clicked.connect(self.on_notification_clicked)
                item.dismissed.connect(self.dismiss_notification)
                self.notifications_list.addWidget(item)
        else:
            # Mostrar mensagem vazia
            self.empty_label = QLabel("Nenhuma notificação para mostrar")
            self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.empty_label.setStyleSheet("color: #999; font-size: 16px; padding: 40px;")
            self.notifications_list.addWidget(self.empty_label)
        
        # Adicionar espaçador no final
        self.notifications_list.addStretch()
    
    def get_filtered_notifications(self):
        """Retorna notificações filtradas"""
        filter_id = self.filter_group.checkedId()
        
        if filter_id == 0:  # Todas
            return self.notifications
        elif filter_id == 1:  # Não lidas
            return [n for n in self.notifications if not n.get('read', False)]
        elif filter_id == 2:  # Importantes
            return [n for n in self.notifications if n.get('important', False)]
        
        return self.notifications
    
    def filter_changed(self):
        """Chamado quando o filtro muda"""
        self.refresh_list()
    
    def on_notification_clicked(self, notification_id):
        """Processa clique em notificação"""
        # Marcar como lida
        for notification in self.notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                self.notification_clicked.emit(notification)
                break
        
        self.refresh_list()
    
    def dismiss_notification(self, notification_id):
        """Remove uma notificação"""
        self.notifications = [n for n in self.notifications if n['id'] != notification_id]
        self.refresh_list()
    
    def mark_all_read(self):
        """Marca todas as notificações como lidas"""
        for notification in self.notifications:
            notification['read'] = True
        self.refresh_list()
    
    def update_timestamps(self):
        """Atualiza os timestamps das notificações"""
        # Recriar os widgets para atualizar os tempos
        self.refresh_list()
    
    def add_notification(self, title, message, icon='🔔', important=False):
        """Adiciona uma nova notificação"""
        notification = {
            'id': str(len(self.notifications) + 1),
            'icon': icon,
            'title': title,
            'message': message,
            'timestamp': datetime.now(),
            'read': False,
            'important': important
        }
        
        self.notifications.insert(0, notification)
        self.refresh_list()
        
        # Mostrar notificação do sistema se habilitado
        if self.enable_notifications_check.isChecked():
            self.show_system_notification(title, message)
    
    def show_system_notification(self, title, message):
        """Mostra notificação do sistema"""
        try:
            # Aqui você poderia usar bibliotecas como plyer ou PyQt6's QSystemTrayIcon
            print(f"Notificação: {title} - {message}")
        except:
            pass