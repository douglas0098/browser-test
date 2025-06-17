# core/managers/page_manager.py
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineUrlSchemeHandler
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestJob

class CustomUrlHandler(QWebEngineUrlSchemeHandler):
    """Handler customizado para URLs especiais"""
    
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
    
    def requestStarted(self, request: QWebEngineUrlRequestJob):
        """Intercepta requisições especiais"""
        url = request.requestUrl().toString()
        
        # Exemplo: upbrowser://action/logout
        if url.startswith("upbrowser://"):
            parts = url.split("/")
            if len(parts) >= 3:
                action = parts[2]
                
                if action == "logout":
                    self.browser_window.handle_logout()
                elif action == "settings":
                    self.browser_window.open_settings()
                    
            # Responder com sucesso
            request.reply(b"text/plain", b"OK")