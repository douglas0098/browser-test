## Modified main.py

import os
import sys
from core.app import run_browser

if __name__ == "__main__":
    # ✅ CONFIGURAÇÕES OTIMIZADAS para sites modernos como ChatGPT
    
    # Configurações básicas do Chromium
    chromium_flags = [
        "--no-sandbox",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--enable-logging",
        "--log-level=0",
        
        # ✅ MELHOR SUPORTE para JavaScript e sites de IA
        "--enable-javascript",
        "--enable-plugins",
        "--enable-extensions",
        
        # ✅ MEMÓRIA e PERFORMANCE
        "--max_old_space_size=4096",
        "--memory-pressure-off",
        "--max-active-webgl-contexts=16",
        
        # ✅ SUPORTE para recursos modernos
        "--enable-webgl",
        "--enable-accelerated-2d-canvas",
        "--enable-accelerated-video-decode",
        
        # ✅ ESPECÍFICO para sites de chat/IA
        "--enable-media-stream",
        "--enable-speech-dispatcher",
        "--autoplay-policy=no-user-gesture-required"
    ]
    
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(chromium_flags)
    
    # ✅ CONFIGURAÇÕES DE RENDERIZAÇÃO mais compatíveis
    # Remover ou comentar as linhas muito restritivas:
    # os.environ["QT_QUICK_BACKEND"] = "software"  # ← PODE CAUSAR PROBLEMAS
    # os.environ["QT_OPENGL"] = "software"         # ← PODE CAUSAR PROBLEMAS
    
    # ✅ CONFIGURAÇÕES OTIMIZADAS
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1.0"
    
    run_browser()