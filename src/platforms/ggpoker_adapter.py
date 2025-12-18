
#Archivo: ggpoker_adapter.py
#Ruta: src/platforms/ggpoker_adapter.py
#Adaptador específico para GG Poker


import cv2
import numpy as np
from PIL import Image, ImageGrab
import pytesseract
import re
from datetime import datetime
import os
import json

from .base_adapter import BasePokerAdapter

class GGPokerAdapter(BasePokerAdapter):
    """Adaptador específico para GG Poker"""
    
    def __init__(self):
        super().__init__()
        self.platform = "ggpoker"
        
        # Cargar configuración específica
        self.load_ggpoker_config()
        
        # Áreas de captura específicas de GG Poker
        self.setup_ggpoker_areas()
        
        # Patrones específicos de GG Poker
        self.setup_ggpoker_patterns()
    
    def load_ggpoker_config(self):
        """Cargar configuración de GG Poker"""
        config_path = os.path.join("config", "ggpoker_config.json")
        try:
            with open(config_path, 'r') as f:
                self.gg_config = json.load(f)
        except:
            self.gg_config = {}
    
    def setup_ggpoker_areas(self):
        """Configurar áreas de captura específicas de GG Poker"""
        
        # Coordenadas relativas (se ajustan en tiempo de ejecución)
        self.areas = {
            'hero_cards': {'x1': 0.45, 'y1': 0.75, 'x2': 0.55, 'y2': 0.85},
            'board_cards': {'x1': 0.35, 'y1': 0.45, 'x2': 0.65, 'y2': 0.55},
            'pot_amount': {'x1': 0.48, 'y1': 0.40, 'x2': 0.52, 'y2': 0.44},
            'hero_stack': {'x1': 0.43, 'y1': 0.82, 'x2': 0.47, 'y2': 0.86},
            'bet_to_call': {'x1': 0.52, 'y1': 0.60, 'x2': 0.56, 'y2': 0.64},
            'action_buttons': {'x1': 0.40, 'y1': 0.65, 'x2': 0.60, 'y2': 0.75},
            'player_positions': {
                'hero': {'x': 0.50, 'y': 0.80},
                'btn': {'x': 0.50, 'y': 0.60},
                'sb': {'x': 0.40, 'y': 0.65},
                'bb': {'x': 0.60, 'y': 0.65}
            }
        }
    
    def setup_ggpoker_patterns(self):
        """Configurar patrones específicos de GG Poker"""
        
        # Patrones de texto GG Poker
        self.patterns = {
            'pot': r'Pot:\s*([\d,\.]+)',
            'bet': r'Bet:\s*([\d,\.]+)',
            'raise': r'Raise to:\s*([\d,\.]+)',
            'call': r'Call:\s*([\d,\.]+)',
            'all_in': r'ALL IN',
            'check': r'CHECK',
            'fold': r'FOLD'
        }
        
        # Colores específicos de GG Poker
        self.colors = {
            'button_color': (255, 215, 0),  # Dorado GG
            'hero_highlight': (0, 100, 255),  # Azul
            'bet_color': (255, 255, 255),     # Blanco
            'fold_color': (128, 128, 128)     # Gris
        }
    
    def analyze_screenshot(self, screenshot):
        """
        Analizar screenshot específico de GG Poker
        
        Args:
            screenshot: Imagen PIL de la pantalla
            
        Returns:
            Dict con estado del juego
        """
        if screenshot is None:
            return self.get_default_game_state()
        
        try:
            # Convertir a OpenCV
            cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Obtener dimensiones
            height, width = cv_image.shape[:2]
            
            # Analizar diferentes componentes
            game_state = {
                'platform': 'ggpoker',
                'timestamp': datetime.now().isoformat(),
                'hero_cards': self.detect_hero_cards(cv_image, width, height),
                'board_cards': self.detect_board_cards(cv_image, width, height),
                'pot_size': self.detect_pot_size(cv_image, width, height),
                'bet_to_call': self.detect_bet_to_call(cv_image, width, height),
                'hero_stack': self.detect_hero_stack(cv_image, width, height),
                'street': self.detect_street(cv_image, width, height),
                'position': self.detect_position(cv_image, width, height),
                'action_to_us': self.detect_action_to_us(cv_image, width, height),
                'buttons_visible': self.detect_action_buttons(cv_image, width, height)
            }
            
            # Calcular stack en BB
            if game_state['hero_stack'] and game_state.get('bet_to_call', 0) > 0:
                game_state['stack_bb'] = game_state['hero_stack'] / game_state['bet_to_call']
            else:
                game_state['stack_bb'] = 100  # Valor por defecto
            
            # Validar y limpiar estado
            game_state = self.validate_game_state(game_state)
            
            return game_state
            
        except Exception as e:
            print(f"Error analizando GG Poker: {e}")
            return self.get_default_game_state()
    
    def detect_hero_cards(self, cv_image, width, height):
        """Detectar cartas del héroe en GG Poker"""
        area = self.areas['hero_cards']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        # Recortar área de cartas
        card_area = cv_image[y1:y2, x1:x2]
        
        # Buscar patrones de cartas (simplificado)
        # En implementación real usaríamos template matching
        cards = []
        
        # Dividir área en dos cartas
        card_width = (x2 - x1) // 2
        
        # Simular detección para desarrollo
        return ['Ah', 'Kd']  # Placeholder
    
    def detect_board_cards(self, cv_image, width, height):
        """Detectar cartas comunitarias"""
        area = self.areas['board_cards']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        board_area = cv_image[y1:y2, x1:x2]
        
        # Determinar número de cartas según street
        street = self.detect_street(cv_image, width, height)
        
        if street == 'preflop':
            return []
        elif street == 'flop':
            return ['2h', '7d', 'Ts']  # Placeholder
        elif street == 'turn':
            return ['2h', '7d', 'Ts', 'Qc']
        elif street == 'river':
            return ['2h', '7d', 'Ts', 'Qc', 'Kd']
        
        return []
    
    def detect_pot_size(self, cv_image, width, height):
        """Detectar tamaño del pozo"""
        area = self.areas['pot_amount']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        pot_area = cv_image[y1:y2, x1:x2]
        
        # Usar OCR para leer el texto
        pot_text = self.ocr_region(pot_area)
        
        # Extraer número
        match = re.search(r'([\d,\.]+)', pot_text)
        if match:
            try:
                # Limpiar y convertir
                amount = match.group(1).replace(',', '')
                return float(amount)
            except:
                pass
        
        return 0.0
    
    def detect_bet_to_call(self, cv_image, width, height):
        """Detectar apuesta a pagar"""
        area = self.areas['bet_to_call']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        bet_area = cv_image[y1:y2, x1:x2]
        
        # Verificar botones de acción primero
        action_buttons = self.detect_action_buttons(cv_image, width, height)
        
        for button in action_buttons:
            if 'call' in button.lower():
                # Extraer cantidad del texto del botón
                match = re.search(r'([\d,\.]+)', button)
                if match:
                    try:
                        amount = match.group(1).replace(',', '')
                        return float(amount)
                    except:
                        pass
        
        return 0.0
    
    def detect_hero_stack(self, cv_image, width, height):
        """Detectar stack del héroe"""
        area = self.areas['hero_stack']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        stack_area = cv_image[y1:y2, x1:x2]
        
        # OCR para stack
        stack_text = self.ocr_region(stack_area)
        
        match = re.search(r'([\d,\.]+)', stack_text)
        if match:
            try:
                amount = match.group(1).replace(',', '')
                return float(amount)
            except:
                pass
        
        return 100.0  # Valor por defecto
    
    def detect_street(self, cv_image, width, height):
        """Detectar calle actual (preflop, flop, turn, river)"""
        
        # Basado en número de cartas comunitarias visibles
        board_cards = self.detect_board_cards(cv_image, width, height)
        
        if len(board_cards) == 0:
            return 'preflop'
        elif len(board_cards) == 3:
            return 'flop'
        elif len(board_cards) == 4:
            return 'turn'
        elif len(board_cards) == 5:
            return 'river'
        
        return 'preflop'
    
    def detect_position(self, cv_image, width, height):
        """Detectar posición del héroe"""
        
        # Analizar posición del botón
        btn_area = self.areas['player_positions']['btn']
        btn_x = int(width * btn_area['x'])
        btn_y = int(height * btn_area['y'])
        
        # Obtener color en posición del botón
        btn_color = cv_image[btn_y, btn_x]
        
        # Verificar si es el botón (color dorado GG Poker)
        if self.is_button_color(btn_color):
            return 'BTN'
        
        # Lógica simplificada
        return 'BTN'  # Placeholder
    
    def detect_action_to_us(self, cv_image, width, height):
        """Detectar si hay acción para nosotros"""
        
        # Verificar botones visibles
        buttons = self.detect_action_buttons(cv_image, width, height)
        
        if buttons:
            return True
        
        return False
    
    def detect_action_buttons(self, cv_image, width, height):
        """Detectar botones de acción visibles"""
        area = self.areas['action_buttons']
        x1 = int(width * area['x1'])
        y1 = int(height * area['y1'])
        x2 = int(width * area['x2'])
        y2 = int(height * area['y2'])
        
        buttons_area = cv_image[y1:y2, x1:x2]
        
        # Detectar colores de botones específicos de GG Poker
        button_colors = [
            ((200, 0, 0), 'raise'),    # Rojo para raise
            ((255, 165, 0), 'call'),   # Naranja para call
            ((128, 128, 128), 'fold'), # Gris para fold
            ((0, 128, 0), 'check')     # Verde para check
        ]
        
        detected_buttons = []
        
        for color_range, action in button_colors:
            # Crear máscara para color
            lower = np.array([c-20 for c in color_range])
            upper = np.array([c+20 for c in color_range])
            mask = cv2.inRange(buttons_area, lower, upper)
            
            if np.sum(mask) > 1000:  # Si hay suficiente del color
                detected_buttons.append(action)
        
        return detected_buttons
    
    def is_button_color(self, color):
        """Verificar si un color es del botón de dealer GG Poker"""
        # GG Poker usa dorado (255, 215, 0)
        gold_color = np.array([255, 215, 0])
        return np.allclose(color, gold_color, atol=30)
    
    def ocr_region(self, image_area):
        """Realizar OCR en una región de imagen"""
        try:
            # Convertir a PIL
            pil_image = Image.fromarray(cv2.cvtColor(image_area, cv2.COLOR_BGR2RGB))
            
            # Preprocesar para mejor OCR
            gray = pil_image.convert('L')
            threshold = gray.point(lambda x: 0 if x < 200 else 255)
            
            # Realizar OCR
            text = pytesseract.image_to_string(threshold, config='--psm 7')
            return text.strip()
        except:
            return ""
    
    def get_platform_specific_decision(self, game_state):
        """Obtener decisión específica para GG Poker"""
        
        # Ajustes específicos de GG Poker
        decision = game_state.copy()
        
        # GG Poker tiene jugadores más loose
        if decision.get('street') == 'preflop':
            # Abrir más manos en GG Poker
            if decision.get('action') == 'RAISE':
                decision['size'] = decision.get('size', 2.2)
        
        return decision