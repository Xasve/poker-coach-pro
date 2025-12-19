# stealth_capture.py - VERSIÓN CORREGIDA
import mss
import cv2
import numpy as np

class StealthScreenCapture:
    def __init__(self, platform, stealth_level="MEDIUM"):
        """Inicializar capturador stealth
        
        Args:
            platform: str - "pokerstars", "ggpoker", etc.
            stealth_level: str o int - "LOW"/1, "MEDIUM"/2, "HIGH"/3
        """
        self.platform = platform
        
        # Convertir nivel stealth a número si es string
        if isinstance(stealth_level, str):
            stealth_map = {
                "LOW": 1,
                "MEDIUM": 2, 
                "HIGH": 3,
                "1": 1,
                "2": 2,
                "3": 3
            }
            self.stealth_level = stealth_map.get(stealth_level.upper(), 2)
        else:
            # Asegurar que sea 1, 2 o 3
            self.stealth_level = max(1, min(3, int(stealth_level)))
        
        self.sct = mss.mss()
        self.last_capture = None
        
        print(f"[StealthCapture] Plataforma: {platform}, Nivel: {self.stealth_level}")
    
    def capture_screen(self, region=None):
        """Capturar pantalla completa o región específica"""
        try:
            if region:
                monitor = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2],
                    "height": region[3]
                }
            else:
                # Capturar monitor principal
                monitor = self.sct.monitors[1]
            
            # Capturar
            screenshot = self.sct.grab(monitor)
            
            # Convertir a numpy array para OpenCV
            img_array = np.array(screenshot)
            
            # Convertir BGRA a BGR (eliminar canal alpha)
            if img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
            
            self.last_capture = img_array
            return img_array
            
        except Exception as e:
            print(f"[ERROR] Captura fallida: {e}")
            return None
    
    def get_last_capture(self):
        """Obtener última captura"""
        return self.last_capture
    
    def start_capture(self):
        """Iniciar captura continua (placeholder)"""
        print("[StealthCapture] Captura iniciada")
        return True
    
    def stop_capture(self):
        """Detener captura continua"""
        print("[StealthCapture] Captura detenida")
        return True