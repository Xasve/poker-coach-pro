import cv2
import numpy as np

class TableDetector:
    """Detector simple de mesas"""
    
    def __init__(self):
        self.min_table_area = 50000
    
    def detect_table(self, screenshot):
        """Detectar mesa verde"""
        if screenshot is None or screenshot.size == 0:
            return None
        
        try:
            # Convertir a HSV
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Rango para verde (mesas típicas)
            lower_green = np.array([35, 50, 50])
            upper_green = np.array([85, 255, 255])
            
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # Buscar el más grande
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            
            if area < self.min_table_area:
                return None
            
            x, y, w, h = cv2.boundingRect(largest)
            return (x, y, x + w, y + h)
            
        except Exception as e:
            print(f"Error detectando mesa: {e}")
            return None
