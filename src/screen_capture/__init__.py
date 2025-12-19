"""
Módulo de captura de pantalla para Poker Coach Pro
Sistema stealth de detección de mesa, cartas y texto.
"""

# Importaciones relativas explícitas
try:
    from .stealth_capture import StealthScreenCapture
    from .card_recognizer import CardRecognizer
    from .table_detector import TableDetector
    from .text_ocr import TextOCR
    
    __all__ = [
        'StealthScreenCapture',
        'CardRecognizer', 
        'TableDetector',
        'TextOCR'
    ]
    
except ImportError as e:
    print(f"Advertencia: Error importando screen_capture: {e}")
    
# Metadatos
__version__ = "2.0.0"
__author__ = "Poker Coach Pro Team"
