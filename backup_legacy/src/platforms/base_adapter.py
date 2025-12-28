"""
Archivo: base_adapter.py
Ruta: src/platforms/base_adapter.py
Clase base para adaptadores de plataformas de poker
"""

from abc import ABC, abstractmethod
import json
import os

class BasePokerAdapter(ABC):
    """Clase base abstracta para adaptadores de plataformas"""
    
    def __init__(self):
        self.platform = None
        self.config = {}
        self.last_state = None
    
    @abstractmethod
    def analyze_screenshot(self, screenshot):
        """Analizar screenshot y extraer estado del juego"""
        pass
    
    def get_default_game_state(self):
        """Obtener estado por defecto del juego"""
        return {
            'platform': self.platform,
            'hero_cards': [],
            'board_cards': [],
            'pot_size': 0.0,
            'bet_to_call': 0.0,
            'hero_stack': 100.0,
            'street': 'preflop',
            'position': 'BTN',
            'action_to_us': False,
            'buttons_visible': [],
            'stack_bb': 100.0,
            'timestamp': None
        }
    
    def validate_game_state(self, game_state):
        """Validar y limpiar el estado del juego"""
        
        # Validar tipos
        validated = {}
        
        for key, value in game_state.items():
            if key.endswith('_size') or key.endswith('_stack') or key == 'bet_to_call':
                try:
                    validated[key] = float(value)
                except:
                    validated[key] = 0.0
            elif key == 'hero_cards' or key == 'board_cards' or key == 'buttons_visible':
                if isinstance(value, list):
                    validated[key] = value
                else:
                    validated[key] = []
            elif key == 'street':
                if value in ['preflop', 'flop', 'turn', 'river']:
                    validated[key] = value
                else:
                    validated[key] = 'preflop'
            elif key == 'position':
                if value in ['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']:
                    validated[key] = value
                else:
                    validated[key] = 'BTN'
            elif key == 'action_to_us':
                validated[key] = bool(value)
            else:
                validated[key] = value
        
        # Asegurar campos mínimos
        default_state = self.get_default_game_state()
        for key in default_state:
            if key not in validated:
                validated[key] = default_state[key]
        
        return validated
    
    def save_hand_history(self, game_state, decision):
        """Guardar historial de mano"""
        if not os.path.exists('data/logs'):
            os.makedirs('data/logs', exist_ok=True)
        
        hand_data = {
            'game_state': game_state,
            'decision': decision,
            'platform': self.platform,
            'timestamp': game_state.get('timestamp')
        }
        
        filename = f"data/logs/hand_history_{self.platform}.json"
        
        try:
            # Cargar historial existente
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Agregar nueva mano
            history.append(hand_data)
            
            # Guardar (mantener últimas 1000 manos)
            if len(history) > 1000:
                history = history[-1000:]
            
            with open(filename, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def detect_anti_cheat_patterns(self, screenshot):
        """
        Detectar patrones anti-trampas
        
        Esta función es CRÍTICA para evitar detección
        """
        patterns = {
            'screen_capture': self.detect_screen_capture_tools,
            'overlay_detection': self.detect_overlay_windows,
            'process_monitoring': self.check_running_processes,
            'memory_scan': self.detect_memory_scanning
        }
        
        warnings = []
        
        for pattern_name, detector in patterns.items():
            try:
                if detector():
                    warnings.append(pattern_name)
            except:
                pass
        
        return warnings
    
    def detect_screen_capture_tools(self):
        """Detectar herramientas de captura de pantalla"""
        # Lista de procesos sospechosos
        suspicious_processes = [
            'fraps.exe', 'obs.exe', 'bandicam.exe',
            'nvidia_capture.exe', 'gamebar.exe',
            'capture.exe', 'screencap.exe'
        ]
        
        # En implementación real, verificaríamos procesos en ejecución
        # Por ahora, retornar False (no detectado)
        return False
    
    def detect_overlay_windows(self):
        """Detectar ventanas overlay sospechosas"""
        # Verificar si hay ventanas con atributos de overlay
        # que podrían ser detectadas por anti-cheat
        return False
    
    def check_running_processes(self):
        """Verificar procesos en ejecución"""
        # Implementación real verificaría blacklist de procesos
        return False
    
    def detect_memory_scanning(self):
        """Detectar escaneo de memoria"""
        # Verificar si hay herramientas de debugging o memory scanning
        return False
    
    def apply_stealth_measures(self):
        """Aplicar medidas de stealth para evitar detección"""
        
        measures = {
            'random_delays': self.add_random_delays,
            'human_like_patterns': self.simulate_human_patterns,
            'obfuscate_memory': self.obfuscate_memory_usage,
            'limit_capture_rate': self.limit_capture_rate
        }
        
        for measure_name, measure_func in measures.items():
            try:
                measure_func()
            except:
                pass
    
    def add_random_delays(self):
        """Agregar delays aleatorios para simular humano"""
        import time
        import random
        
        # Delay aleatorio entre 0.5 y 2 segundos
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
    
    def simulate_human_patterns(self):
        """Simular patrones humanos de interacción"""
        import pyautogui
        import random
        
        # Movimientos de mouse aleatorios ocasionales
        if random.random() < 0.01:  # 1% de probabilidad
            x, y = pyautogui.position()
            pyautogui.moveTo(x + random.randint(-10, 10),
                           y + random.randint(-10, 10),
                           duration=random.uniform(0.1, 0.3))
    
    def obfuscate_memory_usage(self):
        """Ofuscar uso de memoria"""
        # En implementación real, usaríamos técnicas para
        # ocultar el uso de memoria del proceso
        pass
    
    def limit_capture_rate(self):
        """Limitar tasa de captura para parecer humano"""
        # No capturar más de 1 vez por segundo
        import time
        if hasattr(self, 'last_capture'):
            elapsed = time.time() - self.last_capture
            if elapsed < 1.0:
                time.sleep(1.0 - elapsed)
        self.last_capture = time.time()
        