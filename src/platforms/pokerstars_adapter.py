"""
Archivo: pokerstars_adapter.py
Ruta: src/platforms/pokerstars_adapter.py
Adaptador específico para PokerStars
"""

import cv2
import numpy as np
from PIL import Image, ImageGrab
import pytesseract
import re
from datetime import datetime
import os
import json

from .base_adapter import BasePokerAdapter

class PokerStarsAdapter(BasePokerAdapter):
    """Adaptador específico para PokerStars"""
    
    def __init__(self):
        super().__init__()
        self.platform = "pokerstars"
        
        # Cargar configuración específica
        self.load_pokerstars_config()
        
        # Áreas de captura específicas de PokerStars
        self.setup_pokerstars_areas()
        
        # Patrones específicos de PokerStars
        self.setup_pokerstars_patterns()
        
        # PokerStars tiene detección más agresiva
        self.anti_detection_level = "HIGH"
    
    def load_pokerstars_config(self):
        """Cargar configuración de PokerStars"""
        config_path = os.path.join("config", "pokerstars_config.json")
        try:
            with open(config_path, 'r') as f:
                self.ps_config = json.load(f)
        except:
            self.ps_config = {}
    
    def setup_pokerstars_areas(self):
        """Configurar áreas de captura específicas de PokerStars"""
        
        # PokerStars tiene interfaz diferente
        self.areas = {
            'hero_cards': {'x1': 0.47, 'y1': 0.78, 'x2': 0.53, 'y2': 0.85},
            'board_cards': {'x1': 0.38, 'y1': 0.48, 'x2': 0.62, 'y2': 0.55},
            'pot_amount': {'x1': 0.49, 'y1': 0.42, 'x2': 0.51, 'y2': 0.45},
            'hero_stack': {'x1': 0.45, 'y1': 0.80, 'x2': 0.49, 'y2': 0.84},
            'bet_to_call': {'x1': 0.51, 'y1': 0.62, 'x2': 0.55, 'y2': 0.66},
            'action_buttons': {'x1': 0.42, 'y1': 0.68, 'x2': 0.58, 'y2': 0.74},
            'player_positions': {
                'hero': {'x': 0.50, 'y': 0.82},
                'btn': {'x': 0.50, 'y': 0.58},
                'sb': {'x': 0.42, 'y': 0.65},
                'bb': {'x': 0.58, 'y': 0.65}
            },
            'table_identifier': {'x1': 0.02, 'y1': 0.02, 'x2': 0.10, 'y2': 0.05}
        }
    
    def setup_pokerstars_patterns(self):
        """Configurar patrones específicos de PokerStars"""
        
        # PokerStars usa colores diferentes
        self.colors = {
            'button_color': (255, 153, 0),  # Naranja PokerStars
            'hero_highlight': (0, 102, 204),  # Azul
            'bet_color': (255, 255, 255),     # Blanco
            'fold_color': (153, 153, 153),    # Gris
            'raise_color': (204, 0, 0),       # Rojo
            'call_color': (255, 102, 0)       # Naranja
        }
        
        # Patrones de texto PokerStars
        self.patterns = {
            'pot': r'Total pot:?\s*([\d,\.]+)',
            'bet': r'Bet:?\s*([\d,\.]+)',
            'raise': r'Raise to:?\s*([\d,\.]+)',
            'call': r'Call:?\s*([\d,\.]+)',
            'all_in': r'All[\-\s]*In',
            'check': r'Check',
            'fold': r'Fold'
        }
    
    def analyze_screenshot(self, screenshot):
        """
        Analizar screenshot específico de PokerStars
        
        Args:
            screenshot: Imagen PIL de la pantalla
            
        Returns:
            Dict con estado del juego
        """
        # PokerStars tiene detección agresiva, ser más cuidadoso
        self.apply_pokerstars_stealth()
        
        if screenshot is None:
            return self.get_default_game_state()
        
        try:
            # Convertir a OpenCV
            cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Obtener dimensiones
            height, width = cv_image.shape[:2]
            
            # Verificar que sea PokerStars (no captura incorrecta)
            if not self.is_valid_pokerstars_table(cv_image, width, height):
                print("[POKERSTARS] Tabla no reconocida")
                return self.get_default_game_state()
            
            # Analizar componentes
            game_state = {
                'platform': 'pokerstars',
                'timestamp': datetime.now().isoformat(),
                'table_id': self.detect_table_id(cv_image, width, height),
                'hero_cards': self.detect_hero_cards(cv_image, width, height),
                'board_cards': self.detect_board_cards(cv_image, width, height),
                'pot_size': self.detect_pot_size(cv_image, width, height),
                'bet_to_call': self.detect_bet_to_call(cv_image, width, height),
                'hero_stack': self.detect_hero_stack(cv_image, width, height),
                'street': self.detect_street(cv_image, width, height),
                'position': self.detect_position(cv_image, width, height),
                'action_to_us': self.detect_action_to_us(cv_image, width, height),
                'buttons_visible': self.detect_action_buttons(cv_image, width, height),
                'zoom_table': self.is_zoom_table(cv_image, width, height)
            }
            
            # Calcular stack en BB
            if game_state['hero_stack'] and game_state.get('bet_to_call', 0) > 0:
                game_state['stack_bb'] = game_state['hero_stack'] / game_state['bet_to_call']
            else:
                game_state['stack_bb'] = 100
            
            # Validar estado
            game_state = self.validate_game_state(game_state)
            
            # PokerStars específico: ajustar por tipo de mesa
            if game_state['zoom_table']:
                game_state = self.adjust_for_zoom_table(game_state)
            
            return game_state
            
        except Exception as e:
            print(f"Error analizando PokerStars: {e}")
            return self.get_default_game_state()
    
    def is_valid_pokerstars_table(self, cv_image, width, height):
        """Verificar que la captura sea de PokerStars"""
        
        # Verificar área de identificación
        area = self.areas['table_identifier']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        identifier_area = cv_image[y1:y2, x1:x2]
        
        # Convertir a texto
        text = self.ocr_region(identifier_area)
        
        # Buscar indicadores de PokerStars
        pokerstars_indicators = ['pokerstars', 'stars', 'ps', 'table']
        text_lower = text.lower()
        
        return any(indicator in text_lower for indicator in pokerstars_indicators)
    
    def detect_table_id(self, cv_image, width, height):
        """Detectar ID de mesa PokerStars"""
        area = self.areas['table_identifier']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        id_area = cv_image[y1:y2, x1:x2]
        text = self.ocr_region(id_area)
        
        # Extraer números de mesa
        match = re.search(r'#(\d+)', text)
        if match:
            return match.group(1)
        
        return "UNKNOWN"
    
    def detect_hero_cards(self, cv_image, width, height):
        """Detectar cartas del héroe en PokerStars"""
        area = self.areas['hero_cards']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        card_area = cv_image[y1:y2, x1:x2]
        
        # PokerStars tiene diseño específico de cartas
        # Dividir en dos cartas
        card_width = (x2 - x1) // 2
        
        # Simular detección
        return ['Ah', 'Kd']  # Placeholder
    
    def detect_board_cards(self, cv_image, width, height):
        """Detectar cartas comunitarias PokerStars"""
        area = self.areas['board_cards']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        # Determinar street
        street = self.detect_street(cv_image, width, height)
        
        if street == 'preflop':
            return []
        elif street == 'flop':
            return ['2h', '7d', 'Ts']
        elif street == 'turn':
            return ['2h', '7d', 'Ts', 'Qc']
        elif street == 'river':
            return ['2h', '7d', 'Ts', 'Qc', 'Kd']
        
        return []
    
    def detect_pot_size(self, cv_image, width, height):
        """Detectar tamaño del pozo PokerStars"""
        area = self.areas['pot_amount']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        pot_area = cv_image[y1:y2, x1:x2]
        
        # Preprocesar para mejor OCR (PokerStars fondo verde)
        # Convertir a HSV para separar texto
        hsv = cv2.cvtColor(pot_area, cv2.COLOR_BGR2HSV)
        
        # Buscar texto blanco/amarillo
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # OCR en área de máscara
        text = pytesseract.image_to_string(mask, config='--psm 7')
        
        # Extraer número
        match = re.search(r'([\d,\.]+)', text)
        if match:
            try:
                amount = match.group(1).replace(',', '')
                return float(amount)
            except:
                pass
        
        return 0.0
    
    def detect_bet_to_call(self, cv_image, width, height):
        """Detectar apuesta a pagar en PokerStars"""
        # Primero verificar botones
        buttons = self.detect_action_buttons(cv_image, width, height)
        
        for button in buttons:
            if 'call' in button.lower():
                # Extraer cantidad
                match = re.search(r'([\d,\.]+)', button)
                if match:
                    try:
                        amount = match.group(1).replace(',', '')
                        return float(amount)
                    except:
                        pass
        
        # Intentar detectar en área de bet
        area = self.areas['bet_to_call']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        bet_area = cv_image[y1:y2, x1:x2]
        text = self.ocr_region(bet_area)
        
        match = re.search(r'([\d,\.]+)', text)
        if match:
            try:
                amount = match.group(1).replace(',', '')
                return float(amount)
            except:
                pass
        
        return 0.0
    
    def detect_action_buttons(self, cv_image, width, height):
        """Detectar botones de acción PokerStars"""
        area = self.areas['action_buttons']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        buttons_area = cv_image[y1:y2, x1:x2]
        
        # PokerStars tiene colores específicos para botones
        detected = []
        
        # Buscar por colores
        color_ranges = [
            (np.array([0, 100, 200]), np.array([10, 255, 255]), 'raise'),  # Rojo
            (np.array([15, 100, 200]), np.array([25, 255, 255]), 'call'),  # Naranja
            (np.array([0, 0, 100]), np.array([180, 50, 150]), 'fold'),     # Gris
            (np.array([40, 100, 200]), np.array([80, 255, 255]), 'check'), # Verde
        ]
        
        hsv = cv2.cvtColor(buttons_area, cv2.COLOR_BGR2HSV)
        
        for lower, upper, action in color_ranges:
            mask = cv2.inRange(hsv, lower, upper)
            if cv2.countNonZero(mask) > 100:
                detected.append(action)
        
        return detected
    
    def is_zoom_table(self, cv_image, width, height):
        """Detectar si es mesa Zoom/PokerStars Speed"""
        # Zoom tables tienen indicadores específicos
        # Verificar área de nombre de mesa
        area = self.areas['table_identifier']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        id_area = cv_image[y1:y2, x1:x2]
        text = self.ocr_region(id_area).lower()
        
        zoom_indicators = ['zoom', 'speed', 'fast', 'blast']
        
        return any(indicator in text for indicator in zoom_indicators)
    
    def adjust_for_zoom_table(self, game_state):
        """Ajustar estrategia para mesas Zoom"""
        # En Zoom, jugar más tight
        adjusted = game_state.copy()
        
        if adjusted.get('street') == 'preflop':
            # Ajustar rangos
            pass
        
        return adjusted
    
    def apply_pokerstars_stealth(self):
        """Aplicar medidas de stealth específicas para PokerStars"""
        # PokerStars tiene mejor detección, ser más cuidadoso
        
        # 1. Randomizar tiempos más
        import time
        time.sleep(random.uniform(0.2, 0.8))
        
        # 2. Variar patrones de captura
        if random.random() < 0.1:
            # Ocasionalmente saltar una captura
            pass
        
        # 3. Limitar frecuencia
        current_time = time.time()
        if hasattr(self, 'last_capture_time'):
            elapsed = current_time - self.last_capture_time
            if elapsed < 1.5:  # No capturar más de cada 1.5s
                time.sleep(1.5 - elapsed)
        
        self.last_capture_time = current_time
    
    def ocr_region(self, image_area):
        """OCR optimizado para PokerStars"""
        try:
            # PokerStars tiene fondos verdes, ajustar preprocesamiento
            pil_image = Image.fromarray(cv2.cvtColor(image_area, cv2.COLOR_BGR2RGB))
            
            # Convertir a escala de grises
            gray = pil_image.convert('L')
            
            # Aumentar contraste
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(gray)
            enhanced = enhancer.enhance(2.0)
            
            # Binarizar
            threshold = enhanced.point(lambda x: 0 if x < 200 else 255)
            
            # OCR con configuración específica
            text = pytesseract.image_to_string(
                threshold, 
                config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789$,.#PokerStarsTable'
            )
            
            return text.strip()
            
        except Exception as e:
            print(f"OCR error: {e}")
            return ""