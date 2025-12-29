"""
DETECTOR OPTIMIZADO PARA POKERSTARS EN VIVO
Versión rápida para tiempo real
"""

import cv2
import numpy as np
import time
import os
from datetime import datetime

class PokerStarsLiveDetector:
    """Detector optimizado para PokerStars real"""
    
    def __init__(self):
        self.cache = {}
        self.last_scan_time = 0
        self.min_scan_interval = 0.5  # 500ms entre escaneos
        
        # Plantillas pre-cargadas
        self.card_templates = self.load_card_templates()
        self.button_templates = self.load_button_templates()
        
        # Regiones predefinidas (se ajustan en calibración)
        self.regions = {
            'hero_cards': (700, 800, 200, 100),  # Ajustar según resolución
            'flop': (600, 400, 300, 100),
            'turn': (650, 400, 50, 100),
            'river': (700, 400, 50, 100),
            'fold_button': (900, 700, 100, 50),
            'call_button': (1000, 700, 100, 50),
            'raise_button': (1100, 700, 100, 50)
        }
        
    def load_card_templates(self):
        """Cargar plantillas de cartas desde archivos"""
        templates = {}
        template_dir = os.path.join('data', 'card_templates')
        
        if not os.path.exists(template_dir):
            print(f"⚠️  Directorio de plantillas no encontrado: {template_dir}")
            return templates
        
        # Cargar cartas de ejemplo
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        for suit in suits:
            for rank in ranks:
                filename = f"{rank}_{suit}.png"
                filepath = os.path.join(template_dir, filename)
                
                if os.path.exists(filepath):
                    template = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                    if template is not None:
                        key = f"{rank}{suit[0].upper()}"
                        templates[key] = template
        
        print(f"📁 Cargadas {len(templates)} plantillas de cartas")
        return templates
    
    def load_button_templates(self):
        """Cargar plantillas de botones"""
        buttons = {}
        # Estos son placeholders - en realidad deberían ser capturas de botones reales
        return buttons
    
    def calibrate(self, screenshot):
        """Calibrar detector con screenshot actual"""
        print("🔧 Calibrando detector...")
        
        height, width = screenshot.shape[:2]
        print(f"📏 Resolución detectada: {width}x{height}")
        
        # Ajustar regiones según resolución
        if width == 1920 and height == 1080:  # 1080p
            self.regions = {
                'hero_cards': (800, 850, 150, 80),
                'flop': (650, 450, 250, 80),
                'turn': (750, 450, 50, 80),
                'river': (800, 450, 50, 80),
                'fold_button': (850, 750, 80, 40),
                'call_button': (950, 750, 80, 40),
                'raise_button': (1050, 750, 80, 40)
            }
        elif width == 1280 and height == 720:  # 720p
            self.regions = {
                'hero_cards': (550, 600, 120, 60),
                'flop': (450, 300, 180, 60),
                'turn': (520, 300, 40, 60),
                'river': (560, 300, 40, 60),
                'fold_button': (600, 500, 60, 30),
                'call_button': (680, 500, 60, 30),
                'raise_button': (760, 500, 60, 30)
            }
        
        print("✅ Calibración básica completada")
        return True
    
    def detect_game_state(self, screenshot):
        """Detectar estado actual del juego"""
        current_time = time.time()
        
        # Evitar escaneos muy frecuentes
        if current_time - self.last_scan_time < self.min_scan_interval:
            # Usar cache si está disponible
            if 'last_state' in self.cache:
                return self.cache['last_state']
        
        self.last_scan_time = current_time
        
        # Convertir a escala de grises para procesamiento más rápido
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Detectar fase del juego (simplificado)
        game_phase = self.detect_game_phase(gray)
        
        # Detectar si es nuestro turno
        is_our_turn = self.detect_our_turn(gray)
        
        # Detectar acciones disponibles
        available_actions = self.detect_available_actions(gray)
        
        state = {
            "game_phase": game_phase,
            "is_our_turn": is_our_turn,
            "available_actions": available_actions,
            "timestamp": datetime.now().isoformat()
        }
        
        # Guardar en cache
        self.cache['last_state'] = state
        
        return state
    
    def detect_game_phase(self, gray_image):
        """Detectar fase del juego basado en posición de cartas"""
        # Región de las cartas comunitarias
        flop_region = self.get_region('flop', gray_image)
        
        # Analizar intensidad de píxeles para determinar si hay cartas
        flop_mean = np.mean(flop_region)
        
        if flop_mean > 200:  # Muy claro, probablemente no hay cartas
            return "PREFLOP"
        elif flop_mean > 100:  # Mediano, podría haber cartas
            # Verificar más detalladamente
            return self.refine_game_phase(gray_image)
        else:
            return "POSTFLOP"  # Oscuro, probablemente hay cartas
    
    def refine_game_phase(self, gray_image):
        """Refinar detección de fase del juego"""
        # Verificar cada posición de carta comunitaria
        regions_to_check = ['flop', 'turn', 'river']
        card_count = 0
        
        for region_name in regions_to_check:
            region = self.get_region(region_name, gray_image)
            # Detección simple basada en contraste
            if np.std(region) > 25:  # Hay variación, probablemente una carta
                card_count += 1
        
        if card_count == 0:
            return "PREFLOP"
        elif card_count == 3:
            return "FLOP"
        elif card_count == 4:
            return "TURN"
        elif card_count == 5:
            return "RIVER"
        else:
            return "UNKNOWN"
    
    def detect_our_turn(self, gray_image):
        """Detectar si es nuestro turno"""
        # Verificar si hay botones de acción visibles
        action_regions = ['fold_button', 'call_button', 'raise_button']
        
        for region_name in action_regions:
            region = self.get_region(region_name, gray_image)
            # Los botones suelen ser más brillantes cuando están activos
            if np.mean(region) > 150:  # Umbral empírico
                return True
        
        return False
    
    def detect_available_actions(self, gray_image):
        """Detectar qué acciones están disponibles"""
        actions = []
        
        # Mapeo región -> acción
        action_map = {
            'fold_button': 'FOLD',
            'call_button': 'CALL', 
            'raise_button': 'RAISE'
        }
        
        for region_name, action in action_map.items():
            region = self.get_region(region_name, gray_image)
            if np.mean(region) > 150:  # Botón visible/activo
                actions.append(action)
        
        return actions
    
    def detect_hero_cards(self, screenshot):
        """Detectar cartas del jugador (hero)"""
        # Usar región predefinida
        card_region = self.get_region('hero_cards', screenshot)
        
        # Para MVP, retornar placeholder
        # EN PRÓXIMAS ITERACIONES: implementar OCR real aquí
        return ["??", "??"]
    
    def detect_board_cards(self, screenshot):
        """Detectar cartas comunitarias"""
        board_cards = []
        
        # Verificar cada posición
        phase_regions = {
            'FLOP': ['flop'],
            'TURN': ['flop', 'turn'],
            'RIVER': ['flop', 'turn', 'river']
        }
        
        # Para MVP, placeholder
        # EN PRÓXIMAS ITERACIONES: implementar detección real
        return []
    
    def get_region(self, region_name, image):
        """Obtener región de la imagen"""
        if region_name not in self.regions:
            raise ValueError(f"Región desconocida: {region_name}")
        
        x, y, w, h = self.regions[region_name]
        
        # Asegurar que la región está dentro de los límites
        img_height, img_width = image.shape[:2]
        x = max(0, min(x, img_width - 1))
        y = max(0, min(y, img_height - 1))
        w = min(w, img_width - x)
        h = min(h, img_height - y)
        
        return image[y:y+h, x:x+w]
    
    def save_region_for_debug(self, region, region_name):
        """Guardar región para debugging"""
        debug_dir = "debug_regions"
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{debug_dir}/{region_name}_{timestamp}.png"
        cv2.imwrite(filename, region)