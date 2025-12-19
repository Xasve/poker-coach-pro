import mss
import cv2
import numpy as np
import time

class StealthScreenCapture:
    """Captura de pantalla stealth"""
    
    def __init__(self, monitor=1):
        self.monitor = monitor
        self.sct = None
        self.last_capture = 0
        self.capture_delay = 0.1
        
    def initialize(self):
        """Inicializar capturador"""
        try:
            self.sct = mss.mss()
            return True
        except Exception as e:
            print(f"Error inicializando MSS: {e}")
            return False
    
    def capture_screen(self, region=None):
        """Capturar pantalla"""
        if not self.sct:
            if not self.initialize():
                return np.zeros((100, 100, 3), np.uint8)
        
        try:
            current_time = time.time()
            if current_time - self.last_capture < self.capture_delay:
                time.sleep(self.capture_delay - (current_time - self.last_capture))
            
            if region:
                monitor = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2] - region[0],
                    "height": region[3] - region[1]
                }
            else:
                if len(self.sct.monitors) > self.monitor:
                    monitor = self.sct.monitors[self.monitor]
                else:
                    monitor = self.sct.monitors[1]
            
            screenshot = self.sct.grab(monitor)
            img = np.array(screenshot)
            
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            self.last_capture = time.time()
            return img
            
        except Exception as e:
            print(f"Error capturando: {e}")
            return np.zeros((100, 100, 3), np.uint8)
