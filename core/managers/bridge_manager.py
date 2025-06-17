import os

from PyQt6.QtCore import QTimer
from PyQt6.QtWebEngineCore import QWebEnginePage


def load_js_script(script_name: str) -> str:
    """Carrega um script JavaScript da pasta assets/js"""
    script_path = os.path.join(
        os.path.dirname(__file__), "../", "..", "assets", "js", "bridge", script_name
    )
    with open(script_path, "r", encoding="utf-8") as file:
        return file.read()


def inject_bridge_script(page: QWebEnginePage):
    """Injeta o script bridge_injector.js na página WebEngine"""
    try:
        js_code = load_js_script("bridge_injector.js")
        page.runJavaScript(js_code)

        # Log para depuração após 1 segundo
        QTimer.singleShot(
            1000,
            lambda: page.runJavaScript(
                "console.log('Verificação pós-injeção: pyQtApi?', typeof window.pyQtApi !== 'undefined', 'pyQtBridge?', typeof window.pyQtBridge !== 'undefined');"
            ),
        )

    except Exception as e:
        print(f"[ERRO] Falha ao injetar bridge_injector.js: {e}")
