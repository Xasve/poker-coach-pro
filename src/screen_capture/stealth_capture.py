"""
Stealth Capture para PokerStars
"""
import numpy as np
import mss
import time
import random

class StealthScreenCapture:
    def __init__(self, platform: str = \"POKERSTARS\", stealth_level: str = \"MEDIUM\"):
        self.platform = platform
        self.stealth_level = stealth_level
        self.sct = mss.mss()
        print(f\"[Stealth Capture] Inicializado para {platform}\")
        print(f\"[Stealth Capture] Nivel de stealth: {stealth_level}\")
    
    def capture(self):
        \"\"\"Capturar pantalla completa\"\"\"
        try:
            # Capturar toda la pantalla
            monitor = self.sct.monitors[1]  # Monitor principal
            screenshot = self.sct.grab(monitor)
            
            # Convertir a numpy array
            img = np.array(screenshot, dtype=np.uint8)
            
            # Añadir variabilidad stealth
            if self.stealth_level == \"HIGH\":
                time.sleep(random.uniform(0.1, 0.3))
            elif self.stealth_level == \"MEDIUM\":
                time.sleep(random.uniform(0.05, 0.15))
            
            return img
            
        except Exception as e:
            print(f\"[Stealth Capture] Error en captura: {e}\")
            return None
    
    def capture_region(self, region):
        \"\"\"Capturar región específica\"\"\"
        try:
            screenshot = self.sct.grab(region)
            img = np.array(screenshot, dtype=np.uint8)
            return img
        except Exception as e:
            print(f\"[Stealth Capture] Error capturando región: {e}\")
            return None
