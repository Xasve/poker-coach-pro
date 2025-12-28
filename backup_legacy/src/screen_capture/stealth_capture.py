import mss
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
