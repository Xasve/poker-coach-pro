# auto_template_capturer.py - Sistema automático de captura
import cv2
import numpy as np
import os
import time
import json
from datetime import datetime
import mss
from pathlib import Path

class AutoTemplateCapturer:
    """Capturador automático de templates de cartas"""
    
    def __init__(self, config_path="config/pokerstars_coords.json"):
        self.config_path = config_path
        self.regions = self.load_regions()
        self.captured_count = 0
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def load_regions(self):
        """Cargar regiones de captura desde configuración"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get("pokerstars_regions", {})
        return {}
    
    def setup_capture_folders(self):
        """Configurar estructura de carpetas para captura"""
        base_path = "data/card_templates/auto_captured"
        
        folders = [
            "session_data",
            "raw_captures", 
            "processed_cards",
            "classified",
            "training_data"
        ]
        
        for folder in folders:
            path = os.path.join(base_path, self.session_id, folder)
            os.makedirs(path, exist_ok=True)
            print(f" {path}")
        
        self.session_folder = os.path.join(base_path, self.session_id)
        return self.session_folder
    
    def capture_table_screenshot(self):
        """Capturar pantalla completa de la mesa"""
        try:
            with mss.mss() as sct:
                if not self.regions:
                    print("❌ No hay regiones configuradas")
                    return None
                
                mesa = self.regions.get("mesa", [0, 0, 1920, 1080])
                monitor = {
                    "top": mesa[1],
                    "left": mesa[0],
                    "width": mesa[2],
                    "height": mesa[3]
                }
                
                screenshot = np.array(sct.grab(monitor))
                return screenshot
        except Exception as e:
            print(f" Error capturando pantalla: {e}")
            return None
    
    def detect_card_candidates(self, screenshot):
        """Detectar posibles cartas en la captura"""
        if screenshot is None:
            return []
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Aplicar filtros para encontrar cartas
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilatar para conectar bordes
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, 
                                      cv2.CHAIN_APPROX_SIMPLE)
        
        candidates = []
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filtrar por tamaño y relación de aspecto (cartas ~70x95)
            if 3000 < area < 8000 and 0.6 < w/h < 0.9:
                candidates.append({
                    "contour": contour,
                    "bbox": (x, y, w, h),
                    "area": area,
                    "image": screenshot[y:y+h, x:x+w]
                })
        
        print(f" Candidatos detectados: {len(candidates)}")
        return candidates
    
    def extract_card_features(self, card_image):
        """Extraer características de una carta para identificación"""
        if card_image.size == 0:
            return None
        
        # Redimensionar a tamaño estándar
        standard_size = (70, 95)
        resized = cv2.resize(card_image, standard_size)
        
        # Convertir a diferentes espacios de color
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        
        # Detectar esquinas
        corners = cv2.goodFeaturesToTrack(gray, 4, 0.01, 10)
        
        # Calcular histogramas
        hist_bgr = []
        for i in range(3):  # B, G, R
            hist = cv2.calcHist([resized], [i], None, [32], [0, 256])
            hist_bgr.append(hist.flatten())
        
        # Características combinadas
        features = {
            "size": card_image.shape[:2],
            "aspect_ratio": card_image.shape[1] / card_image.shape[0],
            "corners_count": len(corners) if corners is not None else 0,
            "histograms": hist_bgr,
            "mean_color": np.mean(card_image, axis=(0, 1)).tolist()
        }
        
        return features
    
    def save_card_candidate(self, card_image, candidate_info):
        """Guardar candidato a carta"""
        timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]
        filename = f"card_{self.captured_count:04d}_{timestamp}.png"
        
        # Guardar en raw_captures
        raw_path = os.path.join(self.session_folder, "raw_captures", filename)
        cv2.imwrite(raw_path, card_image)
        
        # Guardar metadatos
        metadata = {
            "filename": filename,
            "candidate_id": self.captured_count,
            "timestamp": datetime.now().isoformat(),
            "bbox": candidate_info["bbox"],
            "area": candidate_info["area"],
            "features": self.extract_card_features(card_image),
            "session_id": self.session_id
        }
        
        metadata_path = raw_path.replace('.png', '.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.captured_count += 1
        print(f" Guardado: {filename}")
        
        return raw_path, metadata
    
    def continuous_capture_mode(self, duration_seconds=300, interval=2):
        """Modo de captura continua"""
        print(f"\n MODO CAPTURA CONTINUA")
        print(f"   Duración: {duration_seconds} segundos")
        print(f"   Intervalo: {interval} segundos")
        print("   Presiona Ctrl+C para detener")
        print("=" * 50)
        
        self.setup_capture_folders()
        
        start_time = time.time()
        capture_cycles = 0
        
        try:
            while time.time() - start_time < duration_seconds:
                capture_cycles += 1
                print(f"\n Ciclo {capture_cycles}")
                
                # Capturar pantalla
                screenshot = self.capture_table_screenshot()
                if screenshot is None:
                    print("    Fallo captura, esperando...")
                    time.sleep(interval)
                    continue
                
                # Detectar candidatos
                candidates = self.detect_card_candidates(screenshot)
                
                # Procesar cada candidato
                for candidate in candidates:
                    card_img = candidate["image"]
                    
                    # Filtrar imágenes muy oscuras o claras
                    mean_brightness = np.mean(cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY))
                    if 30 < mean_brightness < 220:  # Rango de brillo aceptable
                        self.save_card_candidate(card_img, candidate)
                
                print(f"    Total capturadas: {self.captured_count}")
                
                # Esperar intervalo
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n  Captura interrumpida por usuario")
        
        finally:
            self.generate_session_report()
    
    def generate_session_report(self):
        """Generar reporte de la sesión de captura"""
        report = {
            "session_id": self.session_id,
            "start_time": self.session_id,
            "end_time": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "total_captured": self.captured_count,
            "session_folder": self.session_folder,
            "regions_used": self.regions,
            "system_info": {
                "opencv_version": cv2.__version__,
                "numpy_version": np.__version__
            }
        }
        
        report_path = os.path.join(self.session_folder, "session_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n REPORTE DE SESIÓN:")
        print(f"   📁 Carpeta: {self.session_folder}")
        print(f"   📸 Cartas capturadas: {self.captured_count}")
        print(f"    Reporte: {report_path}")
        
        return report_path

# Función principal
def main():
    """Función principal del capturador automático"""
    print(" CAPTURADOR AUTOMÁTICO DE TEMPLATES")
    print("=" * 60)
    
    capturer = AutoTemplateCapturer()
    
    if not capturer.regions:
        print(" No hay configuración de PokerStars")
        print("   Ejecuta primero: python detect_coords.py")
        return
    
    print(" Configuración cargada")
    print(f"   Regiones: {len(capturer.regions)}")
    
    # Iniciar captura continua (5 minutos por defecto)
    capturer.continuous_capture_mode(duration_seconds=300, interval=2)

if __name__ == "__main__":
    main()
