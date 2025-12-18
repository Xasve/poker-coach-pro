"""
screen_capture module - Captura y análisis de pantalla para poker
"""

# Importar todos los componentes
from .stealth_capture import StealthScreenCapture
from .screen_reader import ScreenReader
from .image_processor import ImageProcessor
from .text_ocr import TextOCR
from .card_recognizer import CardRecognizer, Card
from .table_detector import TableDetector
from .adaptive_recognizer import AdaptiveCardRecognizer  # NUEVO

# Definir qué se exporta
__all__ = [
    'StealthScreenCapture',
    'ScreenReader',
    'ImageProcessor',
    'TextOCR',
    'CardRecognizer',
    'Card',
    'TableDetector',
    'AdaptiveCardRecognizer'  # NUEVO
]