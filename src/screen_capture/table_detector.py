import cv2
import numpy as np
from typing import Optional, Tuple

class TableDetector:
    """Detecta mesas de poker en la pantalla"""
    
    def __init__(self):
        # Colores característicos de mesas verdes
        self.green_table_lower = np.array([40, 40, 40])
        self.green_table_upper = np.array([80, 255, 255])
        
    def detect_table(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Encuentra la mesa de poker en la captura"""
        if screenshot is None or screenshot.size == 0:
            print("⚠️  Screenshot vacía")
            return None
        
        try:
            # Convertir a HSV para mejor detección de color
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Crear máscara para colores verdes (mesas típicas)
            mask = cv2.inRange(hsv, self.green_table_lower, self.green_table_upper)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                print("⚠️  No se encontraron contornos verdes")
                return None
            
            # Buscar el contorno más grande
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Filtrar por tamaño mínimo
            if area < 50000:  # Muy pequeño para ser una mesa
                print(f"⚠️  Contorno muy pequeño: {area:.0f} píxeles")
                return None
            
            # Obtener bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            print(f"✅ Mesa detectada - Área: {area:.0f}px, Posición: ({x}, {y}, {w}, {h})")
            return (x, y, x + w, y + h)
            
        except Exception as e:
            print(f"❌ Error detectando mesa: {e}")
            return None