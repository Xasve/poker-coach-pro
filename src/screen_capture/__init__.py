"""
Módulo de captura de pantalla con técnicas stealth
Sistema completo para análisis de mesas de poker
"""

from .stealth_capture import StealthScreenCapture, AdaptiveRegionCapture
from .screen_reader import ScreenReader
from .card_recognizer import CardRecognizer
from .table_detector import TableDetector
from .text_ocr import TextOCR
from .image_processor import ImageProcessor

__all__ = [
    'StealthScreenCapture',
    'AdaptiveRegionCapture', 
    'ScreenReader',
    'CardRecognizer',
    'TableDetector',
    'TextOCR',
    'ImageProcessor'
]

__version__ = '2.0.0'
__author__ = 'Poker Coach Pro Team'
__description__ = 'Sistema profesional de captura y análisis para poker'