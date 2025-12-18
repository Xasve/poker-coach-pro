"""
Módulo de captura de pantalla para Poker Coach Pro
"""
from .stealth_capture import StealthScreenCapture
from .card_recognizer import CardRecognizer
from .table_detector import TableDetector
from .text_ocr import TextOCR

__all__ = ['StealthScreenCapture', 'CardRecognizer', 'TableDetector', 'TextOCR']
