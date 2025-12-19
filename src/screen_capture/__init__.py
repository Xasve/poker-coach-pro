"""
Screen Capture Module for Poker Coach Pro
"""
from .stealth_capture import StealthScreenCapture
from .table_detector import TableDetector
from .card_recognizer import CardRecognizer
from .text_ocr import TextOCR

__all__ = [
    'StealthScreenCapture',
    'TableDetector',
    'CardRecognizer',
    'TextOCR'
]

__version__ = "2.0.0"

print("✅ screen_capture module loaded")
