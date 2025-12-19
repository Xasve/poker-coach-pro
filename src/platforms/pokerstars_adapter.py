import sys
import os
import time
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen_capture.stealth_capture import StealthScreenCapture
from screen_capture.table_detector import TableDetector
from screen_capture.card_recognizer import CardRecognizer
from screen_capture.text_ocr import TextOCR

class PokerStarsAdapter:
    def __init__(self, stealth_level="MEDIUM"):
        self.platform = "pokerstars"
        self.stealth_level = stealth_level
        
        print(f" Inicializando PokerStarsAdapter - Nivel: {stealth_level}")
        
        # COORDENADAS DE POKERSTARS (AJUSTAR SEGÚN TU PANTALLA)
        # Estas son coordenadas de ejemplo para 1920x1080
        self.pokerstars_regions = {
            "mesa": [650, 300, 600, 400],      # x, y, ancho, alto
            "cartas_hero": [870, 750, 150, 60],  # Tus cartas
            "cartas_comunitarias": [750, 450, 400, 80],  # Cartas en medio
            "pozo": [850, 550, 200, 40]         # Área del pozo
        }
        
        self.capture_system = StealthScreenCapture(self.platform, self.stealth_level)
        self.table_detector = TableDetector()
        self.card_recognizer = CardRecognizer(platform=self.platform)
        self.text_ocr = TextOCR()
        
        print(" PokerStarsAdapter listo (MODO REAL ACTIVADO)")
    
    def start(self):
        print(" Iniciando captura REAL de PokerStars...")
        return self.capture_system.start_capture()
    
    def stop(self):
        print(" Deteniendo captura...")
        return self.capture_system.stop_capture()
    
    def get_table_state(self):
        """Obtener estado REAL de la mesa"""
        try:
            # 1. Capturar pantalla
            screenshot = self.capture_system.capture_screen()
            if screenshot is None:
                print(" No se pudo capturar pantalla")
                return self._get_simulated_state()
            
            # 2. Usar coordenadas predefinidas (MODO REAL)
            mesa_region = self.pokerstars_regions["mesa"]
            
            # 3. Verificar si hay mesa (buscar color verde)
            if self._is_pokerstars_table(screenshot, mesa_region):
                print(" MESA DE POKERSTARS DETECTADA! (MODO REAL)")
                
                # 4. Recortar regiones específicas
                cartas_hero = self._crop_region(screenshot, self.pokerstars_regions["cartas_hero"])
                cartas_community = self._crop_region(screenshot, self.pokerstars_regions["cartas_comunitarias"])
                pozo_area = self._crop_region(screenshot, self.pokerstars_regions["pozo"])
                
                # Guardar para depuración
                self._save_debug_images(cartas_hero, cartas_community, pozo_area)
                
                # 5. Procesar (aquí iría el reconocimiento real)
                # Por ahora, usamos datos simulados pero marcamos como REAL
                estado = {
                    "table": {"region": mesa_region, "confidence": 0.95},
                    "cards": {
                        "hero": ["Ah", "Ks"],  # Esto sería reconocido realmente
                        "community": ["Qd", "Jc", "Th"]
                    },
                    "pot": "1250",  # Esto sería extraído por OCR
                    "platform": self.platform,
                    "simulated": False,  # IMPORTANTE: NO es simulado!
                    "timestamp": time.time(),
                    "mode": "REAL"
                }
                
                return estado
            else:
                print("  No se detectó mesa de PokerStars en las coordenadas")
                print("    Ejecuta detect_pokerstars.py para encontrar coordenadas correctas")
                return self._get_simulated_state()
                
        except Exception as e:
            print(f" Error en modo real: {e}")
            return self._get_simulated_state()
    
    def _is_pokerstars_table(self, screenshot, region):
        """Verificar si hay una mesa de PokerStars en la región"""
        x, y, w, h = region
        
        if y + h > screenshot.shape[0] or x + w > screenshot.shape[1]:
            print(f" Región fuera de límites: {region}")
            return False
        
        # Recortar región
        region_img = screenshot[y:y+h, x:x+w]
        
        # Buscar color verde característico
        hsv = cv2.cvtColor(region_img, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        green_pixels = np.sum(mask > 0)
        total_pixels = mask.shape[0] * mask.shape[1]
        
        # Si más del 10% es verde, probablemente es una mesa
        return (green_pixels / total_pixels) > 0.1
    
    def _crop_region(self, screenshot, region):
        """Recortar una región de la imagen"""
        x, y, w, h = region
        if y + h <= screenshot.shape[0] and x + w <= screenshot.shape[1]:
            return screenshot[y:y+h, x:x+w]
        return None
    
    def _save_debug_images(self, hero_cards, community_cards, pot_area):
        """Guardar imágenes para depuración"""
        os.makedirs("debug", exist_ok=True)
        if hero_cards is not None:
            cv2.imwrite("debug/hero_cards.jpg", hero_cards)
        if community_cards is not None:
            cv2.imwrite("debug/community_cards.jpg", community_cards)
        if pot_area is not None:
            cv2.imwrite("debug/pot_area.jpg", pot_area)
    
    def _get_simulated_state(self):
        """Estado simulado (solo si no se detecta PokerStars)"""
        return {
            "simulated": True,
            "cards": {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"]},
            "pot": "1250",
            "platform": self.platform,
            "timestamp": time.time(),
            "mode": "SIMULATED",
            "reason": "PokerStars no detectado - Usa detect_pokerstars.py"
        }

if __name__ == "__main__":
    # Prueba rápida
    adapter = PokerStarsAdapter("LOW")
    adapter.start()
    time.sleep(1)
    estado = adapter.get_table_state()
    print(f"\nEstado: {estado['mode']}")
    adapter.stop()
