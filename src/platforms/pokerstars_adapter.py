import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen_capture.stealth_capture import StealthScreenCapture
from screen_capture.table_detector import TableDetector
from screen_capture.card_recognizer import CardRecognizer
from screen_capture.text_ocr import TextOCR

class PokerStarsAdapter:
    def __init__(self, stealth_level="MEDIUM"):
        self.platform = "pokerstars"
        self.stealth_level = stealth_level
        
        print(f"Inicializando PokerStarsAdapter (stealth: {stealth_level})")
        
        self.capture_system = StealthScreenCapture(self.platform, self.stealth_level)
        self.table_detector = TableDetector()
        self.card_recognizer = CardRecognizer(platform=self.platform)
        self.text_ocr = TextOCR()
        
        print("PokerStarsAdapter listo")
    
    def start(self):
        print("Iniciando captura...")
        return self.capture_system.start_capture()
    
    def stop(self):
        print("Deteniendo captura...")
        return self.capture_system.stop_capture()
    
    def get_table_state(self):
        try:
            screenshot = self.capture_system.capture_screen()
            
            if screenshot is None:
                return self._get_simulated_state()
            
            table_info = self.table_detector.detect(screenshot)
            cards_info = self.card_recognizer.recognize(screenshot, table_info.get("region", (0, 0, 1920, 1080)))
            pot_text = self.text_ocr.extract_text(screenshot, (100, 100, 200, 40))
            
            return {
                "table": table_info,
                "cards": cards_info,
                "pot": pot_text,
                "platform": self.platform,
                "simulated": False,
                "timestamp": time.time()
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return self._get_simulated_state()
    
    def _get_simulated_state(self):
        return {
            "simulated": True,
            "cards": {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"]},
            "pot": "1250",
            "players": 6,
            "position": "middle",
            "platform": self.platform,
            "timestamp": time.time()
        }
