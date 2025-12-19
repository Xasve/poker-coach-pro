# nuclear_fix.py
import os
import shutil

def nuclear_fix():
    """Solución nuclear: Recrear estructura completa"""
    
    print("⚡ SOLUCIÓN NUCLEAR: RECREANDO ESTRUCTURA")
    print("=" * 60)
    
    # 1. Archivos críticos que deben existir
    critical_files = {
        "src/screen_capture/stealth_capture.py": '''import mss
import cv2
import numpy as np

class StealthScreenCapture:
    def __init__(self, platform, stealth_level="MEDIUM"):
        self.platform = platform
        
        # Convertir nivel stealth
        if isinstance(stealth_level, str):
            stealth_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
            self.stealth_level = stealth_map.get(stealth_level.upper(), 2)
        else:
            self.stealth_level = max(1, min(3, int(stealth_level)))
        
        self.sct = mss.mss()
        self.last_capture = None
        
    def capture_screen(self, region=None):
        try:
            if region:
                monitor = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2],
                    "height": region[3]
                }
            else:
                monitor = self.sct.monitors[1]
            
            screenshot = self.sct.grab(monitor)
            img_array = np.array(screenshot)
            
            if img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
            
            self.last_capture = img_array
            return img_array
            
        except Exception as e:
            print(f"Error captura: {e}")
            return None
    
    def get_last_capture(self):
        return self.last_capture
    
    def start_capture(self):
        return True
    
    def stop_capture(self):
        return True
''',
        
        "src/screen_capture/table_detector.py": '''import cv2
import numpy as np

class TableDetector:
    def __init__(self):
        pass
    
    def detect(self, screenshot):
        # Simulación para pruebas
        height, width = screenshot.shape[:2]
        return {
            "region": (width//4, height//4, width//2, height//2),
            "confidence": 0.95,
            "type": "poker_table"
        }
''',
        
        "src/screen_capture/card_recognizer.py": '''import cv2
import numpy as np
import os

class CardRecognizer:
    def __init__(self, platform="pokerstars"):
        self.platform = platform
        print(f"CardRecognizer para {platform}")
    
    def recognize(self, screenshot, table_region):
        # Simulación para pruebas
        return {
            "hero": ["Ah", "Ks"],
            "community": ["Qd", "Jc", "Th"],
            "confidence": 0.9
        }
''',
        
        "src/screen_capture/text_ocr.py": '''import cv2
import numpy as np

class TextOCR:
    def __init__(self):
        pass
    
    def extract_text(self, screenshot, region):
        # Simulación para pruebas
        return "1250"
''',
        
        "src/platforms/pokerstars_adapter.py": '''import sys
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
''',
        
        "src/core/poker_engine.py": '''import random

class PokerEngine:
    def __init__(self, aggression=1.0, tightness=1.0):
        self.aggression = aggression
        self.tightness = tightness
        print(f"PokerEngine inicializado")
    
    def analyze_hand(self, hole_cards=None, community_cards=None, pot_size=0, position="middle"):
        print(f"Analizando: {hole_cards} vs {community_cards}, pot: {pot_size}, pos: {position}")
        
        # Lógica simple
        if hole_cards and len(hole_cards) >= 2:
            rank1 = hole_cards[0][0] if hole_cards[0] else '2'
            rank2 = hole_cards[1][0] if hole_cards[1] else '2'
            
            if rank1 == rank2:
                action = "RAISE"
                confidence = 0.8
                reason = "Pareja"
            elif rank1 in 'AKQJ' and rank2 in 'AKQJ':
                action = "CALL"
                confidence = 0.7
                reason = "Cartas altas"
            else:
                action = random.choice(["CHECK", "FOLD"])
                confidence = 0.5
                reason = "Mano promedio"
        else:
            action = "CHECK"
            confidence = 0.5
            reason = "Sin datos"
        
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "hand_strength": 0.5
        }
'''
    }
    
    # 2. Crear directorios
    for dir_path in ['src', 'src/screen_capture', 'src/platforms', 'src/core', 'config', 'debug']:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Creado: {dir_path}/")
    
    # 3. Crear archivos __init__.py
    for init_file in ['src/__init__.py', 'src/screen_capture/__init__.py', 
                     'src/platforms/__init__.py', 'src/core/__init__.py']:
        with open(init_file, 'w') as f:
            f.write('# Package initialization\n')
        print(f"📄 Creado: {init_file}")
    
    # 4. Crear archivos críticos
    for file_path, content in critical_files.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Creado: {file_path}")
    
    # 5. Crear configuración
    config_content = '''capture:
  stealth_level: MEDIUM
  interval: 1.0

platforms:
  default: pokerstars

overlay:
  enabled: false
'''
    
    with open('config/default_config.yaml', 'w') as f:
        f.write(config_content)
    print(f"📄 Creado: config/default_config.yaml")
    
    print("\n" + "=" * 60)
    print("✅ ESTRUCTURA RECREADA COMPLETAMENTE")
    print("\n🎯 Ejecutar test: python test_final_corrected.py")

if __name__ == "__main__":
    nuclear_fix()