"""
Archivo: stealth_capture.py
Ruta: src/screen_capture/stealth_capture.py
Sistema de captura de pantalla con técnicas anti-detección avanzadas
"""

import mss
import mss.tools
import numpy as np
from PIL import Image
import random
import time
import os
import sys
from datetime import datetime
from typing import Optional, Tuple, Dict, List
import ctypes
import win32gui
import win32ui
import win32con
import win32api

class StealthScreenCapture:
    """
    Sistema de captura de pantalla profesional con técnicas stealth
    Características:
    1. Rotación de métodos de captura
    2. Randomización de timings
    3. Comportamiento humano simulado
    4. Ofuscación de patrones
    5. Anti-detección de captura de pantalla
    """
    
    def __init__(self, platform: str = "ggpoker", stealth_level: str = "medium"):
        """
        Inicializar sistema de captura stealth
        
        Args:
            platform: Plataforma objetivo ("ggpoker" o "pokerstars")
            stealth_level: Nivel de stealth ("minimum", "medium", "maximum")
        """
        self.platform = platform.lower()
        self.stealth_level = stealth_level.lower()
        
        # Estadísticas y monitoreo
        self.capture_stats = {
            'total_captures': 0,
            'failed_captures': 0,
            'methods_used': {},
            'avg_capture_time': 0.0,
            'last_capture_time': 0.0
        }
        
        # Historial de capturas
        self.capture_history = []
        self.max_history_size = 50
        
        # Configuración de stealth según nivel
        self.stealth_config = self._load_stealth_config()
        
        # Inicializar métodos de captura disponibles
        self.available_methods = self._initialize_capture_methods()
        
        # Semilla aleatoria para randomización
        random.seed(time.time())
        
        print(f"[Stealth Capture] Inicializado para {self.platform.upper()}")
        print(f"[Stealth Capture] Nivel de stealth: {self.stealth_level.upper()}")
        
    def _load_stealth_config(self) -> Dict:
        """Cargar configuración de stealth según nivel"""
        
        config_templates = {
            "minimum": {
                "method_rotation": False,
                "random_delay": False,
                "delay_min": 0.5,
                "delay_max": 1.0,
                "human_behavior": False,
                "pattern_obfuscation": False,
                "max_captures_per_minute": 60
            },
            "medium": {
                "method_rotation": True,
                "random_delay": True,
                "delay_min": 1.0,
                "delay_max": 2.5,
                "human_behavior": True,
                "pattern_obfuscation": True,
                "max_captures_per_minute": 40
            },
            "maximum": {
                "method_rotation": True,
                "random_delay": True,
                "delay_min": 1.5,
                "delay_max": 4.0,
                "human_behavior": True,
                "pattern_obfuscation": True,
                "memory_obfuscation": True,
                "max_captures_per_minute": 25
            }
        }
        
        return config_templates.get(self.stealth_level, config_templates["medium"])
    
    def _initialize_capture_methods(self) -> Dict:
        """Inicializar todos los métodos de captura disponibles"""
        
        methods = {
            'mss': {
                'function': self._capture_mss,
                'weight': 0.4,
                'description': 'MSS (menos detectable)',
                'requires_admin': False
            },
            'windows_api': {
                'function': self._capture_windows_api,
                'weight': 0.3,
                'description': 'Windows API (nativo)',
                'requires_admin': False
            },
            'windows_api_indirect': {
                'function': self._capture_windows_api_indirect,
                'weight': 0.3,
                'description': 'Windows API indirecto',
                'requires_admin': False
            }
        }
        
        # Ajustar pesos según plataforma
        if self.platform == "pokerstars":
            # PokerStars es más agresivo, usar métodos más stealth
            methods['windows_api_indirect']['weight'] = 0.5
            methods['mss']['weight'] = 0.3
            methods['windows_api']['weight'] = 0.2
        
        return methods
    
    def capture(self, monitor: int = 1, region: Optional[Tuple] = None) -> Optional[Image.Image]:
        """
        Capturar pantalla con técnicas stealth
        
        Args:
            monitor: Número de monitor (0 = todos, 1 = primario)
            region: Tuple (left, top, width, height) para captura parcial
            
        Returns:
            PIL Image o None si falla
        """
        start_time = time.time()
        
        try:
            # 1. Aplicar delay aleatorio según configuración
            self._apply_random_delay()
            
            # 2. Seleccionar método de captura
            capture_method = self._select_capture_method()
            
            # 3. Aplicar técnicas de comportamiento humano
            if self.stealth_config.get('human_behavior', False):
                self._simulate_human_behavior()
            
            # 4. Ejecutar captura
            screenshot = capture_method(monitor, region)
            
            # 5. Aplicar ofuscación si está habilitada
            if screenshot and self.stealth_config.get('pattern_obfuscation', False):
                screenshot = self._apply_pattern_obfuscation(screenshot)
            
            # 6. Actualizar estadísticas
            capture_time = time.time() - start_time
            self._update_stats(capture_method.__name__, capture_time, success=True)
            
            return screenshot
            
        except Exception as e:
            capture_time = time.time() - start_time
            self._update_stats("unknown", capture_time, success=False)
            print(f"[Stealth Capture] Error en captura: {e}")
            
            # Intentar método de fallback
            try:
                return self._capture_fallback(monitor, region)
            except:
                return None
    
    def capture_window(self, window_title: str, exact_match: bool = True) -> Optional[Image.Image]:
        """
        Capturar ventana específica por título
        
        Args:
            window_title: Título de la ventana a capturar
            exact_match: Si requiere coincidencia exacta
            
        Returns:
            PIL Image de la ventana o None
        """
        try:
            # Encontrar ventana
            hwnd = self._find_window_by_title(window_title, exact_match)
            if not hwnd:
                print(f"[Stealth Capture] Ventana no encontrada: {window_title}")
                return None
            
            # Obtener dimensiones de la ventana
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            
            # Ajustar región para incluir bordes
            region = (left, top, width, height)
            
            # Capturar usando método stealth
            return self.capture(region=region)
            
        except Exception as e:
            print(f"[Stealth Capture] Error capturando ventana: {e}")
            return None
    
    def capture_poker_table(self) -> Optional[Image.Image]:
        """
        Capturar mesa de poker específica según plataforma
        
        Returns:
            PIL Image de la mesa de poker
        """
        # Definir nombres de ventana por plataforma
        window_patterns = {
            "ggpoker": ["GG Poker", "GGPoker", "GG"],
            "pokerstars": ["PokerStars", "Stars", "Poker"]
        }
        
        patterns = window_patterns.get(self.platform, [])
        
        for pattern in patterns:
            screenshot = self.capture_window(pattern, exact_match=False)
            if screenshot:
                print(f"[Stealth Capture] Mesa de {self.platform} capturada")
                return screenshot
        
        print(f"[Stealth Capture] No se encontró mesa de {self.platform}")
        return None
    
    def _select_capture_method(self):
        """Seleccionar método de captura basado en pesos y rotación"""
        
        if not self.stealth_config.get('method_rotation', True):
            # Usar método predeterminado si no hay rotación
            return self.available_methods['mss']['function']
        
        # Selección ponderada
        methods = list(self.available_methods.keys())
        weights = [self.available_methods[m]['weight'] for m in methods]
        
        selected_method = random.choices(methods, weights=weights, k=1)[0]
        
        return self.available_methods[selected_method]['function']
    
    def _apply_random_delay(self):
        """Aplicar delay aleatorio entre capturas"""
        
        if not self.stealth_config.get('random_delay', True):
            return
        
        # Calcular tiempo desde última captura
        time_since_last = time.time() - self.capture_stats.get('last_capture_time', 0)
        
        # Delay mínimo entre capturas
        min_delay = self.stealth_config.get('delay_min', 1.0)
        
        if time_since_last < min_delay:
            sleep_time = min_delay - time_since_last
            time.sleep(sleep_time)
        
        # Delay adicional aleatorio
        if random.random() < 0.3:  # 30% de probabilidad
            max_delay = self.stealth_config.get('delay_max', 2.5)
            extra_delay = random.uniform(0, max_delay - min_delay)
            
            # Sleep en pequeños incrementos para parecer humano
            increments = random.randint(3, 8)
            for _ in range(increments):
                time.sleep(extra_delay / increments)
                
                # Micro-pausas aleatorias
                if random.random() < 0.1:
                    time.sleep(random.uniform(0.01, 0.05))
    
    def _simulate_human_behavior(self):
        """Simular comportamiento humano aleatorio"""
        
        # Ocasionalmente mover el mouse aleatoriamente
        if random.random() < 0.05:  # 5% de probabilidad
            try:
                import pyautogui
                current_x, current_y = pyautogui.position()
                
                # Movimiento pequeño y natural
                move_x = current_x + random.randint(-20, 20)
                move_y = current_y + random.randint(-20, 20)
                
                # Duración humana (0.1-0.3 segundos)
                duration = random.uniform(0.1, 0.3)
                pyautogui.moveTo(move_x, move_y, duration=duration)
                
            except ImportError:
                pass  # PyAutoGUI no instalado
        
        # Pequeñas pausas aleatorias
        if random.random() < 0.1:  # 10% de probabilidad
            time.sleep(random.uniform(0.05, 0.15))
    
    def _apply_pattern_obfuscation(self, image: Image.Image) -> Image.Image:
        """Aplicar ofuscación de patrones a la imagen"""
        
        # Solo aplicar ocasionalmente
        if random.random() < 0.2:  # 20% de probabilidad
            
            # Método 1: Pequeñas variaciones de color
            if random.random() < 0.5:
                image = self._apply_color_variation(image)
            
            # Método 2: Compresión JPEG con calidad variable
            elif random.random() < 0.5:
                image = self._apply_jpeg_compression(image)
            
            # Método 3: Pequeño ruido aleatorio
            else:
                image = self._apply_random_noise(image)
        
        return image
    
    def _apply_color_variation(self, image: Image.Image) -> Image.Image:
        """Aplicar pequeñas variaciones de color"""
        img_array = np.array(image)
        
        # Variación mínima de color (±1-2 en cada canal)
        variation = random.randint(-2, 2)
        img_array = np.clip(img_array.astype(np.int16) + variation, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def _apply_jpeg_compression(self, image: Image.Image) -> Image.Image:
        """Aplicar compresión JPEG con calidad variable"""
        import io
        
        buffer = io.BytesIO()
        quality = random.randint(85, 98)  # Calidad variable
        
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        
        return Image.open(buffer)
    
    def _apply_random_noise(self, image: Image.Image) -> Image.Image:
        """Aplicar ruido aleatorio mínimo"""
        img_array = np.array(image)
        
        # Añadir ruido a un pequeño porcentaje de píxeles
        height, width = img_array.shape[:2]
        noise_pixels = int(height * width * 0.0001)  # 0.01% de píxeles
        
        for _ in range(noise_pixels):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            # Cambiar ligeramente el color
            if len(img_array.shape) == 3:  # Color
                for c in range(3):
                    img_array[y, x, c] = np.clip(img_array[y, x, c] + random.randint(-5, 5), 0, 255)
        
        return Image.fromarray(img_array)
    
    def _capture_mss(self, monitor: int = 1, region: Optional[Tuple] = None) -> Optional[Image.Image]:
        """Capturar usando MSS (menos detectable)"""
        try:
            with mss.mss() as sct:
                if region:
                    # Capturar región específica
                    monitor_dict = {
                        "left": region[0],
                        "top": region[1],
                        "width": region[2],
                        "height": region[3]
                    }
                else:
                    # Capturar monitor completo
                    monitor_dict = sct.monitors[monitor]
                
                # Capturar pantalla
                sct_img = sct.grab(monitor_dict)
                
                # Convertir a PIL Image
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                
                # Pequeña pausa para parecer humano
                if self.stealth_config.get('human_behavior', False):
                    time.sleep(random.uniform(0.01, 0.03))
                
                return img
                
        except Exception as e:
            print(f"[MSS Capture] Error: {e}")
            return None
    
    def _capture_windows_api(self, monitor: int = 1, region: Optional[Tuple] = None) -> Optional[Image.Image]:
        """Capturar usando Windows API (método nativo)"""
        try:
            if region:
                left, top, width, height = region
            else:
                # Capturar pantalla completa
                left = 0
                top = 0
                width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
                height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            
            # Obtener device context del escritorio
            hdesktop = win32gui.GetDesktopWindow()
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Crear bitmap compatible
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Copiar pantalla al bitmap
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
            
            # Convertir a formato PIL
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Limpiar handles
            mem_dc.DeleteDC()
            win32gui.DeleteObject(screenshot.GetHandle())
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            return img
            
        except Exception as e:
            print(f"[Windows API Capture] Error: {e}")
            return None
    
    def _capture_windows_api_indirect(self, monitor: int = 1, region: Optional[Tuple] = None) -> Optional[Image.Image]:
        """Captura indirecta usando Windows API (más stealth)"""
        
        # Pequeña pausa aleatoria
        time.sleep(random.uniform(0.05, 0.15))
        
        # Usar API estándar pero con variaciones
        return self._capture_windows_api(monitor, region)
    
    def _capture_fallback(self, monitor: int = 1, region: Optional[Tuple] = None) -> Optional[Image.Image]:
        """Método de fallback usando PIL (menos stealth)"""
        try:
            from PIL import ImageGrab
            
            if region:
                left, top, width, height = region
                bbox = (left, top, left + width, top + height)
                img = ImageGrab.grab(bbox=bbox)
            else:
                img = ImageGrab.grab()
            
            return img
            
        except Exception as e:
            print(f"[Fallback Capture] Error: {e}")
            return None
    
    def _find_window_by_title(self, title: str, exact_match: bool = True) -> Optional[int]:
        """Encontrar ventana por título"""
        
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:
                    if exact_match:
                        if window_title == title:
                            windows.append(hwnd)
                    else:
                        if title.lower() in window_title.lower():
                            windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        return windows[0] if windows else None
    
    def _update_stats(self, method_name: str, capture_time: float, success: bool = True):
        """Actualizar estadísticas de captura"""
        
        self.capture_stats['total_captures'] += 1
        
        if success:
            # Actualizar método usado
            method_key = method_name.replace('_capture_', '')
            self.capture_stats['methods_used'][method_key] = \
                self.capture_stats['methods_used'].get(method_key, 0) + 1
            
            # Actualizar tiempo promedio
            old_avg = self.capture_stats['avg_capture_time']
            self.capture_stats['avg_capture_time'] = \
                0.1 * capture_time + 0.9 * old_avg if old_avg > 0 else capture_time
        else:
            self.capture_stats['failed_captures'] += 1
        
        self.capture_stats['last_capture_time'] = time.time()
        
        # Guardar en historial
        self.capture_history.append({
            'timestamp': datetime.now().isoformat(),
            'method': method_name,
            'time': capture_time,
            'success': success
        })
        
        # Limitar tamaño del historial
        if len(self.capture_history) > self.max_history_size:
            self.capture_history = self.capture_history[-self.max_history_size:]
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas de captura"""
        
        total = self.capture_stats['total_captures']
        
        stats = {
            'total_captures': total,
            'failed_captures': self.capture_stats['failed_captures'],
            'success_rate': ((total - self.capture_stats['failed_captures']) / total * 100) if total > 0 else 0,
            'avg_capture_time_ms': self.capture_stats['avg_capture_time'] * 1000,
            'methods_used': self.capture_stats['methods_used'],
            'stealth_level': self.stealth_level,
            'platform': self.platform
        }
        
        return stats
    
    def get_detection_risk(self) -> str:
        """Obtener evaluación de riesgo de detección"""
        
        # Calcular tasa de captura por minuto
        if len(self.capture_history) >= 2:
            first_time = datetime.fromisoformat(self.capture_history[0]['timestamp'])
            last_time = datetime.fromisoformat(self.capture_history[-1]['timestamp'])
            time_diff = (last_time - first_time).total_seconds() / 60  # en minutos
            
            if time_diff > 0:
                captures_per_minute = len(self.capture_history) / time_diff
            else:
                captures_per_minute = 60
        else:
            captures_per_minute = 0
        
        # Evaluar riesgo
        max_allowed = self.stealth_config.get('max_captures_per_minute', 40)
        
        if captures_per_minute > max_allowed * 1.2:
            risk = "HIGH"
        elif captures_per_minute > max_allowed:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        
        return {
            'risk_level': risk,
            'captures_per_minute': captures_per_minute,
            'max_recommended': max_allowed,
            'recommendation': self._get_risk_recommendation(risk, captures_per_minute)
        }
    
    def _get_risk_recommendation(self, risk: str, captures_per_minute: float) -> str:
        """Obtener recomendación basada en riesgo"""
        
        if risk == "HIGH":
            return f"ALTO RIESGO: {captures_per_minute:.1f} capturas/minuto. Reducir frecuencia."
        elif risk == "MEDIUM":
            return f"RIESGO MODERADO: {captures_per_minute:.1f} capturas/minuto. Considerar reducir."
        else:
            return f"BAJO RIESGO: {captures_per_minute:.1f} capturas/minuto. Nivel seguro."

class AdaptiveRegionCapture:
    """
    Captura adaptativa de regiones específicas
    Para capturar solo áreas relevantes de la mesa de poker
    """
    
    def __init__(self, platform: str = "ggpoker"):
        self.platform = platform
        self.region_templates = self._load_region_templates()
        
    def _load_region_templates(self) -> Dict:
        """Cargar plantillas de regiones por plataforma"""
        
        # Coordenadas relativas (0-1) que se escalarán según resolución
        templates = {
            "ggpoker": {
                "hero_cards": {"x1": 0.45, "y1": 0.75, "x2": 0.55, "y2": 0.85},
                "board_cards": {"x1": 0.35, "y1": 0.45, "x2": 0.65, "y2": 0.55},
                "pot_amount": {"x1": 0.48, "y1": 0.40, "x2": 0.52, "y2": 0.44},
                "hero_stack": {"x1": 0.43, "y1": 0.82, "x2": 0.47, "y2": 0.86}
            },
            "pokerstars": {
                "hero_cards": {"x1": 0.47, "y1": 0.78, "x2": 0.53, "y2": 0.85},
                "board_cards": {"x1": 0.38, "y1": 0.48, "x2": 0.62, "y2": 0.55},
                "pot_amount": {"x1": 0.49, "y1": 0.42, "x2": 0.51, "y2": 0.45},
                "hero_stack": {"x1": 0.45, "y1": 0.80, "x2": 0.49, "y2": 0.84}
            }
        }
        
        return templates.get(self.platform, templates["ggpoker"])
    
    def get_region(self, region_name: str, screen_width: int, screen_height: int) -> Tuple:
        """
        Obtener coordenadas absolutas de una región
        
        Args:
            region_name: Nombre de la región (ej: "hero_cards")
            screen_width: Ancho de la pantalla en píxeles
            screen_height: Alto de la pantalla en píxeles
            
        Returns:
            Tuple (left, top, width, height)
        """
        
        if region_name not in self.region_templates:
            raise ValueError(f"Región desconocida: {region_name}")
        
        template = self.region_templates[region_name]
        
        # Convertir coordenadas relativas a absolutas
        left = int(template['x1'] * screen_width)
        top = int(template['y1'] * screen_height)
        right = int(template['x2'] * screen_width)
        bottom = int(template['y2'] * screen_height)
        
        width = right - left
        height = bottom - top
        
        return (left, top, width, height)
    
    def capture_region(self, capture_system: StealthScreenCapture, region_name: str) -> Optional[Image.Image]:
        """
        Capturar una región específica de la mesa
        
        Args:
            capture_system: Instancia de StealthScreenCapture
            region_name: Nombre de la región a capturar
            
        Returns:
            PIL Image de la región
        """
        try:
            # Obtener resolución de pantalla
            width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            
            # Obtener coordenadas de la región
            region = self.get_region(region_name, width, height)
            
            # Capturar región
            return capture_system.capture(region=region)
            
        except Exception as e:
            print(f"[Adaptive Capture] Error capturando región {region_name}: {e}")
            return None

# Función de utilidad para prueba rápida
def test_capture_system():
    """Probar el sistema de captura"""
    
    print("🧪 Probando sistema de captura stealth...")
    
    # Crear instancia
    capture = StealthScreenCapture(platform="ggpoker", stealth_level="medium")
    
    # Probar captura de pantalla completa
    print("📸 Capturando pantalla completa...")
    screenshot = capture.capture()
    
    if screenshot:
        print(f"✅ Captura exitosa: {screenshot.size}")
        
        # Guardar para inspección
        screenshot.save("test_capture.png")
        print("💾 Captura guardada como 'test_capture.png'")
        
        # Mostrar estadísticas
        stats = capture.get_stats()
        print(f"📊 Estadísticas: {stats}")
        
        # Evaluar riesgo
        risk = capture.get_detection_risk()
        print(f"⚠️  Riesgo de detección: {risk}")
    else:
        print("❌ Error en captura")
    
    # Probar captura de región específica
    print("\n🎴 Probando captura adaptativa de mesa...")
    adaptive = AdaptiveRegionCapture(platform="ggpoker")
    
    # Obtener resolución
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    print(f"🖥️  Resolución: {width}x{height}")
    
    # Mostrar regiones disponibles
    print("📍 Regiones disponibles:")
    for region_name in adaptive.region_templates.keys():
        coords = adaptive.get_region(region_name, width, height)
        print(f"  {region_name}: {coords}")
    
    return capture

if __name__ == "__main__":
    # Ejecutar prueba si se ejecuta directamente
    print("🚀 Iniciando prueba del sistema de captura")
    test_capture_system()