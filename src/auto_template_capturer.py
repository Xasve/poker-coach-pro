# auto_template_capturer.py - VERSIÓN CORREGIDA
import cv2
import numpy as np
import os
import time
import json
from datetime import datetime
import mss
from pathlib import Path

class AutoTemplateCapturer:
    """Capturador automático de templates de cartas - VERSIÓN CORREGIDA"""
    
    def __init__(self, config_path="config/pokerstars_coords.json"):
        self.config_path = config_path
        self.regions = self.load_regions()
        self.captured_count = 0
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_folder = None
        
    def load_regions(self):
        """Cargar regiones de captura desde configuración"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get("pokerstars_regions", {})
        return {}
    
    def setup_capture_folders(self):
        """Configurar estructura de carpetas para captura - VERSIÓN SIMPLIFICADA"""
        base_path = "data/card_templates/auto_captured"
        
        # SOLO DOS CARPETAS: raw_captures y reports
        folders = [
            "raw_captures", 
            "reports"
        ]
        
        # Crear carpeta de sesión principal
        self.session_folder = os.path.join(base_path, self.session_id)
        os.makedirs(self.session_folder, exist_ok=True)
        
        # Crear subcarpetas
        for folder in folders:
            path = os.path.join(self.session_folder, folder)
            os.makedirs(path, exist_ok=True)
        
        print(f" Sesión creada: {self.session_folder}")
        
        # Guardar información básica de la sesión
        session_info = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "folders": folders,
            "regions_used": list(self.regions.keys()) if self.regions else []
        }
        
        info_path = os.path.join(self.session_folder, "session_info.json")
        with open(info_path, 'w') as f:
            json.dump(session_info, f, indent=2)
        
        return self.session_folder
    
    def capture_table_screenshot(self):
        """Capturar pantalla completa de la mesa"""
        try:
            with mss.mss() as sct:
                if not self.regions:
                    print("  Usando pantalla completa (regiones no configuradas)")
                    monitor = sct.monitors[1]
                else:
                    mesa = self.regions.get("mesa", sct.monitors[1])
                    if isinstance(mesa, list) and len(mesa) >= 4:
                        monitor = {
                            "top": mesa[1],
                            "left": mesa[0],
                            "width": min(mesa[2], 800),  # Limitar tamaño para performance
                            "height": min(mesa[3], 600)
                        }
                    else:
                        monitor = sct.monitors[1]
                
                screenshot = np.array(sct.grab(monitor))
                return screenshot
        except Exception as e:
            print(f"❌ Error capturando pantalla: {e}")
            return None
    
    def simple_capture_mode(self, duration_seconds=120, interval=2):
        """Modo de captura simple y robusto"""
        print(f"\n INICIANDO CAPTURA SIMPLE")
        print(f"   Duración: {duration_seconds} segundos")
        print(f"   Intervalo: {interval} segundos")
        print("=" * 50)
        
        # Configurar carpetas
        self.setup_capture_folders()
        
        start_time = time.time()
        last_save_time = time.time()
        
        try:
            with mss.mss() as sct:
                # Configurar monitor
                if not self.regions:
                    monitor = sct.monitors[1]
                else:
                    mesa = self.regions.get("mesa", sct.monitors[1])
                    if isinstance(mesa, list) and len(mesa) >= 4:
                        monitor = {
                            "top": mesa[1],
                            "left": mesa[0],
                            "width": min(mesa[2], 800),
                            "height": min(mesa[3], 600)
                        }
                    else:
                        monitor = sct.monitors[1]
                
                while time.time() - start_time < duration_seconds:
                    elapsed = time.time() - start_time
                    remaining = duration_seconds - elapsed
                    
                    # Actualizar progreso
                    print(f"\r  {int(elapsed)}s / {duration_seconds}s |  {self.captured_count} imágenes", end="")
                    
                    # Capturar cada 'interval' segundos
                    if time.time() - last_save_time >= interval:
                        try:
                            # Capturar pantalla
                            screenshot = np.array(sct.grab(monitor))
                            
                            if screenshot is not None and screenshot.size > 0:
                                # Guardar imagen
                                timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]
                                filename = f"capture_{self.captured_count:04d}_{timestamp}.png"
                                filepath = os.path.join(self.session_folder, "raw_captures", filename)
                                
                                cv2.imwrite(filepath, screenshot)
                                
                                # Guardar metadatos básicos
                                metadata = {
                                    "filename": filename,
                                    "timestamp": datetime.now().isoformat(),
                                    "capture_number": self.captured_count,
                                    "elapsed_seconds": elapsed
                                }
                                
                                metadata_path = filepath.replace('.png', '.json')
                                with open(metadata_path, 'w') as f:
                                    json.dump(metadata, f, indent=2)
                                
                                self.captured_count += 1
                                last_save_time = time.time()
                        
                        except Exception as e:
                            print(f"\n  Error en captura: {e}")
                    
                    time.sleep(0.1)  # Pequeña pausa para no saturar CPU
        
        except KeyboardInterrupt:
            print("\n\n  Captura interrumpida por usuario")
        
        finally:
            self.generate_session_report()
    
    def generate_session_report(self):
        """Generar reporte básico de la sesión"""
        report = {
            "session_id": self.session_id,
            "start_time": self.session_id,  # El ID contiene la fecha/hora
            "end_time": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "total_captures": self.captured_count,
            "session_folder": self.session_folder,
            "capture_settings": {
                "duration_seconds": "120",  # Podría ser configurable
                "interval_seconds": "2"
            }
        }
        
        report_path = os.path.join(self.session_folder, "reports", "session_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n\n REPORTE DE SESIÓN:")
        print(f"    Carpeta: {self.session_folder}")
        print(f"    Imágenes capturadas: {self.captured_count}")
        print(f"    Reporte: {report_path}")
        
        return report_path
    
    def continuous_capture_mode(self, duration_seconds=300, interval=1.5):
        """Modo de captura continua (alias para compatibilidad)"""
        self.simple_capture_mode(duration_seconds, interval)

# Función principal
def main():
    """Función principal del capturador"""
    print(" CAPTURADOR SIMPLIFICADO DE TEMPLATES")
    print("=" * 60)
    
    capturer = AutoTemplateCapturer()
    
    if not capturer.regions:
        print("  No hay configuración específica de PokerStars")
        print("   Usando pantalla completa...")
    
    print(" Capturador inicializado")
    print(f"   Sesión ID: {capturer.session_id}")
    
    # Iniciar captura (2 minutos por defecto)
    capturer.simple_capture_mode(duration_seconds=120, interval=2)

if __name__ == "__main__":
    main()
