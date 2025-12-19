# src/screen_capture/table_detector.py (AJUSTE PARA 7.44% VERDE)
import cv2
import numpy as np

class TableDetector:
    def __init__(self):
        """Inicializador mejorado para PokerStars"""
        print("🟢 TableDetector inicializado (modo MEJORADO)")
        
        # 🔥 AJUSTADO para tu 7.44% de verde
        self.lower_green1 = np.array([40, 40, 40])   # Ajustado según tus picos
        self.upper_green1 = np.array([85, 255, 255]) 
        
        # 🔥 UMBRAL OPTIMIZADO para tu 7.44%
        # Original: 0.015 (1.5%), Recomendado: 0.005 (0.5%) para más sensibilidad
        self.green_threshold = 0.005  # Más sensible!
        
        # Tamaño mínimo de región verde
        self.min_green_area = 30000  # píxeles
        
        print(f"📊 Configuración: umbral={self.green_threshold:.3%}")
    
    def detect(self, image):
        """
        Detectar si hay una mesa de poker en la imagen.
        """
        if image is None or image.size == 0:
            return False
        
        try:
            # Reducir tamaño para procesamiento más rápido
            height, width = image.shape[:2]
            if width > 1000:
                scale = 1000 / width
                new_width = 1000
                new_height = int(height * scale)
                image_resized = cv2.resize(image, (new_width, new_height))
            else:
                image_resized = image
            
            # Convertir a HSV
            hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)
            
            # Crear máscara de verde
            green_mask = cv2.inRange(hsv, self.lower_green1, self.upper_green1)
            
            # Aplicar operaciones morfológicas para limpiar
            kernel = np.ones((3, 3), np.uint8)
            green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
            green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Calcular estadísticas
            green_pixels = cv2.countNonZero(green_mask)
            total_pixels = green_mask.shape[0] * green_mask.shape[1]
            green_ratio = green_pixels / total_pixels
            
            # Contar áreas verdes grandes
            large_areas = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.min_green_area:
                    large_areas += 1
            
            # 🔥 CRITERIO MEJORADO: Verde suficiente O áreas grandes
            table_detected = (green_ratio > self.green_threshold) or (large_areas > 0)
            
            # Solo mostrar debug si cambia el estado
            if table_detected:
                print(f"✅ Mesa detectada (verde: {green_ratio:.2%}, áreas: {large_areas})")
            # No imprimir cuando no detecta para reducir spam
            
            return table_detected
            
        except Exception as e:
            print(f"⚠️  Error en detección: {e}")
            return False
    
    def get_table_region(self, image):
        """Obtener región de la mesa"""
        height, width = image.shape[:2]
        return (0, 0, width, height)
    
    def adjust_threshold(self, new_threshold):
        """Ajustar umbral dinámicamente"""
        self.green_threshold = new_threshold
        print(f"📊 Umbral ajustado a: {self.green_threshold:.3%}")