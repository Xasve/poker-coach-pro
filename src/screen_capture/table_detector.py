# src/screen_capture/table_detector.py (MEJORADO)
import cv2
import numpy as np

class TableDetector:
    def __init__(self):
        """Inicializador mejorado para PokerStars"""
        print("🟢 TableDetector inicializado (modo mejorado)")
        
        # 🔥 RANGOS MEJORADOS para verde de PokerStars
        # PokerStars usa varios tonos de verde
        self.lower_green1 = np.array([35, 40, 40])   # Verde más claro
        self.upper_green1 = np.array([85, 255, 255]) # Verde más oscuro
        
        # Rangos alternativos para diferentes temas/mesas
        self.lower_green2 = np.array([40, 30, 30])
        self.upper_green2 = np.array([90, 255, 200])
        
        # Umbral de detección (5% era muy alto, bajamos a 1.5%)
        self.green_threshold = 0.015  # 1.5% de píxeles verdes
        
        # Tamaño mínimo de región verde (para evitar falsos positivos)
        self.min_green_area = 50000  # píxeles
        
    def detect(self, image):
        """
        Detectar si hay una mesa de poker en la imagen.
        Versión mejorada con múltiples rangos y filtros.
        """
        if image is None or image.size == 0:
            print("❌ Imagen inválida para detección")
            return False
        
        try:
            # Reducir tamaño para procesamiento más rápido (opcional)
            height, width = image.shape[:2]
            if width > 1000:
                scale = 1000 / width
                new_width = 1000
                new_height = int(height * scale)
                image_resized = cv2.resize(image, (new_width, new_height))
            else:
                image_resized = image
            
            # Convertir a HSV para mejor detección de color
            hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)
            
            # Crear máscaras con múltiples rangos de verde
            mask1 = cv2.inRange(hsv, self.lower_green1, self.upper_green1)
            mask2 = cv2.inRange(hsv, self.lower_green2, self.upper_green2)
            
            # Combinar máscaras
            green_mask = cv2.bitwise_or(mask1, mask2)
            
            # Aplicar operaciones morfológicas para limpiar la máscara
            kernel = np.ones((5, 5), np.uint8)
            green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
            green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
            
            # Encontrar contornos de regiones verdes
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Buscar contornos grandes (mesas)
            large_green_areas = 0
            total_green_pixels = cv2.countNonZero(green_mask)
            total_pixels = green_mask.shape[0] * green_mask.shape[1]
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.min_green_area:
                    large_green_areas += 1
            
            # Calcular ratio de píxeles verdes
            green_ratio = total_green_pixels / total_pixels
            
            # 🔥 CRITERIO MEJORADO de detección:
            # 1. Suficientes píxeles verdes O
            # 2. Contornos grandes de verde
            table_detected = (green_ratio > self.green_threshold) or (large_green_areas > 0)
            
            # Información de debug
            if table_detected:
                print(f"✅ Mesa detectada (verde: {green_ratio:.2%}, áreas grandes: {large_green_areas})")
            else:
                if total_green_pixels > 0:
                    print(f"❌ Mesa no detectada (verde: {green_ratio:.2%}, umbral: {self.green_threshold:.2%})")
                # No imprimir cuando no hay verde para reducir spam
            
            return table_detected
            
        except Exception as e:
            print(f"⚠️  Error en detección de mesa: {e}")
            return False
    
    def get_table_region(self, image):
        """Obtener la región de la mesa"""
        height, width = image.shape[:2]
        
        # Por defecto, usar toda la pantalla
        # En versión avanzada, detectar contorno exacto
        return (0, 0, width, height)
    
    def adjust_threshold(self, new_threshold):
        """Ajustar umbral de detección dinámicamente"""
        self.green_threshold = max(0.001, min(0.5, new_threshold))
        print(f"📊 Umbral de verde ajustado a: {self.green_threshold:.3%}")
    
    def calibrate_for_image(self, image_path):
        """Calibrar rangos de color para una imagen específica"""
        print("🎨 Calibrando detector para imagen...")
        
        image = cv2.imread(image_path)
        if image is None:
            print("❌ No se pudo cargar imagen para calibración")
            return
        
        # Analizar histograma de colores
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Calcular valores promedio de verde
        mask = cv2.inRange(hsv, self.lower_green1, self.upper_green1)
        green_pixels = hsv[mask > 0]
        
        if len(green_pixels) > 0:
            h_mean = np.mean(green_pixels[:, 0])
            s_mean = np.mean(green_pixels[:, 1])
            v_mean = np.mean(green_pixels[:, 2])
            
            print(f"📊 Estadísticas de verde:")
            print(f"   Hue promedio: {h_mean:.1f}")
            print(f"   Saturación promedio: {s_mean:.1f}")
            print(f"   Valor promedio: {v_mean:.1f}")
            
            # Ajustar rangos basados en los promedios
            self.lower_green1 = np.array([max(0, h_mean-20), max(0, s_mean-40), max(0, v_mean-40)])
            self.upper_green1 = np.array([min(180, h_mean+20), min(255, s_mean+40), min(255, v_mean+40)])
            
            print("✅ Rangos de color ajustados automáticamente")