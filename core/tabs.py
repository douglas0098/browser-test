# Lógica do DraggableTabWidget e DetachableTabBar

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QTabBar, QTabWidget


class DetachableTabBar(QTabBar):
    """Barra de abas especial que permite destacar as abas"""

    tabDetached = pyqtSignal(int, QPoint)

    def __init__(self, parent=None):
        super(DetachableTabBar, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setSelectionBehaviorOnRemove(QTabBar.SelectionBehavior.SelectPreviousTab)
        self.setMovable(True)
        self._drag_start_pos = None
        self._is_dragging = False
        self._tab_being_dragged = -1

    def mousePressEvent(self, event):
        """Captura o ponto inicial de um possível arrasto"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.position()
            self._tab_being_dragged = self.tabAt(event.position().toPoint())
        super(DetachableTabBar, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Detecta se o mouse está sendo arrastado e inicia a operação de destacar a aba"""
        # Se não estava arrastando ou não é o botão esquerdo, trata normalmente
        if not self._drag_start_pos or not (
            event.buttons() & Qt.MouseButton.LeftButton
        ):
            super(DetachableTabBar, self).mouseMoveEvent(event)
            return

        # Verifica se moveu o suficiente para considerar um arrasto
        if (
            not self._is_dragging
            and (event.position() - self._drag_start_pos).manhattanLength()
            < QApplication.startDragDistance()
        ):
            super(DetachableTabBar, self).mouseMoveEvent(event)
            return

        # Marca que estamos em processo de arrasto
        self._is_dragging = True

        # Se o mouse saiu da área da barra de abas, destacamos a aba
        tab_rect = self.tabRect(self._tab_being_dragged)
        if not tab_rect.contains(event.position().toPoint()):
            # Captura a posição global do mouse para posicionar a nova janela
            global_pos = event.globalPosition().toPoint()

            # Emite o sinal de que uma aba foi destacada
            self.tabDetached.emit(self._tab_being_dragged, global_pos)

            # Reseta o estado de arrasto
            self._drag_start_pos = None
            self._is_dragging = False
            self._tab_being_dragged = -1

            # Evita processamento adicional
            event.accept()
            return

        # Se chegou aqui, continua com o comportamento padrão (mover dentro da barra)
        super(DetachableTabBar, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Reseta o estado do arrasto quando o botão do mouse é solto"""
        self._drag_start_pos = None
        self._is_dragging = False
        self._tab_being_dragged = -1
        super(DetachableTabBar, self).mouseReleaseEvent(event)


class DraggableTabWidget(QTabWidget):
    """Widget de abas que permite destacar abas arrastando-as para fora"""

    tabDetached = pyqtSignal(int, QPoint, QWebEngineView)

    def __init__(self, parent=None):
        super(DraggableTabWidget, self).__init__(parent)

        # Substitui a barra de abas padrão por nossa versão destacável
        self.detachable_tab_bar = DetachableTabBar(self)
        self.setTabBar(self.detachable_tab_bar)

        # Conecta o sinal da barra de abas ao slot correspondente
        self.detachable_tab_bar.tabDetached.connect(self._handle_tab_detach)

        # Configura opções básicas do widget de abas
        self.setMovable(True)  # As abas podem ser reorganizadas
        self.setAcceptDrops(True)  # Aceita operações de arrastar e soltar

    def _handle_tab_detach(self, index, global_pos):
        """Gerencia o processo quando uma aba é destacada"""
        # Verifica se o índice da aba é válido
        if index < 0 or index >= self.count():
            return

        # Obtém o widget atual da aba antes de qualquer operação
        web_view = self.widget(index)
        if not web_view:
            return

        # Emite o sinal para a classe principal processar o destacamento
        self.tabDetached.emit(index, global_pos, web_view)

    def dragEnterEvent(self, event):
        """Aceita arrastar abas de volta para o widget"""
        event.accept()  # Aceita todos os eventos de arrasto por padrão

    def dropEvent(self, event):
        """Trata o soltar de uma aba arrastada"""
        event.accept()  # Aceita o evento de soltar
