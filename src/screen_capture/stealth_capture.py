import mss
import cv2
import numpy as np

class StealthScreenCapture:
    """Captura básica de pantalla"""
    
    def __init__(self, platform=None, stealth_level=None):
        """Constructor corregido"""
        self.platform = platform
        self.stealth_level = stealth_level
        self.sct = None
        self.last_capture = 0
        print(f"📷 Capturador: {platform or 'default'}")
    
    def initialize(self):
        """Inicializar capturador"""
        try:
            self.sct = mss.mss()
            return True
        except Exception as e:
            print(f"Error inicializando MSS: {e}")
            return False
    
    def capture(self):
        """Capturar pantalla completa"""
        if not self.sct:
            if not self.initialize():
                return None
        
        try:
            screenshot = self.sct.grab(self.sct.monitors[1])
            img = np.array(screenshot)
            
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            return img
        except Exception as e:
            print(f"Error capturando: {e}")
            return None
