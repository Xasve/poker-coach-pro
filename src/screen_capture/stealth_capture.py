import mss
import cv2
import numpy as np
import time
from typing import Optional, Tuple

class StealthScreenCapture:
    """Captura de pantalla stealth para evitar detección"""
    
    def __init__(self, monitor: int = 1):
        self.monitor = monitor
        self.sct = mss.mss()
        self.last_capture_time = 0
        self.capture_delay = 0.1
        
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Captura pantalla o región específica"""
        try:
            if region:
                monitor = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2] - region[0],
                    "height": region[3] - region[1]
                }
            else:
                monitor = self.sct.monitors[self.monitor]
            
            screenshot = self.sct.grab(monitor)
            img = np.array(screenshot)
            
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            return img
            
        except Exception as e:
            print(f"Error capturando pantalla: {e}")
            return np.zeros((100, 100, 3), dtype=np.uint8)
