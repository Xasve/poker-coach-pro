# src/screen_capture/__init__.py
"""
Módulo de captura de pantalla y reconocimiento para Poker Coach Pro.
"""

# Exportar las clases que SÍ existen
from .stealth_capture import StealthScreenCapture
from .card_recognizer import CardRecognizer
from .table_detector import TableDetector
from .text_ocr import TextOCR
from .template_manager import CardTemplateManager

# 🔥 NO exportar 'Card' - esa clase no existe en nuestros archivos
# Esto causaría el error "cannot import name 'Card'"

__all__ = [
    'StealthScreenCapture',
    'CardRecognizer', 
    'TableDetector',
    'TextOCR',
    'CardTemplateManager'
]