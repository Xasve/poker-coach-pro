# src/screen_capture/stealth_capture.py
import mss
import mss.tools
import time
import random
import numpy as np
import cv2

class StealthScreenCapture:
    def __init__(self, stealth_level=1, platform="pokerstars"):
        """
        Inicializador CORREGIDO - maneja correctamente los argumentos
        
        Args:
            stealth_level (int): Nivel de sigilo (1-3)
            platform (str): Plataforma ('pokerstars', 'ggpoker', etc.)
        """
        # 🔥 CORRECCIÓN: Asegurar que platform sea string
        self.platform = str(platform) if platform else "pokerstars"
        
        # Validar y convertir stealth_level
        if isinstance(stealth_level, str):
            try:
                self.stealth_level = int(stealth_level)
            except ValueError:
                self.stealth_level = 1
        else:
            self.stealth_level = int(stealth_level)
        
        # Limitar el rango de stealth_level
        self.stealth_level = max(1, min(3, self.stealth_level))
        
        # Configurar delays según nivel de sigilo
        self.capture_delays = {
            1: 0.1,    # Bajo sigilo - más rápido
            2: 0.3,    # Medio sigilo
            3: 0.5     # Alto sigilo - más lento
        }
        
        self.capture_delay = self.capture_delays.get(self.stealth_level, 0.1)
        
        # Nombres de niveles de sigilo
        stealth_names = {
            1: "BAJO",
            2: "MEDIO", 
            3: "ALTO"
        }
        
        print(f"🎯 StealthScreenCapture inicializado para {self.platform}")
        print(f"🔰 Nivel de sigilo: {stealth_names.get(self.stealth_level, 'BAJO')}")
        print(f"⚙️  Delay de captura: {self.capture_delay}s")
        
        # Inicializar MSS para captura de pantalla
        try:
            self.sct = mss.mss()
            print("✅ MSS inicializado correctamente")
        except Exception as e:
            print(f"⚠️  Error inicializando MSS: {e}")
            self.sct = None
    
    def capture_screen(self, region=None):
        """
        Capturar una región de la pantalla con delays aleatorios para sigilo
        
        Args:
            region (tuple): (left, top, width, height). Si es None, captura toda la pantalla.
            
        Returns:
            numpy.ndarray: Imagen en formato BGR, o None si hay error.
        """
        if self.sct is None:
            print("❌ MSS no está inicializado")
            return None
        
        try:
            # Aplicar delay sigiloso (con variación aleatoria)
            base_delay = self.capture_delay
            random_variation = random.uniform(-0.05, 0.1)
            actual_delay = max(0.05, base_delay + random_variation)
            time.sleep(actual_delay)
            
            # Determinar región a capturar
            if region is None:
                # Capturar pantalla completa
                monitor = self.sct.monitors[1]  # Monitor principal
                region_to_capture = {
                    "left": monitor["left"],
                    "top": monitor["top"],
                    "width": monitor["width"],
                    "height": monitor["height"]
                }
            else:
                left, top, width, height = region
                region_to_capture = {
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height
                }
            
            # Capturar pantalla
            screenshot = self.sct.grab(region_to_capture)
            
            # Convertir a numpy array (BGR para OpenCV)
            img_array = np.array(screenshot)
            
            # Convertir BGRA a BGR si es necesario
            if img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
            
            # 🔥 CORRECCIÓN: Guardar para debug si está habilitado
            if hasattr(self, 'debug_mode') and self.debug_mode:
                self._save_debug_capture(img_array)
            
            return img_array
            
        except Exception as e:
            print(f"❌ Error capturando pantalla: {e}")
            return None
    
    def capture_table_region(self):
        """Capturar la región donde se espera encontrar la mesa"""
        # Regiones por defecto para diferentes plataformas
        platform_regions = {
            "pokerstars": (0, 0, 1920, 1080),  # 1080p completo
            "ggpoker": (0, 0, 1920, 1080),
        }
        
        region = platform_regions.get(self.platform.lower(), (0, 0, 1920, 1080))
        return self.capture_screen(region)
    
    def _save_debug_capture(self, image):
        """Guardar captura para debugging"""
        import os
        from datetime import datetime
        
        debug_dir = "debug/captures"
        os.makedirs(debug_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{debug_dir}/capture_{self.platform}_{timestamp}.png"
        
        cv2.imwrite(filename, image)
        print(f"💾 Captura guardada para debug: {filename}")
    
    def set_stealth_level(self, level):
        """Cambiar nivel de sigilo dinámicamente"""
        old_level = self.stealth_level
        self.stealth_level = max(1, min(3, int(level)))
        self.capture_delay = self.capture_delays.get(self.stealth_level, 0.1)
        
        print(f"🔄 Nivel de sigilo cambiado: {old_level} → {self.stealth_level}")
        print(f"⚙️  Nuevo delay: {self.capture_delay}s")
    
    def get_capture_info(self):
        """Obtener información de configuración"""
        return {
            "platform": self.platform,
            "stealth_level": self.stealth_level,
            "capture_delay": self.capture_delay,
            "mss_initialized": self.sct is not None
        }