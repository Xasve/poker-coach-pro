"""
CAPTURADOR DE PANTALLA OPTIMIZADO
Captura rápida de regiones específicas
"""

import pyautogui
import cv2
import numpy as np
import time

class ScreenCapturer:
    """Capturador optimizado de pantalla"""
    
    def __init__(self):
        self.last_capture_time = 0
        self.min_capture_interval = 0.2  # 200ms mínimo entre capturas
        self.cache = {}
        self.cache_duration = 1.0  # 1 segundo
    
    def capture_region(self, region):
        """Capturar región específica de la pantalla"""
        current_time = time.time()
        
        # Verificar cache
        cache_key = str(region)
        if cache_key in self.cache:
            cached_time, cached_image = self.cache[cache_key]
            if current_time - cached_time < self.cache_duration:
                return cached_image
        
        # Verificar intervalo mínimo
        if current_time - self.last_capture_time < self.min_capture_interval:
            time.sleep(self.min_capture_interval - (current_time - self.last_capture_time))
        
        try:
            # Capturar región
            x, y, width, height = region
            
            # Asegurar valores positivos
            x, y = max(0, x), max(0, y)
            width, height = max(1, width), max(1, height)
            
            # Capturar con pyautogui
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Convertir a numpy array
            screenshot_np = np.array(screenshot)
            
            # Convertir BGR a RGB (pyautogui usa RGB, OpenCV usa BGR)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Actualizar cache y timestamp
            self.cache[cache_key] = (current_time, screenshot_bgr)
            self.last_capture_time = current_time
            
            return screenshot_bgr
            
        except Exception as e:
            print(f"❌ Error capturando región {region}: {e}")
            return None
    
    def capture_full_screen(self):
        """Capturar pantalla completa"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            return screenshot_bgr
        except Exception as e:
            print(f"❌ Error capturando pantalla completa: {e}")
            return None
    
    def capture_multiple_regions(self, regions):
        """Capturar múltiples regiones eficientemente"""
        # Primero capturar pantalla completa
        full_screen = self.capture_full_screen()
        if full_screen is None:
            return {}
        
        results = {}
        for name, region in regions.items():
            x, y, w, h = region
            
            # Verificar límites
            height, width = full_screen.shape[:2]
            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))
            w = min(w, width - x)
            h = min(h, height - y)
            
            if w > 0 and h > 0:
                region_image = full_screen[y:y+h, x:x+w]
                results[name] = region_image
        
        return results
    
    def save_capture(self, image, filename):
        """Guardar captura en archivo"""
        if image is not None:
            cv2.imwrite(filename, image)
            return True
        return False