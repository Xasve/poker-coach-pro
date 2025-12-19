# pokerstars_adapter.py - VERSIÓN CORREGIDA

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen_capture.stealth_capture import StealthScreenCapture
from screen_capture.table_detector import TableDetector
from screen_capture.card_recognizer import CardRecognizer
from screen_capture.text_ocr import TextOCR

class PokerStarsAdapter:
    def __init__(self, stealth_level="MEDIUM"):
        self.platform = "pokerstars"  # ← DEFINIR ANTES DE USARLO
        self.stealth_level = stealth_level
        
        print(f"🔄 Inicializando PokerStarsAdapter con nivel stealth: {stealth_level}")
        
        # CONSTRUCTORES CORRECTOS:
        self.capture_system = StealthScreenCapture(self.platform, self.stealth_level)  # ✓ 2 args
        self.table_detector = TableDetector()  # ✓ 0 args  
        self.card_recognizer = CardRecognizer(platform=self.platform)  # ✓ 1 arg (platform)
        self.text_ocr = TextOCR()  # ✓ 0 args
        
        print("✅ PokerStarsAdapter inicializado correctamente")
    
    def start(self):
        """Iniciar el sistema de captura"""
        print("🎴 Iniciando captura de PokerStars...")
        return self.capture_system.start_capture()
    
    def stop(self):
        """Detener el sistema de captura"""
        print("⏹️ Deteniendo captura...")
        return self.capture_system.stop_capture()
    
    def detect_table(self, screenshot=None):
        """Detectar mesa en la captura"""
        if screenshot is None:
            screenshot = self.capture_system.get_last_capture()
        return self.table_detector.detect(screenshot)
    
    def recognize_cards(self, table_region):
        """Reconocer cartas en la región de la mesa"""
        screenshot = self.capture_system.get_last_capture()
        return self.card_recognizer.recognize(screenshot, table_region)
    
    def extract_text(self, region):
        """Extraer texto de una región específica"""
        screenshot = self.capture_system.get_last_capture()
        return self.text_ocr.extract_text(screenshot, region)
    
    def analyze_table_state(self):
        """Analizar el estado completo de la mesa"""
        # 1. Capturar pantalla
        screenshot = self.capture_system.get_last_capture()
        if screenshot is None:
            return None
        
        # 2. Detectar mesa
        table_info = self.detect_table(screenshot)
        if not table_info:
            return None
        
        # 3. Reconocer cartas
        cards_info = self.recognize_cards(table_info["region"])
        
        # 4. Extraer textos (pozo, apuestas, etc.)
        pot_region = (table_info["region"][0] + 100, table_info["region"][1] + 50, 200, 40)
        pot_text = self.extract_text(pot_region)
        
        return {
            "table": table_info,
            "cards": cards_info,
            "pot": pot_text,
            "platform": self.platform
        }