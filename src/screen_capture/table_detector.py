import cv2
import numpy as np

class TableDetector:
    """Detector básico de mesas"""
    
    def detect(self, image):
        """Detectar si hay una mesa en la imagen"""
        if image is None:
            return False
        
        # Método simple: buscar áreas verdes grandes
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Rango para verde
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])
            
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Contar píxeles verdes
            green_pixels = np.sum(mask > 0)
            total_pixels = image.shape[0] * image.shape[1]
            green_percentage = green_pixels / total_pixels
            
            return green_percentage > 0.1  # Más del 10% verde
            
        except Exception as e:
            print(f"Error detectando mesa: {e}")
            return False
