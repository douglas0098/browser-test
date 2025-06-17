from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QProgressBar, QFrame, QGridLayout,
                             QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor
from typing import List, Dict
import json
import os

class RewardCard(QFrame):
    """Card individual de recompensa"""
    
    claimed = pyqtSignal(str)  # reward_id
    
    def __init__(self, reward_data: dict):
        super().__init__()
        self.reward_data = reward_data
        self.setup_ui()
        
    def setup_ui(self):
        """Cria UI do card de recompensa"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setFixedSize(250, 300)
        
        # Aplicar estilo baseado no status
        if self.reward_data.get('claimed', False):
            style = """
                QFrame {
                    background-color: #e8f5e9;
                    border: 2px solid #4caf50;
                    border-radius: 10px;
                    padding: 15px;
                }
            """
        elif self.reward_data.get('available', True):
            style = """
                QFrame {
                    background-color: white;
                    border: 2px solid #3498db;
                    border-radius: 10px;
                    padding: 15px;
                }
                QFrame:hover {
                    background-color: #f0f8ff;
                    border-color: #2196f3;
                }
            """
        else:
            style = """
                QFrame {
                    background-color: #f5f5f5;
                    border: 2px solid #ccc;
                    border-radius: 10px;
                    padding: 15px;
                }
            """
        
        self.setStyleSheet(style)
        
        layout = QVBoxLayout()
        
        # Ícone
        icon_label = QLabel(self.reward_data.get('icon', '🎁'))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel(self.reward_data.get('title', 'Recompensa'))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Descrição
        desc_label = QLabel(self.reward_data.get('description', ''))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # Pontos necessários
        points_label = QLabel(f"💎 {self.reward_data.get('points', 0)} pontos")
        points_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        points_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        layout.addWidget(points_label)
        
        # Botão de ação
        if self.reward_data.get('claimed', False):
            action_btn = QPushButton("✅ Resgatado")
            action_btn.setEnabled(False)
            action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4caf50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                }
            """)
        elif self.reward_data.get('available', True):
            action_btn = QPushButton("Resgatar")
            action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            action_btn.clicked.connect(
                lambda: self.claimed.emit(self.reward_data.get('id', ''))
            )
        else:
            action_btn = QPushButton("🔒 Bloqueado")
            action_btn.setEnabled(False)
            action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ccc;
                    color: #666;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                }
            """)
        
        layout.addWidget(action_btn)
        self.setLayout(layout)


class RewardsWidget(QWidget):
    """Widget principal de recompensas"""
    
    def __init__(self):
        super().__init__()
        self.user_points = 150  # Pontos iniciais de exemplo
        self.rewards = []
        self.achievements = []
        self.setup_ui()
        self.load_rewards_data()
        
    def setup_ui(self):
        """Cria interface de recompensas"""
        main_layout = QVBoxLayout()
        
        # Cabeçalho
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        header_layout = QVBoxLayout()
        
        # Título
        title = QLabel("Centro de Recompensas")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # Pontos do usuário
        points_container = QHBoxLayout()
        points_container.addStretch()
        
        points_icon = QLabel("💎")
        points_icon.setStyleSheet("font-size: 32px;")
        points_container.addWidget(points_icon)
        
        self.points_label = QLabel(str(self.user_points))
        self.points_label.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: bold;
            margin: 0 10px;
        """)
        points_container.addWidget(self.points_label)
        
        points_text = QLabel("pontos")
        points_text.setStyleSheet("color: white; font-size: 18px;")
        points_container.addWidget(points_text)
        
        points_container.addStretch()
        header_layout.addLayout(points_container)
        
        # Barra de progresso para próximo nível
        level_layout = QVBoxLayout()
        
        level_info = QHBoxLayout()
        current_level = QLabel("Nível 5")
        current_level.setStyleSheet("color: white; font-weight: bold;")
        level_info.addWidget(current_level)
        
        level_info.addStretch()
        
        next_level = QLabel("Nível 6")
        next_level.setStyleSheet("color: white; font-weight: bold;")
        level_info.addWidget(next_level)
        
        level_layout.addLayout(level_info)
        
        self.level_progress = QProgressBar()
        self.level_progress.setRange(0, 200)
        self.level_progress.setValue(150)
        self.level_progress.setTextVisible(True)
        self.level_progress.setFormat("150/200 XP")
        self.level_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid white;
                border-radius: 5px;
                text-align: center;
                color: white;
                background-color: rgba(255, 255, 255, 0.2);
            }
            QProgressBar::chunk {
                background-color: white;
                border-radius: 3px;
            }
        """)
        level_layout.addWidget(self.level_progress)
        
        header_layout.addLayout(level_layout)
        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)
        
        # Tabs para diferentes seções
        from PyQt6.QtWidgets import QTabWidget
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #3498db;
            }
        """)
        
        # Aba de Recompensas
        rewards_tab = self.create_rewards_tab()
        self.tabs.addTab(rewards_tab, "🎁 Recompensas")
        
        # Aba de Conquistas
        achievements_tab = self.create_achievements_tab()
        self.tabs.addTab(achievements_tab, "🏆 Conquistas")
        
        # Aba de Missões
        missions_tab = self.create_missions_tab()
        self.tabs.addTab(missions_tab, "🎯 Missões")
        
        # Aba de Histórico
        history_tab = self.create_history_tab()
        self.tabs.addTab(history_tab, "📜 Histórico")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
    
    def create_rewards_tab(self):
        """Cria aba de recompensas disponíveis"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filtros
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filtrar por:")
        filter_layout.addWidget(filter_label)
        
        from PyQt6.QtWidgets import QComboBox
        filter_combo = QComboBox()
        filter_combo.addItems(["Todas", "Disponíveis", "Resgatadas", "Bloqueadas"])
        filter_layout.addWidget(filter_combo)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Grid de recompensas
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.rewards_grid = QGridLayout()
        self.rewards_grid.setSpacing(20)
        
        scroll_widget.setLayout(self.rewards_grid)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8f9fa;
            }
        """)
        
        layout.addWidget(scroll_area)
        widget.setLayout(layout)
        return widget
    
    def create_achievements_tab(self):
        """Cria aba de conquistas"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Lista de conquistas
        achievements_layout = QVBoxLayout()
        
        # Conquistas de exemplo
        achievements = [
            {
                'icon': '🌟',
                'title': 'Primeiro Acesso',
                'description': 'Fazer login pela primeira vez',
                'points': 10,
                'completed': True
            },
            {
                'icon': '🔍',
                'title': 'Explorador',
                'description': 'Visitar 100 sites diferentes',
                'points': 50,
                'completed': True,
                'progress': 100,
                'total': 100
            },
            {
                'icon': '🛡️',
                'title': 'Guardião da Privacidade',
                'description': 'Ativar todas as proteções de privacidade',
                'points': 30,
                'completed': False,
                'progress': 2,
                'total': 3
            },
            {
                'icon': '📚',
                'title': 'Leitor Ávido',
                'description': 'Passar 10 horas navegando',
                'points': 100,
                'completed': False,
                'progress': 7,
                'total': 10
            }
        ]
        
        for achievement in achievements:
            item_frame = QFrame()
            item_frame.setFrameStyle(QFrame.Shape.Box)
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 5px;
                }
            """)
            
            item_layout = QHBoxLayout()
            
            # Ícone
            icon_label = QLabel(achievement['icon'])
            icon_label.setStyleSheet("font-size: 36px;")
            item_layout.addWidget(icon_label)
            
            # Informações
            info_layout = QVBoxLayout()
            
            title_layout = QHBoxLayout()
            title_label = QLabel(achievement['title'])
            title_font = QFont()
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_layout.addWidget(title_label)
            
            if achievement['completed']:
                check_label = QLabel("✅")
                title_layout.addWidget(check_label)
            
            title_layout.addStretch()
            info_layout.addLayout(title_layout)
            
            desc_label = QLabel(achievement['description'])
            desc_label.setStyleSheet("color: #666;")
            info_layout.addWidget(desc_label)
            
            # Progresso
            if 'progress' in achievement and not achievement['completed']:
                progress_bar = QProgressBar()
                progress_bar.setRange(0, achievement['total'])
                progress_bar.setValue(achievement['progress'])
                progress_bar.setFormat(f"{achievement['progress']}/{achievement['total']}")
                progress_bar.setMaximumHeight(15)
                info_layout.addWidget(progress_bar)
            
            item_layout.addLayout(info_layout)
            item_layout.addStretch()
            
            # Pontos
            points_label = QLabel(f"+{achievement['points']} pts")
            points_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #3498db;
            """)
            item_layout.addWidget(points_label)
            
            item_frame.setLayout(item_layout)
            achievements_layout.addWidget(item_frame)
        
        achievements_layout.addStretch()
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(achievements_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)
        widget.setLayout(layout)
        return widget
    
    def create_missions_tab(self):
        """Cria aba de missões diárias/semanais"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Missões Diárias
        daily_label = QLabel("Missões Diárias")
        daily_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")
        layout.addWidget(daily_label)
        
        daily_missions = [
            {
                'title': 'Navegue por 30 minutos',
                'reward': 10,
                'progress': 15,
                'total': 30
            },
            {
                'title': 'Visite 5 sites diferentes',
                'reward': 15,
                'progress': 3,
                'total': 5
            },
            {
                'title': 'Use a busca 3 vezes',
                'reward': 5,
                'progress': 3,
                'total': 3,
                'completed': True
            }
        ]
        
        for mission in daily_missions:
            mission_frame = self.create_mission_item(mission)
            layout.addWidget(mission_frame)
        
        # Espaçador
        layout.addSpacing(20)
        
        # Missões Semanais
        weekly_label = QLabel("Missões Semanais")
        weekly_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #9b59b6;")
        layout.addWidget(weekly_label)
        
        weekly_missions = [
            {
                'title': 'Complete todas as missões diárias 5 dias',
                'reward': 50,
                'progress': 3,
                'total': 5
            },
            {
                'title': 'Navegue por 5 horas no total',
                'reward': 100,
                'progress': 2.5,
                'total': 5
            }
        ]
        
        for mission in weekly_missions:
            mission_frame = self.create_mission_item(mission)
            layout.addWidget(mission_frame)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_mission_item(self, mission_data):
        """Cria item de missão"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Informações da missão
        info_layout = QVBoxLayout()
        
        title_label = QLabel(mission_data['title'])
        if mission_data.get('completed', False):
            title_label.setStyleSheet("text-decoration: line-through; color: #999;")
        info_layout.addWidget(title_label)
        
        # Barra de progresso
        progress_bar = QProgressBar()
        progress_bar.setRange(0, int(mission_data['total']))
        progress_bar.setValue(int(mission_data['progress']))
        progress_bar.setMaximumHeight(10)
        
        if mission_data.get('completed', False):
            progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #4caf50;
                }
            """)
        
        info_layout.addWidget(progress_bar)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Recompensa
        reward_label = QLabel(f"🎁 {mission_data['reward']} pts")
        reward_label.setStyleSheet("font-weight: bold; color: #f39c12;")
        layout.addWidget(reward_label)
        
        # Status
        if mission_data.get('completed', False):
            status_label = QLabel("✅")
            layout.addWidget(status_label)
        
        frame.setLayout(layout)
        return frame
    
    def create_history_tab(self):
        """Cria aba de histórico de resgates"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Histórico
        history_layout = QVBoxLayout()
        
        history_items = [
            {
                'date': '17/06/2025',
                'title': 'Tema Premium - Dark Pro',
                'points': -100,
                'type': 'resgate'
            },
            {
                'date': '16/06/2025',
                'title': 'Missão diária completada',
                'points': 10,
                'type': 'ganho'
            },
            {
                'date': '15/06/2025',
                'title': 'Conquista desbloqueada: Explorador',
                'points': 50,
                'type': 'ganho'
            }
        ]
        
        for item in history_items:
            item_frame = QFrame()
            item_frame.setFrameStyle(QFrame.Shape.Box)
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
            
            item_layout = QHBoxLayout()
            
            # Data
            date_label = QLabel(item['date'])
            date_label.setStyleSheet("color: #666; font-size: 12px;")
            item_layout.addWidget(date_label)
            
            # Título
            title_label = QLabel(item['title'])
            item_layout.addWidget(title_label)
            
            item_layout.addStretch()
            
            # Pontos
            points_label = QLabel(f"{'+' if item['points'] > 0 else ''}{item['points']} pts")
            if item['type'] == 'ganho':
                points_label.setStyleSheet("color: #27ae60; font-weight: bold;")
            else:
                points_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            item_layout.addWidget(points_label)
            
            item_frame.setLayout(item_layout)
            history_layout.addWidget(item_frame)
        
        history_layout.addStretch()
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(history_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)
        widget.setLayout(layout)
        return widget
    
    def load_rewards_data(self):
        """Carrega dados de recompensas"""
        # Recompensas de exemplo
        self.rewards = [
            {
                'id': '1',
                'icon': '🎨',
                'title': 'Tema Premium',
                'description': 'Desbloqueie temas exclusivos',
                'points': 100,
                'available': True,
                'claimed': False
            },
            {
                'id': '2',
                'icon': '🚀',
                'title': 'Turbo Mode',
                'description': 'Navegação 2x mais rápida',
                'points': 200,
                'available': False,
                'claimed': False
            },
            {
                'id': '3',
                'icon': '🛡️',
                'title': 'VPN Grátis (1 mês)',
                'description': 'Proteção extra na navegação',
                'points': 300,
                'available': False,
                'claimed': False
            },
            {
                'id': '4',
                'icon': '💎',
                'title': 'Badge Exclusiva',
                'description': 'Mostre seu nível',
                'points': 50,
                'available': True,
                'claimed': True
            }
        ]
        
        # Adicionar cards ao grid
        row = 0
        col = 0
        for reward in self.rewards:
            card = RewardCard(reward)
            card.claimed.connect(self.claim_reward)
            self.rewards_grid.addWidget(card, row, col)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def claim_reward(self, reward_id):
        """Processa o resgate de uma recompensa"""
        # Encontrar a recompensa
        reward = None
        for r in self.rewards:
            if r['id'] == reward_id:
                reward = r
                break
        
        if not reward:
            return
        
        # Verificar se tem pontos suficientes
        if self.user_points < reward['points']:
            QMessageBox.warning(
                self,
                "Pontos Insuficientes",
                f"Você precisa de {reward['points']} pontos para esta recompensa.\n"
                f"Você tem apenas {self.user_points} pontos."
            )
            return
        
        # Confirmar resgate
        reply = QMessageBox.question(
            self,
            "Confirmar Resgate",
            f"Deseja resgatar '{reward['title']}' por {reward['points']} pontos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Deduzir pontos
            self.user_points -= reward['points']
            self.points_label.setText