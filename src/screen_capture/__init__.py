"""
Módulo de captura de pantalla para Poker Coach Pro
Sistema stealth de detección de mesa, cartas y texto.
"""

__all__ = [
    'StealthScreenCapture',
    'CardRecognizer', 
    'TableDetector',
    'TextOCR'
]

# Importaciones diferidas para evitar errores circulares
def import_stealth_capture():
    from .stealth_capture import StealthScreenCapture
    return StealthScreenCapture

def import_card_recognizer():
    from .card_recognizer import CardRecognizer
    return CardRecognizer

def import_table_detector():
    from .table_detector import TableDetector
    return TableDetector

def import_text_ocr():
    from .text_ocr import TextOCR
    return TextOCR

# Metadatos
__version__ = "2.0.0"
__author__ = "Poker Coach Pro Team"
