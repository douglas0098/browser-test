# Inicia o app (substitui o 'browser.py')

import sys

from PyQt6.QtWidgets import QApplication

from core.browser_window import ChromeClone


def run_browser():
    app = QApplication(sys.argv)
    window = ChromeClone()
    window.show()
    sys.exit(app.exec())
