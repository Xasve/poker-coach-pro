# actualizar src/screen_capture/table_detector.py
import cv2
import numpy as np

class TableDetector:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Cargar templates para detectar mesas de PokerStars"""
        # En una versión real, cargaría imágenes de templates
        return {}
    
    def detect(self, screenshot):
        """Detectar mesa de poker en la captura"""
        height, width = screenshot.shape[:2]
        
        # Intentar detección real primero
        table_found = self._detect_pokerstars_table(screenshot)
        
        if table_found:
            return {
                "region": table_found,
                "confidence": 0.95,
                "type": "pokerstars_table",
                "detected": True
            }
        else:
            # Modo simulado para pruebas
            print("⚠️  Usando detección simulada - PokerStars no detectado")
            return {
                "region": (width//4, height//4, width//2, height//2),
                "confidence": 0.5,
                "type": "simulated_table",
                "detected": False
            }
    
    def _detect_pokerstars_table(self, screenshot):
        """Intentar detectar mesa real de PokerStars"""
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Buscar colores característicos de PokerStars (verde)
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Rango de verde (mesa de PokerStars)
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])
            
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Tomar el contorno más grande
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Filtrar por tamaño (debe ser una mesa considerable)
                if w > 400 and h > 200:
                    print(f"✅ Mesa PokerStars detectada: {x}, {y}, {w}, {h}")
                    return (x, y, w, h)
            
            return None
            
        except Exception as e:
            print(f"Error en detección: {e}")
            return None