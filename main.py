## Modified main.py

import os
import sys
from core.app import run_browser

if __name__ == "__main__":
    # Enable software rendering as a fallback when GPU is not available
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox"
    
    # Add this environment variable to force software rendering
    os.environ["QT_QUICK_BACKEND"] = "software"
    
    # Add this environment variable to disable GPU acceleration
    os.environ["QT_OPENGL"] = "software"
    
    run_browser()
