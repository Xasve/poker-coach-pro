"""
Archivo: stealth_capture.py
Ruta: src/screen_capture/stealth_capture.py
Captura de pantalla con técnicas stealth avanzadas
"""

import mss
import mss.tools
import numpy as np
from PIL import Image
import random
import time
import ctypes
import win32gui
import win32ui
import win32con
import win32api

class StealthScreenCapture:
    """
    Captura de pantalla con técnicas anti-detección
    """
    
    def __init__(self, platform="ggpoker"):
        self.platform = platform
        self.capture_method = self.choose_capture_method()
        self.capture_history = []
        self.last_capture_time = 0
        
        # Configuración de stealth
        self.stealth_config = {
            'method_rotation': True,
            'random_delay': True,
            'partial_capture': True,
            'color_variance': True,
            'compression_artifacts': True
        }
        
        # Inicializar métodos de captura
        self.init_capture_methods()
        
        # Estadísticas
        self.capture_stats = {
            'total_captures': 0,
            'method_used': {},
            'avg_capture_time': 0
        }
    
    def choose_capture_method(self):
        """Elegir método de captura basado en plataforma"""
        
        # Priorizar métodos menos detectables
        if self.platform == "pokerstars":
            # PokerStars es más agresivo, usar métodos indirectos
            return "windows_api_indirect"
        else:
            # GG Poker, usar métodos rotativos
            return "rotate"
    
    def init_capture_methods(self):
        """Inicializar todos los métodos de captura"""
        self.capture_methods = {
            'mss': self.capture_mss,
            'windows_api': self.capture_windows_api,
            'windows_api_indirect': self.capture_windows_api_indirect,
            'pil': self.capture_pil,
            'dxgi': self.capture_dxgi,
            'rotate': self.rotate_capture_methods
        }
    
    def capture(self, monitor=1, region=None):
        """
        Capturar pantalla con medidas stealth
        
        Args:
            monitor: Número de monitor (1 = primario)
            region: Tuple (left, top, width, height) para captura parcial
            
        Returns:
            PIL Image o None si falla
        """
        # Aplicar delay aleatorio
        if self.stealth_config['random_delay']:
            self.random_delay()
        
        # Rotar método si está configurado
        if self.stealth_config['method_rotation']:
            method = self.choose_rotated_method()
        else:
            method = self.capture_method
        
        # Registrar tiempo de inicio
        start_time = time.time()
        
        try:
            # Ejecutar captura
            screenshot = self.capture_methods[method](monitor, region)
            
            # Aplicar técnicas stealth a la imagen
            if screenshot and self.stealth_config['color_variance']:
                screenshot = self.apply_color_variance(screenshot)
            
            if screenshot and self.stealth_config['compression_artifacts']:
                screenshot = self.add_compression_artifacts(screenshot)
            
            # Actualizar estadísticas
            capture_time = time.time() - start_time
            self.update_stats(method, capture_time)
            
            # Guardar en historial (limitado)
            self.capture_history.append({
                'method': method,
                'time': capture_time,
                'timestamp': time.time()
            })
            
            # Limitar historial
            if len(self.capture_history) > 100:
                self.capture_history = self.capture_history[-100:]
            
            self.last_capture_time = time.time()
            return screenshot
            
        except Exception as e:
            print(f"[STEALTH CAPTURE] Error: {e}")
            
            # Fallback a método simple
            try:
                return self.capture_pil(monitor, region)
            except:
                return None
    
    def capture_mss(self, monitor=1, region=None):
        """Capturar usando MSS (menos detectable que PIL)"""
        with mss.mss() as sct:
            if region:
                monitor = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2],
                    "height": region[3]
                }
            else:
                monitor = sct.monitors[monitor]
            
            # Capturar
            sct_img = sct.grab(monitor)
            
            # Convertir a PIL
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            return img
    
    def capture_windows_api(self, monitor=1, region=None):
        """Capturar usando Windows API (método nativo)"""
        if region:
            left, top, width, height = region
        else:
            # Capturar pantalla completa
            left = 0
            top = 0
            width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        # Obtener device context
        hdesktop = win32gui.GetDesktopWindow()
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        mem_dc = img_dc.CreateCompatibleDC()
        
        # Crear bitmap
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)
        
        # Copiar pantalla
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
        
        # Convertir a formato usable
        bmpinfo = screenshot.GetInfo()
        bmpstr = screenshot.GetBitmapBits(True)
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        # Limpiar
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())
        win32gui.ReleaseDC(hdesktop, desktop_dc)
        
        return img
    
    def capture_windows_api_indirect(self, monitor=1, region=None):
        """Captura indirecta usando Windows API (más stealth)"""
        # Este método simula comportamiento de aplicaciones legítimas
        
        # Pequeña pausa para parecer humano
        time.sleep(random.uniform(0.05, 0.15))
        
        # Usar método estándar pero con variaciones
        return self.capture_windows_api(monitor, region)
    
    def capture_pil(self, monitor=1, region=None):
        """Captura simple con PIL (menos stealth)"""
        if region:
            left, top, width, height = region
            img = ImageGrab.grab(bbox=(left, top, left + width, top + height))
        else:
            img = ImageGrab.grab()
        
        return img
    
    def capture_dxgi(self, monitor=1, region=None):
        """Captura usando DirectX (para juegos)"""
        # Esto requiere pywin32 y acceso DirectX
        # Implementación simplificada
        
        try:
            import DXGI
            # Captura real requeriría setup de DXGI
            # Por ahora fallback a Windows API
            return self.capture_windows_api(monitor, region)
        except:
            return self.capture_mss(monitor, region)
    
    def rotate_capture_methods(self, monitor=1, region=None):
        """Rotar entre diferentes métodos de captura"""
        methods = ['mss', 'windows_api', 'windows_api_indirect']
        method = random.choice(methods)
        
        return self.capture_methods[method](monitor, region)
    
    def choose_rotated_method(self):
        """Elegir método de captura rotado"""
        weights = {
            'mss': 0.4,
            'windows_api': 0.3,
            'windows_api_indirect': 0.3
        }
        
        methods = list(weights.keys())
        probs = list(weights.values())
        
        return np.random.choice(methods, p=probs)
    
    def random_delay(self):
        """Agregar delay aleatorio entre capturas"""
        min_delay = 0.1  # 100ms
        max_delay = 0.5  # 500ms
        
        elapsed = time.time() - self.last_capture_time
        
        # Si la última captura fue muy reciente, esperar
        if elapsed < min_delay:
            time.sleep(min_delay - elapsed)
        
        # Delay adicional aleatorio
        if random.random() < 0.3:  # 30% de probabilidad
            extra_delay = random.uniform(0, max_delay - min_delay)
            time.sleep(extra_delay)
    
    def apply_color_variance(self, image):
        """Aplicar variaciones de color mínimas para evitar detección de patrones"""
        if random.random() < 0.2:  # 20% de probabilidad
            # Convertir a numpy array
            img_array = np.array(image)
            
            # Pequeñas variaciones de color
            variance = random.randint(-1, 1)
            img_array = np.clip(img_array + variance, 0, 255)
            
            # Convertir de vuelta a PIL
            return Image.fromarray(img_array.astype('uint8'))
        
        return image
    
    def add_compression_artifacts(self, image):
        """Agregar artefactos de compresión para parecer captura legítima"""
        if random.random() < 0.1:  # 10% de probabilidad
            # Guardar y cargar con compresión JPEG
            import io
            buffer = io.BytesIO()
            
            # Calidad aleatoria
            quality = random.randint(85, 95)
            image.save(buffer, format='JPEG', quality=quality)
            
            # Cargar de vuelta
            buffer.seek(0)
            return Image.open(buffer)
        
        return image
    
    def update_stats(self, method, capture_time):
        """Actualizar estadísticas de captura"""
        self.capture_stats['total_captures'] += 1
        self.capture_stats['method_used'][method] = \
            self.capture_stats['method_used'].get(method, 0) + 1
        
        # Promedio móvil de tiempo de captura
        alpha = 0.1  # Factor de suavizado
        old_avg = self.capture_stats['avg_capture_time']
        self.capture_stats['avg_capture_time'] = \
            alpha * capture_time + (1 - alpha) * old_avg
    
    def get_capture_stats(self):
        """Obtener estadísticas de captura"""
        return {
            'total_captures': self.capture_stats['total_captures'],
            'methods_used': self.capture_stats['method_used'],
            'avg_capture_time_ms': self.capture_stats['avg_capture_time'] * 1000,
            'history_size': len(self.capture_history),
            'last_capture_ago': time.time() - self.last_capture_time
        }
    
    def adaptive_capture_region(self, base_region):
        """Adaptar región de captura para evitar patrones"""
        if not self.stealth_config['partial_capture']:
            return base_region
        
        # Ocasionalmente cambiar ligeramente la región
        if random.random() < 0.15:  # 15% de probabilidad
            left, top, width, height = base_region
            
            # Pequeños ajustes aleatorios
            left += random.randint(-2, 2)
            top += random.randint(-2, 2)
            width += random.randint(-2, 2)
            height += random.randint(-2, 2)
            
            return (left, top, width, height)
        
        return base_region
    
    def stealth_capture_window(self, window_title):
        """Capturar ventana específica con técnicas stealth"""
        try:
            # Encontrar ventana
            hwnd = win32gui.FindWindow(None, window_title)
            if not hwnd:
                return None
            
            # Obtener posición y tamaño
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            
            # Adaptar región
            region = self.adaptive_capture_region((left, top, width, height))
            
            # Capturar
            return self.capture(region=region)
            
        except Exception as e:
            print(f"[STEALTH WINDOW CAPTURE] Error: {e}")
            return None