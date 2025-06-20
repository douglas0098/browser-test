from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QScrollArea, QFrame,
                             QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor

class AIToolCard(QFrame):
    """Card individual de ferramenta de IA"""
    
    clicked = pyqtSignal(str)  # url
    favorite_toggled = pyqtSignal(str, bool)  # tool_id, is_favorite
    
    def __init__(self, tool_data):
        super().__init__()
        self.tool_data = tool_data
        self.setup_ui()
        
    def setup_ui(self):
        """Cria o card com o estilo do painel.css"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Aplicar estilos do card original
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 20px;
                border: 2px solid transparent;
            }
            QFrame:hover {
                transform: translateY(-5px);
                border-color: #3498db;
                background-color: #f0f8ff;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Header do card
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #4682B4;
                border-radius: 8px 8px 0 0;
                padding: 15px;
                margin: -20px -20px 15px -20px;
            }
        """)
        
        header_layout = QVBoxLayout(header)
        
        # Título
        title = QLabel(self.tool_data.get('name', 'Ferramenta IA'))
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title)
        
        layout.addWidget(header)
        
        # Tags
        tags_layout = QHBoxLayout()
        tags = self.tool_data.get('tags', [])
        tag_colors = ['#3b82f6', '#ef4444', '#f59e0b', '#10b981', '#8b5cf6']
        
        for i, tag in enumerate(tags[:3]):  # Máximo 3 tags
            tag_label = QLabel(tag)
            tag_label.setStyleSheet(f"""
                background-color: {tag_colors[i % len(tag_colors)]};
                color: white;
                padding: 6px 12px;
                border-radius: 50px;
                font-size: 12px;
                font-weight: 600;
            """)
            tags_layout.addWidget(tag_label)
        
        tags_layout.addStretch()
        layout.addLayout(tags_layout)
        
        # URL
        url_label = QLabel(self.tool_data.get('url', '').replace('https://', ''))
        url_label.setStyleSheet("color: #666; font-size: 14px; margin: 10px 0;")
        layout.addWidget(url_label)
        
        # Checkbox favorito
        favorite_layout = QHBoxLayout()
        self.favorite_checkbox = QPushButton("⭐ Adicionar aos Favoritos")
        self.favorite_checkbox.setCheckable(True)
        self.favorite_checkbox.setChecked(self.tool_data.get('is_favorite', False))
        self.update_favorite_button()
        
        self.favorite_checkbox.clicked.connect(self.toggle_favorite)
        favorite_layout.addWidget(self.favorite_checkbox)
        favorite_layout.addStretch()
        
        layout.addLayout(favorite_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def update_favorite_button(self):
        """Atualiza visual do botão de favorito"""
        if self.favorite_checkbox.isChecked():
            self.favorite_checkbox.setText("⭐ Remover dos Favoritos")
            self.favorite_checkbox.setStyleSheet("""
                QPushButton {
                    background-color: #fbbf24;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-weight: bold;
                }
            """)
        else:
            self.favorite_checkbox.setText("⭐ Adicionar aos Favoritos")
            self.favorite_checkbox.setStyleSheet("""
                QPushButton {
                    background-color: #e5e7eb;
                    color: #374151;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d1d5db;
                }
            """)
    
    def toggle_favorite(self):
        """Alterna status de favorito"""
        self.update_favorite_button()
        self.favorite_toggled.emit(
            self.tool_data.get('id', ''),
            self.favorite_checkbox.isChecked()
        )
    
    def mousePressEvent(self, event):
        """Detecta clique no card"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Verifica se não clicou no checkbox
            checkbox_rect = self.favorite_checkbox.geometry()
            if not checkbox_rect.contains(event.position().toPoint()):
                self.clicked.emit(self.tool_data.get('url', ''))


class PanelWidget(QWidget):
    """Widget do painel principal - substitui painel.html"""
    
    open_url = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_category = "todas"
        self.ai_tools = []
        self.setup_ui()
        self.load_ai_tools()
        
    def setup_ui(self):
        """Cria a interface do painel"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Conteúdo principal
        content = self.create_content()
        main_layout.addWidget(content, 1)
        
        self.setLayout(main_layout)
        
        # Aplicar estilo de fundo
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
            }
        """)
    
    def create_sidebar(self):
        """Cria a sidebar do menu"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #4682B4;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("UP Browser")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        """)
        layout.addWidget(header)
        
        # Menu de categorias
        categories = [
            ("todas", "🏠 Todas as IAs"),
            ("conversacao", "💬 Conversação"),
            ("imagem", "🎨 Geração de Imagem"),
            ("codigo", "💻 Programação"),
            ("escrita", "✍️ Escrita"),
            ("analise", "📊 Análise de Dados"),
            ("favoritos", "⭐ Favoritos")
        ]
        
        for cat_id, cat_name in categories:
            btn = QPushButton(cat_name)
            btn.setCheckable(True)
            btn.setChecked(cat_id == "todas")
            btn.clicked.connect(lambda checked, cid=cat_id: self.change_category(cid))
            
            btn.setStyleSheet("""
                QPushButton {
                    background: none;
                    border: none;
                    color: white;
                    text-align: left;
                    padding: 12px 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #3878a8;
                }
                QPushButton:checked {
                    background-color: #3878a8;
                    border-left: 4px solid white;
                }
            """)
            
            layout.addWidget(btn)
            setattr(self, f"btn_{cat_id}", btn)  # Guardar referência
        
        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar
    
    def create_content(self):
        """Cria área de conteúdo principal"""
        content = QWidget()
        layout = QVBoxLayout()
        
        # Título da seção
        self.section_title = QLabel("Todas as IAs")
        self.section_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            padding-bottom: 10px;
            border-bottom: 2px solid #4682B4;
            margin-bottom: 25px;
        """)
        layout.addWidget(self.section_title)
        
        # Área de pesquisa
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar ferramentas de IA...")
        self.search_input.textChanged.connect(self.filter_tools)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 1px solid #ddd;
                border-radius: 25px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Grid de cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(25)
        self.cards_container.setLayout(self.cards_layout)
        
        scroll_area.setWidget(self.cards_container)
        layout.addWidget(scroll_area)
        
        content.setLayout(layout)
        return content
    
    def load_ai_tools(self):
        """Carrega ferramentas de IA (simulado por enquanto)"""
        # Dados de exemplo - depois conectar ao CRUD
        self.ai_tools = [
            {
                'id': '1',
                'name': 'ChatGPT',
                'url': 'https://chat.openai.com',
                'category': 'conversacao',
                'tags': ['Conversação', 'IA', 'OpenAI'],
                'is_favorite': False
            },
            {
                'id': '2',
                'name': 'DALL-E',
                'url': 'https://labs.openai.com',
                'category': 'imagem',
                'tags': ['Imagem', 'Arte', 'IA'],
                'is_favorite': True
            },
            {
                'id': '3',
                'name': 'GitHub Copilot',
                'url': 'https://github.com/features/copilot',
                'category': 'codigo',
                'tags': ['Código', 'Programação', 'GitHub'],
                'is_favorite': False
            },
            # Adicione mais ferramentas aqui
        ]
        
        self.display_tools()
    
    def display_tools(self, tools=None):
        """Exibe as ferramentas na grid"""
        # Limpar grid atual
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Filtrar ferramentas
        if tools is None:
            if self.current_category == "todas":
                tools = self.ai_tools
            elif self.current_category == "favoritos":
                tools = [t for t in self.ai_tools if t.get('is_favorite', False)]
            else:
                tools = [t for t in self.ai_tools if t.get('category') == self.current_category]
        
        # Adicionar cards
        row = 0
        col = 0
        for tool in tools:
            card = AIToolCard(tool)
            card.clicked.connect(self.open_url.emit)
            card.favorite_toggled.connect(self.toggle_favorite)
            
            self.cards_layout.addWidget(card, row, col)
            
            col += 1
            if col > 2:  # 3 colunas
                col = 0
                row += 1
    
    def change_category(self, category):
        """Muda a categoria exibida"""
        self.current_category = category
        
        # Atualizar botões
        for cat in ["todas", "conversacao", "imagem", "codigo", "escrita", "analise", "favoritos"]:
            btn = getattr(self, f"btn_{cat}", None)
            if btn:
                btn.setChecked(cat == category)
        
        # Atualizar título
        titles = {
            "todas": "Todas as IAs",
            "conversacao": "IAs de Conversação",
            "imagem": "IAs de Geração de Imagem",
            "codigo": "IAs de Programação",
            "escrita": "IAs de Escrita",
            "analise": "IAs de Análise de Dados",
            "favoritos": "Minhas Ferramentas Favoritas"
        }
        self.section_title.setText(titles.get(category, "Ferramentas de IA"))
        
        # Recarregar ferramentas
        self.display_tools()
    
    def filter_tools(self, text):
        """Filtra ferramentas pela pesquisa"""
        if not text:
            self.display_tools()
            return
        
        filtered = []
        for tool in self.ai_tools:
            if (text.lower() in tool['name'].lower() or 
                text.lower() in tool.get('url', '').lower() or
                any(text.lower() in tag.lower() for tag in tool.get('tags', []))):
                filtered.append(tool)
        
        self.display_tools(filtered)
    
    def toggle_favorite(self, tool_id, is_favorite):
        """Alterna status de favorito de uma ferramenta"""
        for tool in self.ai_tools:
            if tool['id'] == tool_id:
                tool['is_favorite'] = is_favorite
                break
        
        # Se estiver na categoria favoritos, recarregar
        if self.current_category == "favoritos":
            self.display_tools()