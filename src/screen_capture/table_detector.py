# src/screen_capture/table_detector.py
import cv2
import numpy as np

class TableDetector:
    def __init__(self):
        """Inicializador CORREGIDO: ahora no toma argumentos"""
        print("🟢 TableDetector inicializado (modo simple)")
        # Rangos de color para detectar mesas verdes (PokerStars)
        self.lower_green = np.array([40, 40, 40])
        self.upper_green = np.array([80, 255, 255])
    
    def detect(self, image):
        """
        Detectar si hay una mesa de poker en la imagen.
        Returns:
            bool: True si se detecta una mesa, False en caso contrario
        """
        if image is None:
            return False
        
        try:
            # Convertir a HSV para mejor detección de color
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Crear máscara para el color verde de la mesa
            mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
            
            # Contar píxeles verdes
            green_pixels = cv2.countNonZero(mask)
            total_pixels = image.shape[0] * image.shape[1]
            green_ratio = green_pixels / total_pixels
            
            # Si más del 5% de la imagen es verde, asumimos que es una mesa
            table_detected = green_ratio > 0.05
            
            if table_detected:
                print(f"✅ Mesa detectada (verde: {green_ratio:.1%})")
            else:
                print(f"❌ Mesa no detectada (verde: {green_ratio:.1%})")
            
            return table_detected
            
        except Exception as e:
            print(f"⚠️  Error en detección de mesa: {e}")
            return False
    
    def get_table_region(self, image):
        """Obtener la región de la mesa (placeholder)"""
        # Por ahora, devolver toda la imagen
        height, width = image.shape[:2]
        return (0, 0, width, height)