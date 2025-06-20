from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
import random

class DashboardCard(QFrame):
    """Card de resumo do dashboard"""
    
    def __init__(self, title, value, icon, color, trend=None):
        super().__init__()
        self.setup_ui(title, value, icon, color, trend)
        
    def setup_ui(self, title, value, icon, color, trend):
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 16px;
                padding: 25px;
                border-left: 4px solid {color};
            }}
            QFrame:hover {{
                transform: translateY(-8px);
            }}
        """)
        
        layout = QHBoxLayout()
        
        # Ícone
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            background: {color}20;
            padding: 15px;
            border-radius: 50%;
        """)
        layout.addWidget(icon_label)
        
        # Conteúdo
        content_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 14px; font-weight: 600;")
        content_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        content_layout.addWidget(value_label)
        
        if trend:
            trend_label = QLabel(trend)
            color = "#27ae60" if "+" in trend else "#e74c3c"
            trend_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold;")
            content_layout.addWidget(trend_label)
        
        layout.addLayout(content_layout)
        layout.addStretch()
        
        self.setLayout(layout)


class DashboardWidget(QWidget):
    """Widget do Dashboard Financeiro"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()
        
        # Timer para atualização automática
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(5000)  # Atualiza a cada 5 segundos
        
    def setup_ui(self):
        """Cria interface do dashboard"""
        layout = QVBoxLayout()
        
        # Cabeçalho
        header = QLabel("Dashboard Financeiro")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
            margin-bottom: 20px;
        """)
        layout.addWidget(header)
        
        # Cards de resumo
        self.summary_layout = QGridLayout()
        self.summary_layout.setSpacing(20)
        
        # Criar cards
        self.revenue_card = DashboardCard(
            "RECEITA MENSAL",
            "R$ 0,00",
            "💰",
            "#27ae60",
            "+0%"
        )
        self.summary_layout.addWidget(self.revenue_card, 0, 0)
        
        self.expense_card = DashboardCard(
            "DESPESAS",
            "R$ 0,00",
            "💸",
            "#e74c3c",
            "-0%"
        )
        self.summary_layout.addWidget(self.expense_card, 0, 1)
        
        self.profit_card = DashboardCard(
            "LUCRO LÍQUIDO",
            "R$ 0,00",
            "📈",
            "#3498db",
            "+0%"
        )
        self.summary_layout.addWidget(self.profit_card, 0, 2)
        
        self.margin_card = DashboardCard(
            "MARGEM",
            "0%",
            "📊",
            "#9b59b6"
        )
        self.summary_layout.addWidget(self.margin_card, 0, 3)
        
        layout.addLayout(self.summary_layout)
        
        # Gráficos (placeholder por enquanto)
        charts_frame = QFrame()
        charts_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 25px;
                min-height: 300px;
            }
        """)
        
        charts_layout = QVBoxLayout(charts_frame)
        
        chart_title = QLabel("Evolução Mensal")
        chart_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #2c3e50;")
        charts_layout.addWidget(chart_title)
        
        # Simulação de gráfico com barras
        bars_layout = QHBoxLayout()
        months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        
        for month in months:
            month_layout = QVBoxLayout()
            
            # Barra
            bar = QProgressBar()
            bar.setOrientation(Qt.Orientation.Vertical)
            bar.setRange(0, 100)
            bar.setValue(random.randint(30, 90))
            bar.setTextVisible(False)
            bar.setFixedWidth(40)
            bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background-color: #ecf0f1;
                    border-radius: 4px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3498db, stop:1 #2980b9);
                    border-radius: 4px;
                }
            """)
            
            month_layout.addWidget(bar)
            
            # Label do mês
            label = QLabel(month)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            month_layout.addWidget(label)
            
            bars_layout.addLayout(month_layout)
        
        charts_layout.addLayout(bars_layout)
        charts_layout.addStretch()
        
        layout.addWidget(charts_frame)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def load_data(self):
        """Carrega dados do dashboard"""
        # Simulação - conectar ao banco depois
        self.update_card_value(self.revenue_card, "R$ 15.750,00", "+12.5%")
        self.update_card_value(self.expense_card, "R$ 8.320,00", "-5.2%")
        self.update_card_value(self.profit_card, "R$ 7.430,00", "+8.7%")
        self.update_card_value(self.margin_card, "47.2%", None)
    
    def update_card_value(self, card, value, trend=None):
        """Atualiza valores de um card"""
        # Encontrar labels no card
        labels = card.findChildren(QLabel)
        if len(labels) >= 3:
            labels[2].setText(value)  # Valor
            if trend and len(labels) >= 4:
                labels[3].setText(trend)  # Tendência
                color = "#27ae60" if "+" in trend else "#e74c3c"
                labels[3].setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold;")
    
    def update_data(self):
        """Atualiza dados (simulação)"""
        # Aqui você conectaria ao banco para pegar dados reais
        pass